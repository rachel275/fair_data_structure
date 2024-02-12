#!/usr/bin/env bash

# usage: call when args not parsed, or when help needed
usage () {
    echo "usage: run-experiments.sh [-h] [-a] [-e experiment]"
    echo "  -h                help message"
    echo "  -a                run all experiments"
    echo "  -e n              run only experiment n"
    echo "  experiment 1      single my_hashtable"
    return 0
}

#go_my_hashtable: go to my_hashtable directory
go_my_hashtable () {
  MY_HASH_DIR=./fair_data_structure
  echo $MY_HASH_DIR
  cd $MY_HASH_DIR
}

#build_my_hashtable: run Makefile to build main_hashtable
build_my_hashtable () {
  make clean
  make
}

go_my_hashtable
build_my_hashtable
# if [ -d "./data/futex_hashtable_example" ]; then
#  echo "futex_hashtable_example directory already exists, please remove it first"
#  exit 1
# fi


for i in 1 2 4
do
  for f in 1 2 4
  do
    for t in 10 30 60
    do
       echo "./list_main -t$t -i$i -f$f > ./data/default_list/ithreads${i}_fthreads${f}_duration${t}_CLOUBLAB"
       ./list_main -t$t -i$i -f$f > ./data/default_list/ithreads${i}_fthreads${f}_duration${t}_CLOUDLAB
       echo "./ns_c_list_main -t$t -i$i -f$f > ./data/ns_c_list/ithreads${i}_fthreads${f}_duration${t}_CLOUDLAB"
       ./ns_c_list_main -t$t -i$i -f$f > ./data/ns_c_list/ithreads${i}_fthreads${f}_duration${t}_CLOUDLAB  
    done
  done
done
