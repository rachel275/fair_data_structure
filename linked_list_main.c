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
/*simple linked list with insert and find functions*/
#include "rdtsc.h"

#ifdef NSC
#include "ns_c_linked_list.h"
#elif NSCLOCK
#include "ns_c_linked_list_lock.h"
#else
#include "linked_list.h"
#endif

#define THREADS_PER_APP  4

typedef struct {
    volatile int *stop;
    pthread_t thread;
    int priority;
    int app_id;
    int ncpu;
    list_stat_t stat;
} task_t __attribute__ ((aligned (64)));

void setup_worker(task_t *task) {
    int ret;
	cpu_set_t cpuset;
	CPU_ZERO(&cpuset);
	CPU_SET(task->ncpu, &cpuset);
	ret = pthread_setaffinity_np(pthread_self(), sizeof(cpu_set_t), &cpuset);
	if (ret != 0) {
	    perror("pthread_set_affinity_np");
	    exit(-1);
	}
    pid_t tid = gettid();
    ret = setpriority(PRIO_PROCESS, tid, task->priority);
    if (ret != 0) {
	perror("setpriority");
	exit(-1);
    }
}

#define RAND_MAX 0x7fffffff
uint rseed = 0;

// https://rosettacode.org/wiki/Linear_congruential_generator
uint fast_rand() {
    return rseed = (rseed * 1103515245 + 12345) & RAND_MAX;
}

/********************************** Global Variables *****************************************/
int test_threads = DEFAULT_THREADS;  /*=to some input, set this one when it is first run*/
list_t list;                         /*global linked list*/

unsigned int test_duration = DEFAULT_DURATION;
unsigned int test_wait_duration = DEFAULT_WAIT;
unsigned int test_delete_ratio = 0;
unsigned int test_insert_ratio = 0; 
unsigned int test_find_ratio = 0;
unsigned int key_space = 0;
unsigned int napplications = 0;
unsigned int nratio[100];

pthread_attr_t attr;



/********************************* Main Functions *******************************************/
void print_summary(char * type, task_t *task/*, ull tot_time, char *buffer*/) {
    printf("%s "
	    "app id: %02d / "
        "number of operations: %i / "
	    "tot_time(ms): %10.3f / "
	    "max_time(ms): %10.3f / \n",
	    type,
	    task->app_id,
        (int)task->stat.n_ops,
	    task->stat.tot_cs_time / (float) (CYCLE_PER_US * 1000),
	    task->stat.wc_cs_time / (float) (CYCLE_PER_US * 1000));
#if defined(FAIRLOCK) && defined(DEBUG) && defined(NSC)
    flthread_info_t *info = pthread_getspecific(list.mutexes.flthread_info_key);
    printf("  LHT: %llu	\n",
          // "  own_slice_wait %llu\n"
           //"  lock opportunity %llu\n"
           //"  runnable_wait %10.3f\n"
           //"  total slice 1 %10.3f\n"
           //"  total slice 2  %llu\n",
            //"  reenter %llu\n"
            //"  banned(actual) %llu\n"
            //"  banned %llu\n"
            //"  elapse %llu\n",
           // task->stat.n_ops - info->stat.reenter,
            //info->stat.own_slice_wait,
            //info->stat.prev_slice_wait,
            //(float)info->stat.runnable_wait / CYCLE_PER_US,
            //task->stat.tot_cs_time / (float) (CYCLE_PER_US * 1000) + (float)info->stat.runnable_wait / CYCLE_PER_US + (float) info->stat.own_slice_wait / CYCLE_PER_US,
            info->stat.total_time / (CYCLE_PER_US * 1000));
            //info->stat.reenter,
           // info->stat.banned_time,
           // info->banned_until-info->stat.start,
            //info->start_ticks-info->stat.start);
#endif		  
#if defined(FAIRLOCK) && defined(DEBUG) && defined(NSCLOCK)
    struct head_node_t *thread_node = list.head;    
    flthread_info_t *info;
    while(thread_node != NULL){
         if(thread_node->thread_id == task->app_id){
	      info = pthread_getspecific(thread_node->mutexes.flthread_info_key);
	 }
	 thread_node = thread_node->th_next;
    }
    printf("  LHT: %llu \n",
          // "  own_slice_wait %llu\n"
           //"  lock opportunity %llu\n"
           //"  runnable_wait %10.3f\n"
           //"  total slice 1 %10.3f\n"
           //"  total slice 2  %llu\n",
            //"  reenter %llu\n"
            //"  banned(actual) %llu\n"
            //"  banned %llu\n"
            //"  elapse %llu\n",
           // task->stat.n_ops - info->stat.reenter,
            //info->stat.own_slice_wait,
            //info->stat.prev_slice_wait,
            //(float)info->stat.runnable_wait / CYCLE_PER_US,
            //task->stat.tot_cs_time / (float) (CYCLE_PER_US * 1000) + (float)info->stat.runnable_wait / CYCLE_PER_US + (float) info->stat.own_slice_wait / CYCLE_PER_US,
            info->stat.total_time / (CYCLE_PER_US * 1000));
            //info->stat.reenter,
           // info->stat.banned_time,
           // info->banned_until-info->stat.start,
            //info->start_ticks-info->stat.start);
#endif


}

