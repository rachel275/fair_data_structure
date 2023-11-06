/*simple linked list with insert and find functions*/
#include "linked_list.h"
#include <math.h>

/*********************************** Code for the Linked List *************************************/
typedef struct _node_t {
    int data;
    struct _node_t *next;
} node_t;

typedef struct _list_t {
    node_t *head;
    pthread_mutex_t lock;
} list_t;

void List_Init(list_t *list){
    list->head = NULL;
    pthread_mutex_init(&list->lock, NULL);
}

void insert(list_t *list, int data){
    /*add the thread id as the data of the node_t*/
    node_t *thread_node_t = (node_t *)malloc(sizeof(node_t));
    thread_node_t->data = data;

    pthread_mutex_lock(&list->lock);        
        thread_node_t->next = list->head;
        list->head = thread_node_t;
    pthread_mutex_unlock(&list->lock);
}

void insert_unique(list_t *list, int data){

    /*in this case we don't to always add the task id*/
    pthread_mutex_lock(&list->lock); 
        node_t *n = list->head;
        while (n){
        if (n->data == data) {
            return;
        }
        n = n->next;
        }

        /*don't assign memory until we are sure to use it*/
        node_t *thread_node_t = (node_t *)malloc(sizeof(node_t));
        thread_node_t->data = data;
        thread_node_t->next = list->head;
        list->head = thread_node_t;
    pthread_mutex_unlock(&list->lock);
}

node_t *find(list_t *list, int data){
    pthread_mutex_lock(&list->lock);
        node_t *n = list->head;
        while (n){
        if (n->data == data) {
            //unlock();
            return n;
        }
        n = n->next;
        }
    pthread_mutex_unlock(&list->lock);
    return NULL;
}


/********************************** Global Variables *****************************************/
int thread_status[100] = {STOPPED};
int test_threads = DEFAULT_THREADS;  /*=to some input, set this one when it is first run*/
int current_threads;                 /*this values is to be built up to*/
list_t list;                         /*global linked list*/

unsigned int test_duration = DEFAULT_DURATION;
unsigned int test_wait_duration = DEFAULT_WAIT;
unsigned int test_spec = DEFAULT_SPEC;
//unsigned int test_scenario[SCENARIO_SIZE] = {};

typedef struct {
    volatile int *stop;
    pthread_t thread;
    int id;
    ull operation_executed;
    //ull inserts_executed;
    //ull lookups_executed;
    //int current operation;
} task_t __attribute__ ((aligned (64)));


pthread_attr_t attr;

/********************************* Main Functions *******************************************/
void *myThreadFun(void *vargp)
{
    /*get the thread id*/
    task_t *task = (task_t *) vargp;

    int counter = 1;
    int entry = task->id;

    /*loop continuously*/
    while(thread_status[task->id]){
      /*add to the linked list*/
        switch (test_spec/*[task->id]*/)
        {
        case INSERT:
            insert(&list, entry);
            task->operation_executed++;
            break;
        case INSERT_UNIQUE:
            insert_unique(&list, entry);
            task->operation_executed++;
            break;
        // case LOOKUP:
        //     find(&list, entry);
        //     task->operation_executed++;
        //     break;
        default:
            break;
        }
        counter++;
        entry = (task->id + (10 * counter));
    }
}
  

