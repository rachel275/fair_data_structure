# fair_data_structure
Fair data structure project code and files.
All linked lists results are run from linked_list_main.c apart from the dynamic workload. The results for our graphs and tables in the Motivation section we taken from experiments run with the default linked list with a spin lock and fair lock. For the evaluation, our solutions is contained within ns_c_linked_list.h. The solutions with internal locks added is in ns_c_lock_linked_list.h The files for the hash tables tests are run from hashtable_main.c. To run the dynamic workload we use the c file dynamic_linked_list_main.c.

The Makefile will in it's current state create the following linked lists and hash table objects:

list_spin_main : our default linked list with a spin lock object file              
list_fair_main : our default linked list with a fair lock object file                      
ns_c_list_fair_main : our non-shared correct solution linked list with a fair lock                                
ns_c_list_lock_fair_main: our non-shared correct solution linked list with internal fair locks                  

hash_fair_main : our default hash table with fair locks                      
ns_c_hash_fair_main : our non-shared correct solution hashtable with a fair lock                  
ns_c_hash_lock_fair_main: our non-shared correct solution hashtable with internal fair locks                  

dynamic_list_main : our default linked list with a fair lock object file running a dynamic workload                     
ns_c_dynamic_list_main : our non-shared correct solution linked list with a fair lock running a dynamic workload                                 
ns_c_lock_dynamic_list_main: our non-shared correct solution linked list with internal fair locks running a dynamic workload     

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



The tables and graphs contained in the folders we generated from the python files. These have been edited to produce the different graphs and tables so some may not be able to currently reproduce the graphs and tables that were made without changes needed.
