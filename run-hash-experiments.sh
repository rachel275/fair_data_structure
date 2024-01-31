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


for a in 4 16 64
do
  for d in 30
  do
    for t in 4 8
    do
      b=1
      g=1
      echo "./hash_main $a $b $d $t $g > ./data/futex_hashtable_example/bucket_nfutex${a}_ninsert${b}_duration${d}_buckets${t}_ncpu${g}"
      ./hash_main $a $b $d $t $g > ./data/futex_hashtable_example/bucket_nfutex${a}_ninsert${b}_duration${d}_buckets${t}_ncpu${g}
    done
  done
done
