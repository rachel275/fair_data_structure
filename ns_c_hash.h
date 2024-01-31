#ifndef __NCSHASH_H__
#define __NCSHASH_H__

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include <string.h>
#include <limits.h>
#include <math.h>
#include <stdbool.h>
#include "rdtsc.h"
#include "lock.h"

#define MIN_N 100
#define MAX_N 100000
#define MIN_M 10
#define MAX_M 1000

typedef struct Node{
    unsigned long long key;
    void *value;
    struct Node* next;
}Node;

typedef struct HeadNode{
    //unsigned long long key;
    //void *value;
    //struct Node* next;
}HeadNode;

typedef struct ncs_hash_table
{
    lock_t mutexes __attribute__ ((aligned (64)));
    size_t size;
    struct Node *table;
}ncs_hash_table;

typedef struct ncs_hash_table_stat {
    unsigned long long cs_time;
    unsigned long long wait_time;
    unsigned long long release_time;
    size_t n_ops;
    size_t op_durations_size;
    unsigned int *op_durations;
    unsigned int bucket_id;
    unsigned int nentries[MAX_M];
} ncs_hash_table_stat;

typedef struct ncs_hash_table NcsHashTable;

NcsHashTable* hash_init (size_t N, int totweight);
int hash_insert (NcsHashTable *hp, unsigned int k, void *v, ncs_hash_table_stat *stat);
int hash_delete (NcsHashTable *hp, unsigned int k, ncs_hash_table_stat *stat);
int hash_get (NcsHashTable *hp, unsigned int k, void **vptr);
void print_hash_stats(ncs_hash_table *hp);
void clear_hash_stats(ncs_hash_table *hp);

//unsigned long long insert_time = 0, delete_time = 0;

NcsHashTable* hash_init(size_t N, int tot_weight)
{
    // allocate space as big as table
    NcsHashTable *new_table;
    new_table = (NcsHashTable *) malloc(sizeof( NcsHashTable ));
    // initialize members
    new_table->size = N;
    new_table->table = (Node *) calloc(N, sizeof(Node));

    // init all mutex locks
#ifdef FAIRLOCK
    lock_init(&new_table->mutexes, tot_weight);
#else
    lock_init(&new_table->mutexes);
#endif
    return (new_table);
}

// Function inserting to hp hash table, key k and v value of k.
int hash_insert (ncs_hash_table *hp, unsigned int k, void *v, ncs_hash_table_stat *stat)
{
    size_t bucket_idx = k % hp->size;
    unsigned long long start, end;//, wait, release;
    struct Node* toAdd;
    int insert;
    unsigned int duration;

    //wait = rdtscp();
    //printf("(0)Trying lock:  %llu\n", wait);
    lock_acquire(&hp->mutexes);
    start = rdtscp();

    toAdd = (struct Node*)malloc(sizeof(struct Node));
    struct Node* bucket = &hp->table[bucket_idx];

    insert = 1;
    /*
    searched = 0;
    while (bucket->next && searched++ < 10) {
        if (bucket->next->key == k) {
            insert = 0;
            goto done;
        }
        bucket = bucket->next;
    }
    */

    while(bucket->next != NULL){
        bucket = bucket->next;
    }
    toAdd->key = k;
    toAdd->next = bucket->next;
    toAdd->value = v;
    bucket->next = toAdd;

    end = rdtscp();
    lock_release(&hp->mutexes);
    //release = rdtscp();
    //printf("(0)Lock obtained:  %llu\n", start);
    //printf("(0)Lock released:  %llu\n", end);
    //printf("Insert_time = %llu, wait time = %llu\n", (end - start), (start - wait));
    duration = end - start;

#ifdef CS_DIST
    if (stat->n_ops < stat->op_durations_size)
        stat->op_durations[stat->n_ops++] = release - end;
#endif
    //stat->cs_time += duration;
    stat->cs_time = duration;
    stat->bucket_id = bucket_idx;
    stat->nentries[bucket_idx]++;
    //stat->wait_time += (start - wait);
    //stat->release_time += release - end;
    return insert;
}

// Function deleting from hp hash table, key k and it's properties
int hash_delete (ncs_hash_table *hp, unsigned int k, ncs_hash_table_stat *stat)
{
    struct Node* toDelete;

    size_t bucket_idx = k % hp->size;
    int found = 0;
    unsigned long long start, end;//, wait, release;
    unsigned int duration;

    //printf("(1)Trying lock:  %llu\n", wait);
    //wait = rdtscp();
    lock_acquire(&hp->mutexes);
    start = rdtscp();
    struct Node* bucket = &hp->table[bucket_idx];

    while(bucket->next != NULL){
        if(bucket->next->key == k){
            toDelete = bucket->next;
            bucket->next = bucket->next->next;
            free(toDelete);
            found++;
        } else {
            bucket = bucket->next;
        }
    }

    end = rdtscp();
    lock_release(&hp->mutexes);
    //release = rdtscp();
    //printf("(1)Lock obtained:  %llu\n", start);
    //printf("(1)Lock released:  %llu\n", end);
    //printf("Delete_time = %llu, wait time = %llu\n", (end - start), (start - wait));
    duration = end - start;
#ifdef CS_DIST
    if (stat->n_ops < stat->op_durations_size)
        stat->op_durations[stat->n_ops++] = duration;
#endif
    stat->cs_time += duration;
    stat->nentries[bucket_idx]++;
    //stat->wait_time += start - wait;
    //stat->release_time += release - end;
    return found;
}

// Function returning 0 on success, -1 on fail
// Retrieves key k's value into vptr from hash table hp
int hash_get (ncs_hash_table *hp, unsigned int k, void **vptr){
    // finding the correct bucket
    size_t bucket_idx = k % hp->size;

    // locking respective region
    lock_acquire(&hp->mutexes);
    struct Node* bucket = hp->table[bucket_idx].next;

    // iterate to find the key
    while(bucket != NULL){
        // when key's found
        if(bucket->key == k){
            *vptr = bucket->value;
            lock_release(&hp->mutexes);
            return 0;
        }
        bucket = bucket->next;
    }
    lock_release(&hp->mutexes);

    return -1;
}

#endif /* __HASH_H__ */
