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


for n in 4 16 64
do
  for t in 30
  do
    for i in 1
    do
      for f in 1
      do
        for d in 1
        do
          m=1
          echo "./list_main -n$n -m$m -t$t -i$i -f$f -d$d > ./data/default_list/nthreads${n}_duration${t}_ratio${i},${f},${d}_DICE"
          ./list_main -n$n -m$m -t$t -i$i -f$f -d$d > ./data/default_list/nthreads${n}_duration${t}_ratio${i},${f},${d}_DICE
          echo "./ns_c_list_main -n$n -m$m -t$t -i$i -f$f -d$d > ./data/ns_c_list/nthreads${n}_duration${t}_ratio${i},${f},${d}_DICE"
          ./ns_c_list_main -n$n -m$m -t$t -i$i -f$f -d$d > ./data/ns_c_list/nthreads${n}_duration${t}_ratio${i},${f},${d}_DICE
        done
      done  
    done
  done
done
