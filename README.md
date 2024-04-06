# fair_data_structure
Fair data structure project code and files.


The Makefile will in it's current state create linked lists and hash table objects:

list_spin_main : our default linked list with a spin lock object file
list_fair_main : our default linked list with a fair lock object file
ns_c_list_fair_main : our non-shared correct solution linked list with a fair lock
ns_c_list_lock_fair_main: our non-shared correct solution linked list with internal fair locks

hash_fair_main : our default hash table with fair locks
ns_c_hash_fair_main : our non-shared correct solution hashtable with a fair lock
ns_c_hash_lock_fair_main: our non-shared correct solution hashtable with internal fair locks

To run the linked list experiments you can use the following:
make
./list_fair_main <no applications> <insert ratio application 1> <insert ration application 2> ..... <duration>

To run the hash table experiments:
make
./hash_fair_main <no buckets> <no applications> <insert ratio application 1> <insert ration application 2> ..... <duration>

To run the dynamic performance experiments we altered the original linked list code so you can run:
make
./dynamic_list_main 1 1 1 
(./dynamic_ns_c_list_main 1 1 1)
(./dynamic_ns_c_lock_list_main 1 1 1)

The tables and graphs contained in the folders we generated from the python files. These have been edited to produce the different files so some may not be able to currently reproduce the graphs and tables. 
