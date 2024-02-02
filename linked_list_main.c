/*simple linked list with insert and find functions*/
#include "rdtsc.h"
#include "lock.h"


#ifdef NSC
#include "ns_c_linked_list.h"
#elif NSCLOCK
#include "ns_c_linked_list_lock.h"
#else
#include "linked_list.h"
#endif

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
unsigned int test_ninserts;
unsigned int test_delete_ratio = DEFAULT_RATIO;
unsigned int test_insert_ratio = DEFAULT_RATIO; 
unsigned int test_find_ratio = DEFAULT_RATIO;

typedef struct {
    volatile int *stop;
    pthread_t thread;
    int priority;
    int id;
    int ncpu;
    list_stat_t stat;
} task_t __attribute__ ((aligned (64)));

pthread_attr_t attr;

/********************************* Main Functions *******************************************/
void print_summary(char * type, task_t *task/*, ull tot_time, char *buffer*/) {
    printf("%s "
	    "id: %02d / "
	    //"lock_acquires %8llu "
        "number of operations: %lli / "
        "number of entries: %i / "
	    "tot_time(ms): %10.3f / "
	    "max_time(ms): %10.3f /\n ",
	    //"(ms): %10.3f \n ",
	    //"release_time(ms) %10.3f "
	    //"other_time(ms) %10.3f "
	    //"schedstat %s",
	    type,
	    task->id,
        (int)task->stat.n_ops,
        (int)task->stat.op_entries,
	    //task->lock_acquires,
	    task->stat.tot_cs_time / (float) (CYCLE_PER_US * 1000),
	    task->stat.wc_cs_time / (float) (CYCLE_PER_US * 1000));
	    //task->stat.cs_time / (float) (CYCLE_PER_US * 1000));//,
	    //task->stat.release_time / (float) (CYCLE_PER_US * 1000),
	    //(tot_time-task->stat.wait_time-task->stat.cs_time-task->stat.release_time)/(float) (CYCLE_PER_US * 1000),
	    //buffer);
}

void *threadfunc(void *vargp)
{
    /*get the thread id*/
    task_t *task = (task_t *) vargp;

    int counter = -1;
    int entry = task->id;

    /*loop continuously*/
    while(!*task->stop){
      /*add to the linked list*/
      for (int i = 0; i < test_insert_ratio; i++){
            counter++;
            entry = (task->id + (10 * counter));
            list_insert(&list, entry, &entry, &task->stat, task->id);

            sleep((fast_rand() % 10000) / 10000.0);
        
      }

      for (int i = 0; i < test_find_ratio; i++){

        entry = (task->id + ((fast_rand() % (100)) * 10));
        list_find(&list, entry, &task->stat, task->id);
        sleep((fast_rand() % 10000) / 10000.0);
        
      }

      for (int i = 0; i < test_delete_ratio; i++){
      /*getting a random number that's a multiple of the id.*/

        entry = (task->id + ((fast_rand() % (100)) * 10));
        list_delete(&list, entry, &task->stat, task->id);
        sleep((fast_rand() % 10000) / 10000.0);

      }
    }

    print_summary("genuine", task);; 
    return NULL;
}

void *insertfunc(void *vargp)
{
    task_t *task = (task_t *) vargp;

    int counter = -1;
    int entry = task->id;

    // /*loop continuously*/
    while(!*task->stop){
      /*add to the linked list*/
        list_insert(&list, entry, &entry, &task->stat, task->id);
    }
    print_summary("malicious", task);
    return NULL;
}
  
  

int main(int argc, char **argv)
{

    struct option long_options[] = 
    {
      // These options don't set a flag
      {"nregular",                   required_argument, NULL, 'n'},
      {"ninsert",                    required_argument, NULL, 'm'},
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
	    case 'n':
	        test_threads = atoi(optarg);
	        break;
        case 'm':
            test_ninserts = atoi(optarg);
	        break;
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
    task_t *test_tasks = malloc(sizeof(task_t) * (test_threads));
    task_t *mal_tasks = malloc(sizeof(task_t) * (test_ninserts));

    int rc;

    List_Init(&list);

    pthread_attr_init(&attr);
    pthread_attr_setstacksize (&attr, (size_t)STACKSIZE);

    for (int j = 0; j < test_threads; j++){
        test_tasks[j].id = j;
        test_tasks[j].stop = &stop;
    }

    for (int j = 0; j < test_ninserts; j++){
        mal_tasks[j].id = j;
        mal_tasks[j].stop = &stop;
    }

    for (int j = 0; j < test_threads; j++){
        rc = pthread_create(&test_tasks[j].thread, &attr, threadfunc, &test_tasks[j]);
        sleep(1);
        if (rc) {
            printf("Error:unable to create thread, %d\n", rc);
            exit(-1);
        }
    }

    for (int k = 0; k < test_ninserts; k++){
        rc = pthread_create(&mal_tasks[k].thread, &attr, insertfunc, &mal_tasks[k]);
        if (rc){
            printf("Error:unable to create thread, %d\n", rc);
            exit(-1);
        }
    }

    sleep(test_duration); 

    stop = 1;
    for (int p = 0; p < (test_threads); p++){
        pthread_join(test_tasks[p].thread, NULL);

    }
    for (int p = 0; p < (test_ninserts); p++){
        pthread_join(mal_tasks[p].thread, NULL);

    }

    return 0;
}
