#ifndef __HASH_H__
#define __HASH_H__

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include <string.h>
#include <limits.h>
#include <math.h>
#include <stdbool.h>
//#include "rdtsc.h"
//#include "lock.h"
#include "linked_list.h"

#define MIN_M 10
#define MAX_M 1000

//What do you make this...

// typedef struct Node{
//     unsigned long long key;
//     void *value;
//     struct Node* next;
// }Node;

// typedef struct _list_t {
//     Node *head;
//     lock_t mutexes __attribute__ ((aligned (64)));
// } list_t;

typedef struct hash_table
{
    //lock_t mutexes __attribute__ ((aligned (64)));
    size_t size;
    //struct Node *table;
    struct list_t *table;
}hash_table;

typedef struct bucket_stat {
    unsigned int bucket_id;
    unsigned long long wc_cs_time;
    unsigned long long tot_cs_time;
    size_t n_ops;
    unsigned long long op_entries;
} bucket_stat;

typedef struct hash_table_stat {
    unsigned int bucket_id;
    //unsigned int nentries[MAX_M];
    struct list_stat stats[100];
    //struct bucket_stat b_stats[100];
    unsigned long long wc_cs_time;
    unsigned long long cs_time;
    unsigned long long tot_cs_time;
    size_t n_ops;
    unsigned int op_entries;
} hash_table_stat;

typedef struct hash_table HashTable;

HashTable* hash_init (size_t N, int totweight);
int hash_insert (HashTable *hp, unsigned int k, void *v, hash_table_stat *stat, int pid);
int hash_delete (HashTable *hp, unsigned int k, hash_table_stat *stat, int pid);
int hash_get (HashTable *hp, unsigned int k, void **vptr, hash_table_stat *stat, int pid);
void print_hash_stats(hash_table *hp);
void clear_hash_stats(hash_table *hp);

//unsigned long long insert_time = 0, delete_time = 0;

HashTable* hash_init(size_t N, int tot_weight)
{
    // allocate space as big as table
    HashTable *new_table;
    new_table = (HashTable *) malloc(sizeof( HashTable ));
    // initialize members
    new_table->size = N;
    new_table->table = calloc(N, sizeof(struct list_t));
    //new_table->buckets = (struct hash_bucket*) calloc(N, sizeof(struct hash_bucket)); /*create N versions of the buckets in an array*/

    // init all mutex locks
    for (int i = 0; i < N; i++){
        List_Init(&new_table->table[i]);
    }
// #ifdef FAIRLOCK
//     lock_init(&new_table->mutexes, tot_weight);
// #else
//     //lock_init(&new_table->mutexes);
// #endif
    return (new_table);
}

// Function inserting to hp hash table, key k and v value of k.
int hash_insert (hash_table *hp, unsigned int k, void *v, hash_table_stat *stat, int pid)
{
    
    size_t bucket_idx = k % hp->size;
    int insert;
    struct list_t* bucket = &hp->table[bucket_idx];
    insert = 1;


    list_insert(bucket, k, v, &stat->stats[bucket_idx], pid);


#ifdef CS_DIST
    if (stat->n_ops < stat->op_durations_size)
        stat->op_durations[stat->n_ops++] = release - end;
#endif

    stat->tot_cs_time += stat->stats[bucket_idx].cs_time;
    if (stat->wc_cs_time < stat->stats[bucket_idx].cs_time){
        stat->wc_cs_time = stat->stats[bucket_idx].cs_time;
        stat->bucket_id = bucket_idx;
    }
    stat->op_entries++;
    stat->n_ops++;
    return insert;
}

// Function deleting from hp hash table, key k and it's properties
int hash_delete (hash_table *hp, unsigned int k, hash_table_stat *stat, int pid)
{

    size_t bucket_idx = k % hp->size;
    int found = 0;
    struct list_t* bucket = &hp->table[bucket_idx];

    found = list_delete(bucket, k, &stat->stats[bucket_idx], pid);

    if (found == 1){
        stat->op_entries--;
    }
    stat->n_ops++;

    stat->tot_cs_time += stat->stats[bucket_idx].cs_time;
    if (stat->stats->wc_cs_time > stat->wc_cs_time){
        stat->wc_cs_time = stat->stats->wc_cs_time;
        stat->bucket_id = bucket_idx;
    }

    return found;
}

// Function returning 0 on success, -1 on fail
// Retrieves key k's value into vptr from hash table hp
int hash_get (hash_table *hp, unsigned int k, void **vptr, hash_table_stat *stat, int pid)
{
    // finding the correct bucket
    size_t bucket_idx = k % hp->size;

    //lock_acquire&hp->mutexes);
    struct list_t* bucket = &hp->table[bucket_idx];

    *vptr = list_find(bucket, k, &stat->stats[bucket_idx], pid)->value;

    stat->n_ops++;

    stat->tot_cs_time += stat->stats[bucket_idx].cs_time;
    if (stat->stats->wc_cs_time > stat->wc_cs_time){
        stat->wc_cs_time = stat->stats->wc_cs_time;
        stat->bucket_id = bucket_idx;
    }

    if (*vptr != NULL){
        return 0;
    } else {
        return -1;
    }
}

#endif /* __HASH_H__ */