void *insertfunc(void *vargp)
{
    task_t *task = (task_t *) vargp;
    setup_worker(task);
    int entry = task->app_id;
 
  // /*loop continuously*/
    while(!*task->stop){
      /*add to the linked list*/
        entry = ((fast_rand() % key_space * 10)  + task->app_id);
        list_insert(&list, entry, &entry+entry, &task->stat, task->app_id);
//	printf("find ent: %llu   ", entry);
    }
    print_summary("insert", task);
    return NULL;
}

void *findfunc(void *vargp)
{
    task_t *task = (task_t *) vargp;
    setup_worker(task);
    int entry = task->app_id;

    // /*loop continuously*/
    while(!*task->stop){
    //  /*add to the linked list*/
        entry = (((1000000 - fast_rand()) % key_space * 10) + task->app_id);
        list_find(&list, entry, &task->stat, task->app_id);
    }
    print_summary("find", task);
    return NULL;
}

void *deletefunc(void *vargp)
{
    task_t *task = (task_t *) vargp;
    setup_worker(task);
    int entry = task->app_id;

    // /*loop continuously*/
    while(!*task->stop){
      /*add to the linked list*/
        entry = ((fast_rand() % (500)));
        list_delete(&list, entry, &task->stat, task->app_id);
    }
    print_summary("delete", task);
    return NULL;
}

int main(int argc, char **argv)
{
    if (argc < 3) {
	printf("usage: %s <napplications> <ratio1> <ratio2> <...> <duration> \n", argv[0]);
	return 1;
    }
    napplications = atoi(argv[1]);
    if (argc < 2 + napplications) {
	printf("usage: %s <napplications> <ratio1> <ratio2> <...> <duration> \n", argv[0]);
	return 1;
    }

    for (int i = 0; i < napplications; i++){
        nratio[i] = atoi(argv[i+2]);
        test_insert_ratio += ((nratio[i] * THREADS_PER_APP) / 100);
        test_find_ratio += (((100 - nratio[i]) * THREADS_PER_APP) / 100);
    }

    test_duration = atoi(argv[napplications + 2]);       //the time the test shall run for
    int stop __attribute__((aligned (64))) = 0;
    int ncpu = 0;
    task_t *insert_tasks = malloc(sizeof(task_t) * (test_insert_ratio));
    task_t *find_tasks = malloc(sizeof(task_t) * (test_find_ratio));
    task_t *delete_tasks = malloc(sizeof(task_t) * (test_delete_ratio));

    int rc;
    key_space = ((test_insert_ratio + test_find_ratio) * 500);

    List_Init(&list);

    int h = 0; 
    int g = 0; 
    int ninserts = 0; 
    int nfinds = 0;
    for (int i = 0; i < napplications; i++){
        ninserts += ((nratio[i] * THREADS_PER_APP) / 100);
	for (h; h < ninserts; h++){
            insert_tasks[h].app_id = i;
    	    insert_tasks[h].ncpu = h + g;
	    insert_tasks[h].priority = 0;
            insert_tasks[h].stop = &stop;
        }

	    nfinds += (((100 - nratio[i]) * THREADS_PER_APP) / 100);
        for (g; g < nfinds; g++){
	    find_tasks[g].app_id = i;
    	    find_tasks[g].ncpu = g + h;
	    find_tasks[g].priority = 0;
            find_tasks[g].stop = &stop;
        }
    } 

    for (int k = 0; k < test_insert_ratio; k++){
        rc = pthread_create(&insert_tasks[k].thread, NULL, insertfunc, &insert_tasks[k]);
        if (rc){
            printf("Error:unable to create insert thread, %d\n", rc);
            exit(-1);
        }
    }


    for (int k = 0; k < test_find_ratio; k++){
        rc = pthread_create(&find_tasks[k].thread, NULL, findfunc, &find_tasks[k]);
	if (rc){
            printf("Error:unable to create find thread, %d\n", rc);
            exit(-1);
        }
    }


    for (int k = 0; k < test_delete_ratio; k++){
        rc = pthread_create(&delete_tasks[k].thread, NULL, deletefunc, &delete_tasks[k]);
        if (rc){
            printf("Error:unable to create delete thread, %d\n", rc);
            exit(-1);
        }
    }

    sleep(test_duration); 

    stop = 1;
	
    unsigned long long total_time = 0;
    for (int p = 0; p < (test_insert_ratio); p++){
         total_time += insert_tasks[p].stat.tot_cs_time;
	 pthread_join(insert_tasks[p].thread, NULL);
    }


    for (int p = 0; p < (test_find_ratio); p++){
	total_time += find_tasks[p].stat.tot_cs_time;
        pthread_join(find_tasks[p].thread, NULL);
    }

    for (int p = 0; p < (test_delete_ratio); p++){
        pthread_join(delete_tasks[p].thread, NULL);
    }

    printf("\nSpin_Lock_Opp: %10.3f \n ",
       (float)/* (test_duration * 1000) -*/ (total_time / (CYCLE_PER_US * 1000)));



    return 0;
}