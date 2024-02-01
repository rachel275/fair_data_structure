#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <pthread.h>
#include <sched.h>
#include <sys/resource.h>
#include <sys/syscall.h>
#include <inttypes.h>
#define gettid() syscall(SYS_gettid)
#include "rdtsc.h"
#include "hash.h"

typedef unsigned long long ull;
typedef struct {
    volatile int *stop;
    pthread_t thread;
    int priority;
    int id;
    double cs;
    int ncpu;
    // output
    ull lock_acquires;
    hash_table_stat stat;
} task_t __attribute__ ((aligned (64)));

hash_table *ht;

static inline unsigned int fast_rand() {
    static size_t lfsr = 0xDEADBEEFC0FFEE09;
    //lfsr = (lfsr>>1)|(((lfsr>>3)^(lfsr>>9)^(lfsr>>13)^(lfsr>>21)^(lfsr>>25)^(lfsr>>33)^(lfsr>>45)^(lfsr>>49)^(lfsr>>51)^(lfsr>>55))<<63);
    lfsr = (lfsr>>1)|(((lfsr>>3)^(lfsr>>13)^(lfsr>>25)^(lfsr>>33)^(lfsr>>49)^(lfsr>>55))<<63);
    return lfsr & 0x00FFFFFF;
    // lfsr *= 1103515245 + 12345;
    // return (unsigned int)(lfsr / 8) % 10000000;
}

void setup_worker(task_t *task) {
    int ret;

    if (task->ncpu != 0) {
	cpu_set_t cpuset;
	CPU_ZERO(&cpuset);
	for (int i = 0; i < task->ncpu; i++) {
	    /*
	    if (i < 8 || i >= 24)
		CPU_SET(i, &cpuset);
	    else if (i < 16)
		CPU_SET(i+8, &cpuset);
	    else
		CPU_SET(i-8, &cpuset);
		*/
	    CPU_SET(i, &cpuset);
	}
	ret = pthread_setaffinity_np(pthread_self(), sizeof(cpu_set_t), &cpuset);
	if (ret != 0) {
	    perror("pthread_set_affinity_np");
	    exit(-1);
	}
    }

    pid_t tid = gettid();
    ret = setpriority(PRIO_PROCESS, tid, task->priority);
    if (ret != 0) {
	perror("setpriority");
	exit(-1);
    }
#ifdef CS_DIST
    task->stat.op_durations_size = 100000000; // 100M
    task->stat.op_durations = malloc(task->stat.op_durations_size * sizeof(unsigned int));
#endif
    //printf("Setting priority of thread %d to %d\n", tid, task->priority);
}

void get_schedstat(char *buffer) {
    pid_t tid = gettid();
    pid_t pid = getpid();
    char path[256];
    snprintf(path, 256, "/proc/%d/task/%d/schedstat", pid, tid);
    int fd = open(path, O_RDONLY);
    if (fd < 0) {
	perror("open");
	exit(-1);
    }
    if (read(fd, buffer, 1024) <= 0) {
	perror("read");
	exit(-1);
    }
}

void print_summary(char * type, task_t *task, /*ull tot_time,*/ char *buffer) {
    printf("%s "
	    "id: %02d / "
	    //"lock_acquires %8llu "
        "worst_case_bucket_id: %i / "
	    //"tot_time(ms) %10.3f "
	    //"wait_time(ms) %10.3f "
	    "worst_case_lock_hold(ms): %10.3f / "
	    "tot_time(ms): %10.3f / "
        "no_operations: %i \n",
	    //"release_time(ms) %10.3f "
	    //"other_time(ms) %10.3f "
	    //"schedstat %s",
	    type,
	    task->id,
        0,
	    //task->lock_acquires,
	    //tot_time / (float) (CYCLE_PER_US * 1000),
	    //task->stat.wait_time / (float) (CYCLE_PER_US * 1000),
	    task->stat.wc_cs_time / (float) (CYCLE_PER_US * 1000),
	    task->stat.tot_cs_time / (float) (CYCLE_PER_US * 1000),
        (int)task->stat.n_ops);//,
	    //task->stat.release_time / (float) (CYCLE_PER_US * 1000),
	    //(tot_time-task->stat.wait_time-task->stat.cs_time-task->stat.release_time)/(float) (CYCLE_PER_US * 1000),
	    //buffer);
#if defined(FAIRLOCK) && defined(DEBUG)
    flthread_info_t *info = pthread_getspecific(ht->mutexes.flthread_info_key);
    printf("  slice %llu\n"
            "  own_slice_wait %llu\n"
            "  prev_slice_wait %llu\n"
            "  runnable_wait %llu\n"
            "  next_runnable_wait %llu\n"
            "  succ_wait %llu\n"
	    "  release_succ_wait %llu\n"
            "  reenter %llu\n"
            "  banned(actual) %llu\n"
            "  banned %llu\n"
            "  elapse %llu\n",
            task->lock_acquires - info->stat.reenter,
            info->stat.own_slice_wait,
            info->stat.prev_slice_wait,
            info->stat.runnable_wait,
            info->stat.next_runnable_wait,
            info->stat.succ_wait,
	    info->stat.release_succ_wait,
            info->stat.reenter,
            info->stat.banned_time,
            info->banned_until-info->stat.start,
            info->start_ticks-info->stat.start);
#endif
#ifdef CS_DIST
    snprintf(buffer, 1024, "data/cs_dist/%s%02d.stat", type, task->id);
    int fd = open(buffer, O_RDWR | O_CREAT, 0644);
    if (fd < 0) {
	perror("read");
	exit(-1);
    }
    int len;
    for (int i = 0; i < task->stat.n_ops; i++) {
	len = snprintf(buffer, 1024, "%u\n", (unsigned int) (task->stat.op_durations[i]/(CYCLE_PER_US/1000.0)));
	if (write(fd, buffer, len) < 0) {
	    perror("write");
	    exit(-1);
	}
    }
#endif
}


