#Use machine's CPU-SPEED, else results will be wrong.
#example CYCLE_PER_US=2400L - 2.4 GHz processor
#laptop CYCLE_PER_US=1800L - 1.8 GHz processor

#CYCLE_PER_US=2400L
CYCLE_PER_US=3300L
ifndef CYCLE_PER_US
$(error CYCLE_PER_US not set. Set CYCLE_PER_US according to your machine CPU-SPEED)
endif

CC = gcc
GCCVERSIONGTEQ5 := $(shell expr `gcc -dumpversion | cut -f1 -d.` \>= 5)

# u-SCL is not tested with -O3 flag for gcc version above 5 yet.
ifeq "$(GCCVERSIONGTEQ5)" "1"
    OFLAG=-O2
else
    OFLAG=-O3
endif

FLAGS=-I../ -g -lpthread -Wall -lurcu ${OFLAG} -DCYCLE_PER_US=${CYCLE_PER_US}

# fairlock:
# 	gcc main.c -o main ${FLAGS} -DFAIRLOCK

mutex:
	#gcc main_hashtable.c -o hash_spin_main ${FLAGS} -DSPIN
	gcc main_hashtable.c -o hash_fair_main ${FLAGS} -DFAIRLOCK -DDEBUG
	gcc main_hashtable.c -o ns_c_hash_fair_main ${FLAGS} -DFAIRLOCK -DDEBUG -DNSCLOCK	
	gcc linked_list_main.c -o list_fair_main ${FLAGS} -DFAIRLOCK -DDEBUG
	gcc linked_list_main.c -o list_spiin_main ${FLAGS} -DSPIN 
	gcc linked_list_main.c -o ns_c_list_spin_main ${FLAGS} -DSPIN -DNSC
	gcc linked_list_main.c -o ns_c_list_fair_main ${FLAGS} -DFAIRLOCK -DNSC -DDEBUG
	gcc linked_list_main.c -o ns_c_list_lock_spin_main ${FLAGS} -DSPIN -DNSCLOCK
	gcc linked_list_main.c -o ns_c_list_lock_fair_main ${FLAGS} -DFAIRLOCK -DNSCLOCK -DDEBUG 
# spin:
# 	gcc main.c -o main ${FLAGS} -DSPIN

clean:
	rm list_spin_main
	rm ns_c_list_spin_main
	rm ns_c_list_lock_spin_main
	rm list_fair_main
	rm ns_c_list_fair_main
	rm ns_c_list_lock_fair_main

