#ifndef LINKED_LIST_H
#define LINKED_LIST_H
/*simple linked list with insert and find functions*/
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
#include <getopt.h>
  
#define RUNNING          1  /*the thread is running*/
#define STOPPED          0  /*the thread has either not been started or has been stopped*/
#define SLEEP            2
#define NOTHING          0  /*This thread is doing nothing*/

#define INSERT           1  /*This thread is inserting entries at a constant rate*/
#define INSERT_UNIQUE    2  /*This thread is inserting entires at a linear rate*/
#define LOOKUP           3  /*The thread is doing a lookup*/

#define DEFAULT_DURATION 5
#define DEFAULT_THREADS  1
#define DEFAULT_SPEC     INSERT
#define DEFAULT_WAIT     0

#define STACKSIZE        100000000

#define FALSE            0
#define TRUE             1

#define SCENARIO_SIZE   4

                        /*{Wait time(int), inverval(bool), insert time, lookup type}*/
const int scenario_one[]  =   {0, FALSE, 10, INSERT_UNIQUE};
const int scenario_two[]  =   {2, TRUE, 10, INSERT_UNIQUE};
const int scenario_three[]  =   {4, FALSE, 10, INSERT_UNIQUE};

typedef unsigned long long ull;



#endif /*LINKED_LIST_H*/