void print_summary_buckets(bucket_stat* stat) {
    printf(
	    "bucket_id: %02d / "
	    //"lock_acquires %8llu "
	    //"tot_time(ms) %10.3f "
	    //"wait_time(ms) %10.3f "
	    "worst_case_lock_hold(ms): %10.3f / "
	    "tot_time(ms): %10.3f / "
        "no_entries: %lld / "
        "no_operations: %lld \n",
	    //"release_time(ms) %10.3f "
	    //"other_time(ms) %10.3f "
	    //"schedstat %s",
	    stat->bucket_id,
        (double)stat->wc_cs_time / (float) (CYCLE_PER_US * 1000),
        (double)stat->tot_cs_time / (float) (CYCLE_PER_US * 1000),
        stat->op_entries, 
        stat->n_ops);
	    //task->stat.release_time / (float) (CYCLE_PER_US * 1000),
	    //(tot_time-task->stat.wait_time-task->stat.cs_time-task->stat.release_time)/(float) (CYCLE_PER_US * 1000),
	    //buffer);
}

void *insert_worker(void *arg) {
    task_t *task = (task_t *) arg;
    setup_worker(task);
    unsigned int k;
    //unsigned long long start, end;

    // loop
    //ull lock_acquires = 0;
    /*
    stat.op_durations_size = 100000000; // 100M
    stat.op_durations = malloc(stat.op_durations_size * sizeof(unsigned int));
    */
    //start = rdtsc();
    while (!*task->stop) {
	//k = fast_rand();
    k = 1;

    //fflush(stdout);
	//printf("Add key %d\n", k);
	hash_insert(ht, k, &k+k, &task->stat, task->id);

	//lock_acquires++;
    }
    //end = rdtsc();
    //task->lock_acquires = lock_acquires;

    char buffer[1024] = { 0 };
    get_schedstat(buffer);

    print_summary("insert", task, buffer);
    return NULL;
}

/*The futex worker here is replicating a normal thread that attempts to access a 
futex varaible and so is added to the futex hash table. Thus we have an insert 
(where it is put in the queue for that futex variable) and then we wait and random
amount of time, and then we remove the entry i.e. the thread gets the futex variable*/
/*An inode worker would be non-shared - how would this differ in application?*/
void *futex_worker(void *arg) {

    unsigned int k;
    task_t *task = (task_t *) arg;
    setup_worker(task);
    //unsigned long long start, end;

    // loop
    ull lock_acquires = 0;
    //start = rdtsc();
	k = fast_rand();
    while (!*task->stop) {
    
    //assume this is the hashed futexx address and thread id
	k = fast_rand();
    hash_insert(ht, k, &k+k, &task->stat, task->id);
	lock_acquires++;

    sleep((rand() % 10000) / 10000.0);

	hash_delete(ht, k, &task->stat, task->id); 
	lock_acquires++;

    sleep((rand() % 10000) / 10000.0);
    }
    //end = rdtsc();
    task->lock_acquires = lock_acquires;

    char buffer[1024] = { 0 };
    get_schedstat(buffer);

    print_summary("futex", task, buffer);
    return NULL;

}

void *delete_worker(void *arg) {
    unsigned int k;
    task_t *task = (task_t *) arg;
    setup_worker(task);
    //unsigned long long start, end;

    // loop
    ull lock_acquires = 0;
    //start = rdtsc();
    while (!*task->stop) {
	k = fast_rand();
	//printf("Delete key %d\n", k);
	hash_delete(ht, k, &task->stat, task->id);
	lock_acquires++;
    }
    //end = rdtsc();
    task->lock_acquires = lock_acquires;

    char buffer[1024] = { 0 };
    get_schedstat(buffer);

    print_summary("delete", task, buffer);
    return 0;
}

