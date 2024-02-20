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
//    int priority;
    int id;
    int ncpu;
    list_stat_t stat;
} task_t __attribute__ ((aligned (64)));

void setup_worker(task_t *task) {
    int ret;
    if (task->ncpu != 0) {
	cpu_set_t cpuset;
	CPU_ZERO(&cpuset);
	//for (int i =0; i < task->ncpu; i++){
	CPU_SET(task->ncpu, &cpuset);
	//}
	ret = pthread_setaffinity_np(pthread_self(), sizeof(cpu_set_t), &cpuset);
	if (ret != 0) {
	    perror("pthread_set_affinity_np");
	    exit(-1);
	}
    }
//    pid_t tid = gettid();
//    ret = setpriority(PRIO_PROCESS, tid, task->priority);
//    if (ret != 0) {
//	perror("setpriority");
//	exit(-1);
   // }
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
	    "id: %02d / "
        "number of operations: %lli / "
        "number of entries: %i / "
	    "tot_time(ms): %10.3f / "
	    "max_time(ms): %10.3f / \n",
	    type,
	    task->id,
        (int)task->stat.n_ops,
        (int)task->stat.op_entries,
	    task->stat.tot_cs_time / (float) (CYCLE_PER_US * 1000),
	    task->stat.wc_cs_time / (float) (CYCLE_PER_US * 1000));
}

void *insertfunc(void *vargp)
{
    task_t *task = (task_t *) vargp;
    setup_worker(task);
    int entry = task->id;

    // /*loop continuously*/
    while(!*task->stop){
            //printf("step 1.a\n");
      /*add to the linked list*/
        entry = ((fast_rand() % key_space)  + task->id);
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
        //printf("step 1.b\n");
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
        //printf("%i ", nratio[i]);
        test_insert_ratio += ((nratio[i] * 8) / 100);
        test_find_ratio += (((100 - nratio[i]) * 8) / 100);
    }

    test_duration = atoi(argv[napplications + 2]);       //the time the test shall run for
    //printf ("apps: %i, durations: %i", napplications, test_duration);

    /*now we need to see how many threads of each type we want and make sure we are setting them for each applicaiton...*/
    /*how do we split up the keyspace*/

    //printf("insert: %i      find: %i        \n", test_insert_ratio, test_find_ratio);
    int stop __attribute__((aligned (64))) = 0;
    int ncpu = 0;
    task_t *insert_tasks = malloc(sizeof(task_t) * (test_insert_ratio));
    task_t *find_tasks = malloc(sizeof(task_t) * (test_find_ratio));
    task_t *delete_tasks = malloc(sizeof(task_t) * (test_delete_ratio));

    int rc;
    key_space = (test_find_ratio * 50);

    List_Init(&list);

    // /*set up the linked list before hand*/
    // for (int n = 0; n < key_space; n++){
    //     list_insert(&list, n, &n, &dummy, (n % (test_find_ratio)));
    // }

    for (int i = 0; i < napplications; i++){
        for (int j = 0; j < ((nratio[i] * 8) / 100); j++){
            insert_tasks[j].id = i; //work on this so the id's are related
    	    insert_tasks[j].ncpu = i; //j;//2*(j + i) + 1;
            insert_tasks[j].stop = &stop;
        }

        for (int j = 0; j < (((100 - nratio[i]) * 8) / 100); j++){
            find_tasks[j].id = i;
    	    find_tasks[j].ncpu = i;//napplications - j;//2*(j + i);
            find_tasks[j].stop = &stop;
        }
    } 
    printf("step 1\n");

  /*now that we've orgainsed the threads we need to  */

    for (int k = 0; k < test_insert_ratio; k++){
        rc = pthread_create(&insert_tasks[k].thread, &attr, insertfunc, &insert_tasks[k]);
        if (rc){
            printf("Error:unable to create insert thread, %d\n", rc);
            exit(-1);
        }
    }

    printf("step 2\n");  

    for (int k = 0; k < test_find_ratio; k++){
        rc = pthread_create(&find_tasks[k].thread, &attr, findfunc, &find_tasks[k]);
        if (rc){
            printf("Error:unable to create find thread, %d\n", rc);
            exit(-1);
        }
    }
    printf("step 3\n");
    for (int k = 0; k < test_delete_ratio; k++){
        rc = pthread_create(&delete_tasks[k].thread, &attr, deletefunc, &delete_tasks[k]);
        if (rc){
            printf("Error:unable to create delete thread, %d\n", rc);
            exit(-1);
        }
    }

    printf("step 4\n");
    sleep(test_duration); 

    stop = 1;

    printf("step 5\n");
    for (int p = 0; p < (test_insert_ratio); p++){
        pthread_join(insert_tasks[p].thread, NULL);
    }


    for (int p = 0; p < (test_find_ratio); p++){
        pthread_join(find_tasks[p].thread, NULL);
    }

    for (int p = 0; p < (test_delete_ratio); p++){
        pthread_join(delete_tasks[p].thread, NULL);
    }

    return 0;
}
