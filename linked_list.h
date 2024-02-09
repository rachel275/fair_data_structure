#ifndef LINKED_LIST_H
#define LINKED_LIST_H

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

typedef struct Node {
    unsigned long long key;
    void* value;
    struct Node *next;
} Node;

typedef struct list_t {
    Node *head;
    lock_t mutexes __attribute__ ((aligned (64)));
} list_t;

typedef struct list_stat {
    unsigned long long wc_cs_time;
    unsigned long long cs_time;
    unsigned long long tot_cs_time;
    unsigned long long tot_find_cs_time;
    unsigned long long wc_find_cs_time;
    size_t n_ops;
    unsigned int op_entries;
} list_stat_t;

void List_Init(list_t *list){
    list->head = NULL;
    lock_init(&list->mutexes);
}

void list_insert(list_t *list, int k, void *data, list_stat_t* stat, int pid){
    unsigned long long start, end;//, wait, release;
    unsigned int duration;

    /*add the thread id as the data of the Node*/
    Node *threadNode = (Node *)malloc(sizeof(Node));
    threadNode->value = data;
    threadNode->key = k;

    lock_acquire(&list->mutexes);
    start = rdtscp();
        threadNode->next = list->head;
        list->head = threadNode;
    end = rdtscp();
    lock_release(&list->mutexes);

    duration = end - start;
    if(duration > stat->wc_cs_time){stat->wc_cs_time = duration;}
    stat->cs_time = duration;
    stat->tot_cs_time += duration;
    stat->op_entries++;
    stat->n_ops++;

}

void list_insert_unique(list_t *list, void* data, list_stat_t* stat, int pid){
    unsigned long long start, end;//, wait, release;
    unsigned int duration;

    lock_acquire(&list->mutexes); 
    start = rdtscp();        
    Node *n = list->head;
        while (n){
        if (n->value == data) {
            return;
        }
        n = n->next;
        }

        /*don't assign memory until we are sure to use it*/
        Node *threadNode = (Node *)malloc(sizeof(Node));
        threadNode->value = data;
        threadNode->next = list->head;
        list->head = threadNode;
    end = rdtscp();    
    lock_release(&list->mutexes);


    // duration = end - start;
    // if(duration > stat->wc_cs_time){stat->wc_cs_time = duration;}
    // stat->cs_time = duration;
    // stat->tot_cs_time += duration;
    stat->op_entries++;
    stat->n_ops++;
}

Node *list_find(list_t *list, int k, list_stat_t* stat, int pid){
    unsigned long long start, end;//, wait, release;
    unsigned int duration;

    lock_acquire(&list->mutexes); 
    start = rdtscp(); 

    Node *n = list->head;
       
        while (n){
        if (n->key == k) {
            end = rdtscp();            
            lock_release(&list->mutexes);
            duration = end - start;
            if(duration > stat->wc_cs_time){stat->wc_cs_time = duration;}
            stat->cs_time = duration;
            stat->tot_cs_time += duration;
            stat->n_ops++;
            return n;
        }
        n = n->next;
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
    //unsigned int found = 0;

    Node* toDelete;
    lock_acquire(&list->mutexes); 
        start = rdtscp();
            
        Node *n = list->head;

        // If head node itself holds the key to be list_deleted 
        if (n != NULL && n->key == k) { 
            list->head = n->next; // Changed head 
            free(n);
            
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
    end = rdtscp();    
    lock_release(&list->mutexes);

    duration = end - start;
    if(duration > stat->wc_cs_time){stat->wc_cs_time = duration;}
    stat->cs_time = duration;
    stat->tot_cs_time += duration;
    stat->n_ops++;
    return 0;
}

#endif /*LINKED_LIST_H*/