int main(int argc, char *argv[]) {
    if (argc < 6) {
	printf("usage: %s <nfutex> <nmalicious> <duration> <nbuckets> <ninititems> <prio> <..n> [NCPU]\n", argv[0]);
	return 1;
    }
    int nfutex = atoi(argv[1]);        //the number of futex threads
    //int nfutex = atoi(argv[1]);        //the number of threads inserting entries
    int nmalicous = atoi(argv[2]);      //the number of malicous threads inserting entries
    //int nmalicous = atoi(argv[2]);        //the number of threads deleting entries
    int nthreads = nfutex + nmalicous;   //the total number of threads
    int duration = atoi(argv[3]);       //the time the test shall run for
    int nbuckets = atoi(argv[4]);       //the number of buckets in the hashtable
    int ninititems = 0;//atoi(argv[5]);     //the number of items alreadt in the hashmap
    task_t *futex_tasks = calloc(nfutex, sizeof(task_t));
    task_t *mal_tasks = calloc(nmalicous, sizeof(task_t)); //should be nmalicous?
    if (argc < 5){ //6+nthreads) {
	printf("usage: %s <nfutex> <nmalicous> <duration> <nbuckets> <ninititems> <prio> <..n> [NCPU]\n", argv[0]);
	return 1;
    }

    int stop = 0;
    int tot_weight = 0;
    int ncpu = argc > 6 + nfutex + nmalicous ? atoi(argv[5+nthreads]) : 0;

    for (int i = 0; i < nfutex; i++) {
	futex_tasks[i].stop = &stop;
	//int priority = atoi(argv[6+i]);  //the priority assigned to each thread
	futex_tasks[i].priority = 1; //give each thread the same priority
#ifdef FAIRLOCK
	int weight = prio_to_weight[priority+20];
	tot_weight += weight;
#endif
	futex_tasks[i].ncpu = ncpu;
	futex_tasks[i].id = i;
    }
    for (int i = 0; i < nmalicous; i++) {
	mal_tasks[i].stop = &stop;
	//int priority = atoi(argv[6+nfutex+i]);
	mal_tasks[i].priority = 1; //priority;
#ifdef FAIRLOCK
	int weight = prio_to_weight[priority+20];
	tot_weight += weight;
#endif
	mal_tasks[i].ncpu = ncpu;
	mal_tasks[i].id = i;
    }

    ht = hash_init(nbuckets, tot_weight);

#ifdef FAIRLOCK
    fairlock_thread_init(&ht->mutexes, tot_weight);
#endif
    hash_table_stat dummy = {0};
    for (int i = 0; i < ninititems; i++) {
	hash_insert(ht, fast_rand(), &i+i, &dummy, 0);
    }

    for (int i = 0; i < nfutex; i++) {
	pthread_create(&futex_tasks[i].thread, NULL, futex_worker, &futex_tasks[i]);
    }
    for (int i = 0; i < nmalicous; i++) {
	pthread_create(&mal_tasks[i].thread, NULL, insert_worker, &mal_tasks[i]);
    }

    sleep(duration);

    stop = 1;


    for (int i = 0; i < nfutex; i++) { 
	pthread_join(futex_tasks[i].thread, NULL);
    }

    for (int i = 0; i < nmalicous; i++) {
	pthread_join(mal_tasks[i].thread, NULL);
    }

    // hash_table_stat final = {0};

    // for (int i = 0; i < nfutex; i++){ /*for each thread id - each of which has a stat bucket for each stat*/
    //     for(int j = 0; j < nbuckets; j++){ /*for each bucket*/
    //         final.b_stats[j].bucket_id = j;
    //         final.b_stats[j].n_ops += futex_tasks[i].stat.b_stats[j].n_ops;
    //         final.b_stats[j].op_entries+= futex_tasks[i].stat.b_stats[j].op_entries;
    //         final.b_stats[j].tot_cs_time += futex_tasks[i].stat.b_stats[j].tot_cs_time;
    //         if (final.b_stats[j].wc_cs_time < futex_tasks[i].stat.b_stats[j].wc_cs_time){
    //             final.b_stats[j].wc_cs_time = futex_tasks[i].stat.b_stats[j].wc_cs_time;
    //         }
    //     }
    // }


    // for (int i = 0; i < nmalicous; i++){
    //     for(int j = 0; j < nbuckets; j++){
    //         final.b_stats[j].bucket_id = j;
    //         final.b_stats[j].n_ops += mal_tasks[i].stat.b_stats[j].n_ops;
    //         final.b_stats[j].op_entries += mal_tasks[i].stat.b_stats[j].op_entries;
    //         //printf("op_entries = %lld", mal_tasks[i].stat.b_stats[j].op_entries);
    //         final.b_stats[j].tot_cs_time += mal_tasks[i].stat.b_stats[j].tot_cs_time;
    //         if (final.b_stats[j].wc_cs_time < mal_tasks[i].stat.b_stats[j].wc_cs_time){
    //             final.b_stats[j].wc_cs_time = mal_tasks[i].stat.b_stats[j].wc_cs_time;
    //         }
    //     }
    // }

    // for (int i = 0; i < nbuckets; i++){
    //     print_summary_buckets(&final.b_stats[i]);
    // }
    return 0;
}
