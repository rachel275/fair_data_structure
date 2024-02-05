#ifndef NS_C_LINKED_LIST_H
#define NS_C_LINKED_LIST_H
/*simple linked list with insert and find functions*/
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
#include <getopt.h>
#include "lock.h"
#include "rdtsc.h"

#define DEFAULT_DURATION 5
#define DEFAULT_THREADS  1
#define DEFAULT_WAIT     0
#define DEFAULT_RATIO    1

#define STACKSIZE        1000000000

#define FALSE            0
#define TRUE             1

typedef unsigned long long ull;

typedef struct node_t {
    unsigned long long key;
    void* value;
    struct node_t *next;
} node_t;

typedef struct head_node_t {
    int thread_id;
    struct head_node_t *th_next;
    struct node_t *next;
} head_node_t;

typedef struct list_t {
    struct head_node_t *head;
    lock_t mutexes __attribute__ ((aligned (64)));
} list_t;

typedef struct list_stat {
    unsigned long long wc_cs_time;
    unsigned long long cs_time;
    unsigned long long tot_cs_time;
    size_t n_ops;
    unsigned int op_entries;
} list_stat_t;

void List_Init(list_t *list){
    list->head = NULL;
    lock_init(&list->mutexes);
}

void list_insert(list_t *list, int k, void * data, list_stat_t* stat, int pid){

    unsigned long long start, end;//, wait, release;
    unsigned int duration;

    /*create the node to add*/
    struct node_t *thread_node = (struct node_t *)malloc(sizeof(struct node_t));
    thread_node->value = data;
    thread_node->key = k;
    int insert = FALSE;
    lock_acquire(&list->mutexes);
    start = rdtscp();
    /*use thread id to index in to the linked list of that thread*/
    struct head_node_t *n = list->head;

//should this bit be inside the lock
    while (n){
        if (n->thread_id == pid) {
            /*found thread's list, add entry*/
       
            thread_node->next = n->next;
            n->next = thread_node;
            end = rdtscp();
            lock_release(&list->mutexes);
            insert = TRUE;
        }
        n = n->th_next;
    }

    /*if the thread id isn't found, create a new list at the bottom*/
    if (insert == FALSE){
        /*create new head node*/
        struct head_node_t *th_node = (struct head_node_t *)malloc(sizeof(struct head_node_t));
        th_node->thread_id = pid;

        /*fix it to the end of the list*/
        n = th_node;

        /*add the element to the front of the list*/       
        thread_node->next = th_node->next;
        th_node->next = thread_node;
        end = rdtscp();
        lock_release(&list->mutexes);
    }

    // duration = end - start;
    // if(duration > stat->wc_cs_time){stat->wc_cs_time = duration;}
    // stat->cs_time = duration;
    // stat->tot_cs_time += duration;
    stat->op_entries++;
    stat->n_ops++;
}

/*opportunity here for multiple locks*/
node_t *list_find(list_t *list, int k, list_stat_t* stat, int pid){
    
    unsigned long long start, end;//, wait, release;
    unsigned int duration;
    lock_acquire(&list->mutexes); 
    start = rdtscp(); 

    struct head_node_t *thread_node = list->head;    

        while(thread_node){
            if(thread_node->thread_id == pid){
                struct node_t *n = thread_node->next;
                while (n){
                if (n->key == k) {
                    end = rdtscp();
                    lock_release(&list->mutexes);
                    duration = end - start;
                    if(duration > stat->wc_cs_time){stat->wc_cs_time = duration;}
                    stat->cs_time = duration;
                    stat->tot_cs_time += duration;
                    stat->n_ops++;
                    duration = end - start;
                    stat->cs_time = duration;
                    return n;
                }
                n = n->next;
                }
            }    
            thread_node = thread_node->th_next;
        }    
    end = rdtscp();
    lock_release(&list->mutexes);
    duration = end - start;
    if(duration > stat->wc_cs_time){stat->wc_cs_time = duration;}
    stat->cs_time = duration;
    stat->tot_cs_time += duration;
    stat->n_ops++;
    return NULL;
            
}

int list_delete(list_t *list, int k, list_stat_t* stat, int pid){
    
    unsigned long long start, end;//, wait, release;
    unsigned int duration;

    
    struct node_t* toDelete;
    lock_acquire(&list->mutexes); 
    start = rdtscp();

    struct head_node_t *thread_node = list->head;

    while(thread_node){
        if(thread_node->thread_id == pid){
            struct node_t *n = thread_node->next;
            // If head node itself holds the key to be deleted 
            if (n != NULL && n->key == k) { 
                thread_node->next = n->next; // Changed head 
                free(n); // free old head 
            end = rdtscp();       
            lock_release(&list->mutexes);

            duration = end - start;
            if(duration > stat->wc_cs_time){stat->wc_cs_time = duration;}
            stat->cs_time = duration;
            stat->tot_cs_time += duration;
            stat->op_entries--;
            stat->n_ops++;
            return 1;
            }

            while (n->next != NULL){
                if (n->next->key == k) {
                    toDelete = n->next;
                    n->next = n->next->next;
                    free(toDelete);
                end = rdtscp();       
                lock_release(&list->mutexes);

                duration = end - start;
                if(duration > stat->wc_cs_time){stat->wc_cs_time = duration;}
                stat->cs_time = duration;
                stat->tot_cs_time += duration;
                stat->op_entries--;
                stat->n_ops++;
                return 1;
                } else {
                    n = n->next;
                }
            }
        }
        /*TODO: if this is the last entry in the list for that thread do we want to free the memory here?*/
        thread_node = thread_node->th_next;
    }    
    end = rdtscp();    
    lock_release(&list->mutexes);

    // duration = end - start;
    // if(duration > stat->wc_cs_time){stat->wc_cs_time = duration;}
    // stat->cs_time = duration;
    // stat->tot_cs_time += duration;
    stat->n_ops++;
    // return 0;
}

#endif /*LINKED_LIST_H*/
