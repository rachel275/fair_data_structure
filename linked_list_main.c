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

typedef struct {
    volatile int *stop;
    pthread_t thread;
    int priority;
    int id;
    int ncpu;
    list_stat_t stat;
} task_t __attribute__ ((aligned (64)));

void setup_worker(task_t *task) {
    int ret;

    if (task->ncpu != 0) {
	cpu_set_t cpuset;
	CPU_ZERO(&cpuset);
	for (int i = 0; i < task->ncpu; i++) {
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
}

//#include <math.h>

// static inline unsigned int fast_rand() {
//     static size_t lfsr = 0xDEADBEEFC0FFEE09;
//     //lfsr = (lfsr>>1)|(((lfsr>>3)^(lfsr>>9)^(lfsr>>13)^(lfsr>>21)^(lfsr>>25)^(lfsr>>33)^(lfsr>>45)^(lfsr>>49)^(lfsr>>51)^(lfsr>>55))<<63);
//     lfsr = (lfsr>>1)|(((lfsr>>3)^(lfsr>>13)^(lfsr>>25)^(lfsr>>33)^(lfsr>>49)^(lfsr>>55))<<63);
//     return lfsr & 0x00FFFFFF;
//     // lfsr *= 1103515245 + 12345;
//     // return (unsigned int)(lfsr / 8) % 10000000;
// }

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
unsigned int test_nmalicious = 0;
unsigned int test_insert_find_ratio = 0;
unsigned int test_delete_ratio = 0;
unsigned int test_insert_ratio = 0; 
unsigned int test_find_ratio = 0;
unsigned int key_space = 0;

pthread_attr_t attr;



/********************************* Main Functions *******************************************/
void print_summary(char * type, task_t *task/*, ull tot_time, char *buffer*/) {
    printf("%s "
	    "id: %02d / "
        "number of operations: %lli / "
        "number of entries: %i / "
	    "tot_time(ms): %10.3f / "
	    "max_time(ms): %10.3f / \n",
	    // "tot_find_time(ms): %10.3f / "
	    // "max_find_time(ms): %10.3f /\n ",
	    type,
	    task->id,
        (int)task->stat.n_ops,
        (int)task->stat.op_entries,
	    task->stat.tot_cs_time / (float) (CYCLE_PER_US * 1000),
	    task->stat.wc_cs_time / (float) (CYCLE_PER_US * 1000));
        // task->stat.tot_find_cs_time / (float) (CYCLE_PER_US * 1000),
	    // task->stat.wc_find_cs_time / (float) (CYCLE_PER_US * 1000));
}

// void *threadfunc(void *vargp)
// {
//     /*get the thread id*/
//     task_t *task = (task_t *) vargp;
//     setup_worker(task);
//     int counter = -1;
//     int entry = task->id;

//     /*loop continuously*/
//     while(!*task->stop){
//       /*add to the linked list*/
//     counter++;
//     entry = (task->id + (10 * counter));
//     list_insert(&list, entry, &entry, &task->stat, task->id);
//     sleep((fast_rand() % 1000) / 1000.0);

//     entry = (task->id + ((fast_rand() % (100)) * 10));
//     list_find(&list, entry, &task->stat, task->id);
//     sleep((fast_rand() % 1000) / 1000.0);
//     }

//     print_summary("insert_find", task);
//     return NULL;
// }

// void *malfunc(void *vargp)
// {
//     task_t *task = (task_t *) vargp;
//     setup_worker(task);
//     int entry = task->id;

//     // /*loop continuously*/
//     while(!*task->stop){
//       /*add to the linked list*/
//         list_insert(&list, entry, &entry, &task->stat, task->id);
//     }
//     print_summary("malicious", task);
//     return NULL;
// }

void *insertfunc(void *vargp)
{
    task_t *task = (task_t *) vargp;
    setup_worker(task);
    int entry = task->id;

    // /*loop continuously*/
    while(!*task->stop){
      /*add to the linked list*/
        entry = ((fast_rand()));
        list_insert(&list, entry, &entry+entry, &task->stat, task->id);
        //sleep((fast_rand() % 1000) / 1000.0);
    }
    print_summary("insert", task);
    return NULL;
}

void *findfunc(void *vargp)
{
    task_t *task = (task_t *) vargp;
    setup_worker(task);
    int entry = task->id;

    // /*loop continuously*/
    while(!*task->stop){
      /*add to the linked list*/
        entry = ((fast_rand() % (key_space)) + task->id);
        list_find(&list, entry, &task->stat, task->id);
        //sleep((fast_rand() % 1000) / 1000.0);
    }
    print_summary("find", task);
    return NULL;
}

void *deletefunc(void *vargp)
{
    task_t *task = (task_t *) vargp;
    setup_worker(task);
    int entry = task->id;

    // /*loop continuously*/
    while(!*task->stop){
      /*add to the linked list*/
        entry = ((fast_rand() % (500)));
        list_delete(&list, entry, &task->stat, task->id);
        sleep((fast_rand() % 1000) / 1000.0);
    }
    print_summary("delete", task);
    return NULL;
}


  

int main(int argc, char **argv)
{

    struct option long_options[] = 
    {
      // These options don't set a flag
      //{"nregular",                   required_argument, NULL, 'n'},
     //{"nmalicious",                    required_argument, NULL, 'm'},
      {"duration",                   required_argument, NULL, 't'},
      {"insert_ratio",               required_argument, NULL, 'i'},
      {"find_ratio",                 required_argument, NULL, 'f'},
      {"delete_ratio",               required_argument, NULL, 'd'},
      {NULL, 0, NULL, 0}
    };

    int i;
    char c;

    while(1) 
    {
      i = 0;
      c = getopt_long(argc, argv, "t:n:m:i:f:d:", long_options, &i);

      if(c == -1)
	    break;
    
      if(c == 0 && long_options[i].flag == 0)
	    c = long_options[i].val;

      switch(c) {
	    case 0:
            break;
        case 't':
            test_duration = atoi(optarg);
	        break;
	    // case 'n':
	    //     test_insert_find_ratio = atoi(optarg);
	    //     break;
        // case 'm':
        //     test_nmalicious = atoi(optarg);
	    //     break;
	    case 'i':
	        test_insert_ratio = atoi(optarg);
	        break;
	    case 'f':
	        test_find_ratio = atoi(optarg);
	        break;
	    case 'd':
	        test_delete_ratio = atoi(optarg);
	        break;
        default:
	    exit(1);
        }
    }

    int stop __attribute__((aligned (64))) = 0;
    int ncpu = test_insert_ratio + test_find_ratio + test_delete_ratio;
    // task_t *mal_tasks = malloc(sizeof(task_t) * (test_threads));
    // task_t *insert_find_tasks = malloc((sizeof(task_t) * (test_insert_find_ratio)));
    task_t *insert_tasks = malloc(sizeof(task_t) * (test_insert_ratio));
    task_t *find_tasks = malloc(sizeof(task_t) * (test_find_ratio));
    task_t *delete_tasks = malloc(sizeof(task_t) * (test_delete_ratio));

    int rc;
    key_space = (test_find_ratio * 50);

    List_Init(&list);

    // pthread_attr_init(&attr);
    // pthread_attr_setstacksize (&attr, (size_t)STACKSIZE);

    // for (int j = 0; j < test_nmalicious; j++){
    //     mal_tasks[j].id = j;
    // 	mal_tasks[i].ncpu = ncpu;
    //     mal_tasks[j].stop = &stop;
    // }
    /*set up the linked list before hand*/
    struct list_stat dummy = {0};
    for (int n = 0; n < key_space; n++){
        list_insert(&list, n, &n+n, &dummy, (n % (test_find_ratio)));
    }

    for (int j = 0; j < test_insert_ratio; j++){
        insert_tasks[j].id = j + test_find_ratio;
    	insert_tasks[j].ncpu = ncpu;
        insert_tasks[j].stop = &stop;
    }

    for (int j = 0; j < test_find_ratio; j++){
        find_tasks[j].id = j;
    	find_tasks[j].ncpu = ncpu;
        find_tasks[j].stop = &stop;
    }

    // for (int j = 0; j < test_insert_find_ratio; j++){
    //     insert_find_tasks[j].id = j;
    // 	insert_find_tasks[i].ncpu = ncpu;
    //     insert_find_tasks[j].stop = &stop;
    // }

    for (int j = 0; j < test_delete_ratio; j++){
        delete_tasks[j].id = j + test_insert_ratio + test_find_ratio;
    	delete_tasks[j].ncpu = ncpu;
        delete_tasks[j].stop = &stop;
    }

    // for (int k = 0; k < test_nmalicious; k++){
    //     rc = pthread_create(&mal_tasks[k].thread, &attr, malfunc, &mal_tasks[k]);
    //     if (rc){
    //         printf("Error:unable to create malicious thread, %d\n", rc);
    //         exit(-1);
    //     }
    // }

    // for (int k = 0; k < test_insert_find_ratio; k++){
    //     rc = pthread_create(&insert_find_tasks[k].thread, &attr, threadfunc, &insert_find_tasks[k]);
    //     if (rc){
    //         printf("Error:unable to create malicious thread, %d\n", rc);
    //         exit(-1);
    //     }
    // }

    for (int k = 0; k < test_insert_ratio; k++){
        rc = pthread_create(&insert_tasks[k].thread, &attr, insertfunc, &insert_tasks[k]);
        if (rc){
            printf("Error:unable to create insert thread, %d\n", rc);
            exit(-1);
        }
    }

    for (int k = 0; k < test_find_ratio; k++){
        rc = pthread_create(&find_tasks[k].thread, &attr, findfunc, &find_tasks[k]);
        if (rc){
            printf("Error:unable to create find thread, %d\n", rc);
            exit(-1);
        }
    }

    for (int k = 0; k < test_delete_ratio; k++){
        rc = pthread_create(&delete_tasks[k].thread, &attr, deletefunc, &delete_tasks[k]);
        if (rc){
            printf("Error:unable to create delete thread, %d\n", rc);
            exit(-1);
        }
    }

    sleep(test_duration); 

    stop = 1;
    // for (int p = 0; p < (test_nmalicious); p++){
    //     pthread_join(mal_tasks[p].thread, NULL);
    // }

    for (int p = 0; p < (test_insert_ratio); p++){
        pthread_join(insert_tasks[p].thread, NULL);
    }

    // for (int p = 0; p < (test_insert_find_ratio); p++){
    //     pthread_join(insert_find_tasks[p].thread, NULL);
    // }

    for (int p = 0; p < (test_find_ratio); p++){
        pthread_join(find_tasks[p].thread, NULL);
    }

    for (int p = 0; p < (test_delete_ratio); p++){
        pthread_join(delete_tasks[p].thread, NULL);
    }

    return 0;
}
