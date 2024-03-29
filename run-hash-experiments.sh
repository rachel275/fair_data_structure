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


for b in 4 7
do
  for d in 2 4 8 10
  do
    	#echo "./hash_fair_main $a $b $d 64 > ./data/default_fair_hash/bucket_${a}_applications${b}_ratio{c}_duration64"
    	#./hash_fair_main $b 2 $d $a 64 > ./data/default_fair_hash/buckets_${b}_applications_2_ratio_{$d}_{$a}_duration_64
        echo "./hash_fair_main $a $b $d 64 > ./data/default_fair_hash/bucket_${a}_applications${b}_ratio{c}_duration64"
        ./ns_c_hash_fair_main $b 4 25 25 25 25 64 > ./data/ns_c_lock_fair_hash/buckets_${b}_applications_4_ratio_25_25_25_25_duration_64
        ./ns_c_hash_fair_main $b 4 25 25 25 100 64 > ./data/ns_c_lock_fair_hash/buckets_${b}_applications_4_ratio_25_25_25_100_duration_64
        ./ns_c_hash_fair_main $b 4 25 25 100 100 64 > ./data/ns_c_lock_fair_hash/buckets_${b}_applications_4_ratio_25_25_100_100_duration_64
        ./ns_c_hash_fair_main $b 4 25 100 100 100 64 > ./data/ns_c_lock_fair_hash/buckets_${b}_applications_4_ratio_25_100_100_100_duration_64

	echo "./hash_fair_main $a $b $d 64 > ./data/default_fair_hash/bucket_${a}_applications${b}_ratio{c}_duration64"
        ./ns_c_hash_fair_main $b 8 25 25 25 25 25 25 25 25 64 > ./data/ns_c_lock_fair_hash/buckets_${b}_applications_8_ratio_25_25_25_25_25_25_25_25_duration_64
        ./ns_c_hash_fair_main $b 8 25 25 25 25 25 25 25 100 64 > ./data/ns_c_lock_fair_hash/buckets_${b}_applications_8_ratio_25_25_25_25_25_25_25_100_duration_64
        ./ns_c_hash_fair_main $b 8 25 25 25 25 25 25 100 100 64 > ./data/ns_c_lock_fair_hash/buckets_${b}_applications_8_ratio_25_25_25_25_25_25_100_100_duration_64
        ./ns_c_hash_fair_main $b 8 25 25 25 25 25 100 100 100 64 > ./data/ns_c_lock_fair_hash/buckets_${b}_applications_8_ratio_25_25_25_25_25_100_100_100_duration_64
        echo "./hash_fair_main $a $b $d 64 > ./data/default_fair_hash/bucket_${a}_applications${b}_ratio{c}_duration64"
        ./ns_c_hash_fair_main $b 8 25 25 25 25 100 100 100 100 64 > ./data/ns_c_lock_fair_hash/buckets_${b}_applications_8_ratio_25_25_25_25_100_100_100_100_duration_64
        ./ns_c_hash_fair_main $b 8 25 25 25 100 100 100 100 100 64 > ./data/ns_c_lock_fair_hash/buckets_${b}_applications_8_ratio_25_25_25_100_100_100_100_100_duration_64
        ./ns_c_hash_fair_main $b 8 25 25 100 100 100 100 100 100 64 > ./data/ns_c_lock_fair_hash/buckets_${b}_applications_8_ratio_25_25_100_100_100_100_100_100_duration_64
        ./ns_c_hash_fair_main $b 8 25 100 100 100 100 100 100 100 64 > ./data/ns_c_lock_fair_hash/buckets_${b}_applications_8_ratio_25_100_100_100_100_100_100_100_duration_64

	echo "./hash_fair_main $a $b $d 64 > ./data/default_fair_hash/bucket_${a}_applications${b}_ratio{c}_duration64"
        ./ns_c_hash_fair_main $b 10 25 25 25 25 25 25 25 25 25 25 64 > ./data/ns_c_lock_fair_hash/buckets_${b}_applications_10_ratio_25_25_25_25_25_25_25_25_25_25_duration_64
        ./ns_c_hash_fair_main $b 10 25 25 25 25 25 25 25 25 25 100 64 > ./data/ns_c_lock_fair_hash/buckets_${b}_applications_10_ratio_25_25_25_25_25_25_25_25_25_100_duration_64
        ./ns_c_hash_fair_main $b 10 25 25 25 25 25 25 25 25 100 100 64 > ./data/ns_c_lock_fair_hash/buckets_${b}_applications_10_ratio_25_25_25_25_25_25_25_25_100_100_duration_64
        ./ns_c_hash_fair_main $b 10 25 25 25 25 25 25 25 100 100 100 64 > ./data/ns_c_lock_fair_hash/buckets_${b}_applications_10_ratio_25_25_25_25_25_25_25_100_100_100_duration_64
        echo "./hash_fair_main $a $b $d 64 > ./data/default_fair_hash/bucket_${a}_applications${b}_ratio{c}_duration64"
        ./ns_c_hash_fair_main $b 10 25 25 25 25 25 25 100 100 100 100 64 > ./data/ns_c_lock_fair_hash/buckets_${b}_applications_10_ratio_25_25_25_25_25_25_100_100_100_100_duration_64
        ./ns_c_hash_fair_main $b 10 25 25 25 25 25 100 100 100 100 100 64 > ./data/ns_c_lock_fair_hash/buckets_${b}_applications_10_ratio_25_25_25_25_25_100_100_100_100_100_duration_64
        ./ns_c_hash_fair_main $b 10 25 25 25 25 100 100 100 100 100 100 64 > ./data/ns_c_lock_fair_hash/buckets_${b}_applications_10_ratio_25_25_25_25_100_100_100_100_100_100_duration_64
        ./ns_c_hash_fair_main $b 10 25 25 25 100 100 100 100 100 100 100 64 > ./data/ns_c_lock_fair_hash/buckets_${b}_applications_10_ratio_25_25_25_100_100_100_100_100_100_100_duration_64
        ./ns_c_hash_fair_main $b 10 25 25 100 100 100 100 100 100 100 100 64 > ./data/ns_c_lock_fair_hash/buckets_${b}_applications_10_ratio_25_25_100_100_100_100_100_100_100_100_duration_64
        ./ns_c_hash_fair_main $b 10 25 100 100 100 100 100 100 100 100 100 64 > ./data/ns_c_lock_fair_hash/buckets_${b}_applications_10_ratio_25_100_100_100_100_100_100_100_100_100_duration_64


    	#echo "./hash_fair_main $a $b $d 64 > ./data/default_fair_hash/bucket_${a}_applications${b}_ratio{c}_duration64"
    	#./hash_spin_main $b 2 $d $a 64 > ./data/default_spin_hash/buckets${b}_applications2_ratio{$d}_{$a}_duration64
    	#echo "./hash_fair_main $a $b $d 64 > ./data/default_fair_hash/bucket_${a}_applications${b}_ratio{c}_duration64"
    	#./hash_fair_main $b 4 $d $a 100 25 64 > ./data/default_fair_hash/buckets${b}_applications4_ratio{$d}_{$a}_100_25_duration64
    	#./hash_spin_main $b 4 $d $a 100 25 64 > ./data/default_spin_hash/buckets${b}_applications4_ratio{$d}_{$a}_100_25_duration64
  
    done
  done
done