int main(int argc, char **argv)
{
    int int_test_scenario = 0;
    int thread_alternate = FALSE;

    struct option long_options[] = 
    {
      // These options don't set a flag
    //  {"duration",                  required_argument, NULL, 'd'},
      {"threads",                   required_argument, NULL, 't'},
    //  {"wait",                      required_argument, NULL, 'w'},
      {"spec",                      required_argument, NULL, 'p'},
      {"scenario",                  required_argument, NULL, 's'},  /*scenario 1: they all run the same, scenario 2: they all start at intervals, scenario 3: they alternate scenario, 5, 6, 7: mix of the last three*/  
      {NULL, 0, NULL, 0}
    };

    int i;
    char c;

    while(1) 
    {
      i = 0;
      c = getopt_long(argc, argv, "t:p:s:", long_options, &i);

      if(c == -1)
	    break;
    
      if(c == 0 && long_options[i].flag == 0)
	    c = long_options[i].val;

      switch(c) {
	    case 0:
            break;
        // case 'd':
        //     test_duration = atoi(optarg);
	    //     break;
	    case 't':
	        test_threads = atoi(optarg);
	        break;
    	// case 'w':
	    //     test_wait_duration = atoi(optarg);
	    //     break;
    	case 'p':
	        test_spec = atoi(optarg);
	        break;
        case 's':
	        int_test_scenario = atoi(optarg);
	        break;
        default:
	    exit(1);
        }
    }

    int stop __attribute__((aligned (64))) = 0;
    ull total_executions = 0;
    task_t *tasks = malloc(sizeof(task_t) * test_threads);
    for (int k = 0; k < test_threads; k++) {
            tasks[k].stop = &stop;
            tasks[k].id = k;
            tasks[k].operation_executed = 0;
    }

    //thread_time[test_threads][TIMES] = {};

    int rc;
    int j;

    switch (int_test_scenario)
    {
    case 1:
        test_duration = scenario_one[2];
        thread_alternate = scenario_one[1];
        test_wait_duration = scenario_one[0];
        break;
    case 2:
        test_duration = scenario_two[2];
        thread_alternate = scenario_two[1];
        test_wait_duration = scenario_two[0];
        break;
    case 3:
        test_duration = scenario_three[2];
        thread_alternate = scenario_three[1];
        test_wait_duration = scenario_three[0];
        break;
    default:
        test_duration = scenario_one[2];
        thread_alternate = scenario_one[1];
        test_wait_duration = scenario_one[0];
        break;
    }

    //thread_running = RUNNING;
    int new_test_duration = 1;


    if(test_threads > 1){
        if (test_wait_duration > (test_duration / (test_threads - 1))){
            printf("Error:unable to use wait duration\n");
            exit(-1);
        }
        new_test_duration = test_duration - (test_wait_duration * (test_threads - 1));
    }

    List_Init(&list);

    pthread_attr_init(&attr);
    pthread_attr_setstacksize (&attr, (size_t)STACKSIZE);

    for (j = 0; j < test_threads; j++){

        thread_status[j] = RUNNING;
        rc = pthread_create(&tasks[j].thread, &attr, myThreadFun, &tasks[j]);
        if (rc) {
            printf("Error:unable to create thread, %d\n", rc);
            exit(-1);
        }
        current_threads++;
        if(j != test_threads){
            sleep(test_wait_duration);
            if(thread_alternate == TRUE){
                thread_status[j] = SLEEP;
            }
        }
    }

    if(thread_alternate == TRUE){
        for (j = 0; j < test_threads; j++){
            thread_status[j] = RUNNING;
            sleep(test_wait_duration);
            thread_status[j] = SLEEP;
        }
    } else {
        sleep(new_test_duration); 
    }

    stop = 1;
    for (j = 0; j < test_threads; j++){
        thread_status[j] = STOPPED;
    }

    //float variances[100];
    double thread_data[100][3];

    /*add in code here for find variance*/
    for (int p = 0; p < test_threads; p++){
        pthread_join(tasks[p].thread, NULL);
        total_executions = total_executions + tasks[p].operation_executed;
    }

    for (int m = 0; m < test_threads; m++){
        // printf("Thread %i: Number of insertions: %i    Average index postition: %.2f    Variance of index position: %.2f   \n", tasks[m].id, (int)tasks[m].operation_executed, averages[m], variances[m]);        
        printf("Thread %i: Number of insertions: %i        Average index postition: %.2f        Maximum index postition: %i       Minimum index postition: %i\n", tasks[m].id, 
                                                                                                                                                                    (int)tasks[m].operation_executed, 
                                                                                                                                                                    0.0, //thread_data[m][0], 
                                                                                                                                                                    0, //(int)thread_data[m][1], 
                                                                                                                                                                    0); //(int)thread_data[m][2]);        

    }

    printf("The total executions is %i\n", (int)total_executions);
    //pthread_exit(NULL);
    return 0;
}



/*Scenarios: What do we want to measure?*/
/*Start with two threads: 
    start by adding values to the linked list. - How do you keep track of who has added what to a list - they could add their task id? Look at the fairness of the list after x, y, and z*/
/*Then look at them accessing their items: how long does it take, which can make the most accesses, is there a clear winner and how does that relate to the adding values and the linked list*/

/*How does running one thread for x time before adding another one affect the unfairness?*/

/*run for x amount of time, with x number of threads*/

/*Want the number of insertions each thread makes, and then an occurence map of some sort, i.e. where are they placed.*/

/*The total number of insertions*/

/*The number of insertions of each thread*/

/*Can we come up with a measure of fairness?? - Jain's Index of fairness is simply the number of entries fair*/

