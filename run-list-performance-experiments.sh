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

echo "./list_fair_main 4 25 25 25 64 > ./data/default_fair_list/applications_4_ratio_25_25_25_25_duration_64"
./ns_c_list_fair_main 4 25 25 25 25 64 > ./data/ns_c_fair_list/app_4_ratio_25_25_25_25_duration_64
echo "./list_fair_main 4 25 25 100 64 > ./data/default_fair_list/applications_4_ratio_25_25_25_100_duration_64"
./ns_c_list_fair_main 4 25 25 25 100 64 > ./data/ns_c_fair_list/app_4_ratio_25_25_25_100_duration_64
echo "./list_fair_main 4 25 100 100 64 > ./data/default_fair_list/applications_4_ratio_25_25_25_25_duration_64"
./ns_c_list_fair_main 4 25 100 100 100 64 > ./data/ns_c_fair_list/app_4_ratio_25_100_100_100_duration_64
echo "./list_fair_main 4 25 25 25 64 > ./data/default_fair_list/applications_4_ratio_25_25_25_25_duration_64"
./ns_c_list_fair_main 4 25 25 100 100 64 > ./data/ns_c_fair_list/app_4_ratio_25_25_100_100_duration_64
echo "./list_fair_main 8 25 25 25 64 > ./data/default_fair_list/applications_8_ratio_25_25_25_25_duration_64"
./ns_c_list_fair_main 8 25 25 25 25 25 25 25 25 64 > ./data/ns_c_fair_list/app_8_ratio_25_25_25_25_25_25_25_25_duration_64
echo "./list_fair_main 8 25 25 25 64 > ./data/default_fair_list/applications_8_ratio_25_25_25_25_duration_64"
./ns_c_list_fair_main 8 25 25 25 25 25 25 25 100 64 > ./data/ns_c_fair_list/app_8_ratio_25_25_25_25_25_25_25_100_duration_64
echo "./list_fair_main 8 25 25 25 64 > ./data/default_fair_list/applications_8_ratio_25_25_25_25_duration_64"
./ns_c_list_fair_main 8 25 25 25 25 25 25 100 100 64 > ./data/ns_c_fair_list/app_8_ratio_25_25_25_25_25_25_100_100_duration_64
echo "./list_fair_main 8 25 25 25 64 > ./data/default_fair_list/applications_8_ratio_25_25_25_25_duration_64"
./ns_c_list_fair_main 8 25 25 25 25 25 100 100 100 64 > ./data/ns_c_fair_list/app_8_ratio_25_25_25_25_25_100_100_100_duration_64
echo "./list_fair_main 8 25 25 25 64 > ./data/default_fair_list/applications_8_ratio_25_25_25_25_duration_64"
./ns_c_list_fair_main 8 25 25 25 25 100 100 100 100 64 > ./data/ns_c_fair_list/app_8_ratio_25_25_25_25_100_100_100_100_duration_64
echo "./list_fair_main 8 25 25 25 64 > ./data/default_fair_list/applications_8_ratio_25_25_25_25_duration_64"
./ns_c_list_fair_main 8 25 25 25 100 100 100 100 100 64 > ./data/ns_c_fair_list/app_8_ratio_25_25_25_100_100_100_100_100_duration_64
echo "./list_fair_main 8 25 25 25 64 > ./data/default_fair_list/applications_8_ratio_25_25_25_25_duration_64"
./ns_c_list_fair_main 8 25 25 100 100 100 100 100 100 64 > ./data/ns_c_fair_list/app_8_ratio_25_25_100_100_100_100_100_100_duration_64
echo "./list_fair_main 8 25 25 25 64 > ./data/default_fair_list/applications_8_ratio_25_25_25_25_duration_64"
./ns_C_list_fair_main 8 25 100 100 100 100 100 100 100 64 > ./data/ns_c_fair_list/app_8_ratio_25_100_100_100_100_100_100_100_duration_64

echo "./list_fair_main 10 25 25 25 64 > ./data/default_fair_list/applications_8_ratio_25_25_25_25_duration_64"
./ns_c_list_fair_main 10 25 25 25 25 25 25 25 25 25 25 64 > ./data/ns_c_fair_list/app_10_ratio_25_25_25_25_25_25_25_25_25_25_duration_64
echo "./list_fair_main 8 25 25 25 64 > ./data/default_fair_list/applications_8_ratio_25_25_25_25_duration_64"
./ns_c_list_fair_main 10 25 25 25 25 25 25 25 25 25 100 64 > ./data/ns_c_fair_list/app_10_ratio_25_25_25_25_25_25_25_25_25_100_duration_64
echo "./list_fair_main 8 25 25 25 64 > ./data/default_fair_list/applications_8_ratio_25_25_25_25_duration_64"
./ns_c_list_fair_main 10 25 25  25 25 25 25 25 25 100 100 64 > ./data/ns_c_fair_list/app_10_ratio25_25_25_25_25_25_25_25_100_100_duration_64
echo "./list_fair_main 8 25 25 25 64 > ./data/default_fair_list/applications_8_ratio_25_25_25_25_duration_64"
./ns_c_list_fair_main 10 25 25 25 25 25 25 25 100 100 100 64 > ./data/ns_c_fair_list/app_10_ratio_25_25_25_25_25_25_25_100_100_100_duration_64
echo "./list_fair_main 10 25 25 25 64 > ./data/default_fair_list/applications_8_ratio_25_25_25_25_duration_64"
./ns_c_list_fair_main 10 25 25 25 25 25 25 100 100 100 100 64 > ./data/ns_c_fair_list/app_10_ratio_25_25_25_25_25_25_100_100_100_100_duration_64
echo "./list_fair_main 8 25 25 25 64 > ./data/default_fair_list/applications_8_ratio_25_25_25_25_duration_64"
./ns_c_list_fair_main 10 25 25 25 25 25 100 100 100 100 100 64 > ./data/ns_c_fair_list/app_10_ratio_25_25_25_25_25_100_100_100_100_100_duration_64
echo "./list_fair_main 8 25 25 25 64 > ./data/default_fair_list/applications_8_ratio_25_25_25_25_duration_64"
./ns_c_list_fair_main 10 25 25 25 25 100 100 100 100 100 100 64 > ./data/ns_c_fair_list/app_10_ratio_25_25_25_25_100_100_100_100_100_100_duration_64
echo "./list_fair_main 8 25 25 25 64 > ./data/default_fair_list/applications_8_ratio_25_25_25_25_duration_64"
./ns_c_list_fair_main 10 25 25 25 100 100 100 100 100 100 100 64 > ./data/ns_c_fair_list/app_10_ratio_25_25_25_100_100_100_100_100_100_100_duration_64
echo "./list_fair_main 8 25 25 25 64 > ./data/default_fair_list/applications_8_ratio_25_25_25_25_duration_64"
./ns_c_list_fair_main 10 25 25 100 100 100 100 100 100 100 100 64 > ./data/ns_c_fair_list/app_10_ratio_25_25_100_100_100_100_100_100_100_100_duration_64
echo "./list_fair_main 8 25 25 25 64 > ./data/default_fair_list/applications_8_ratio_25_25_25_25_duration_64"
./ns_c_list_fair_main 10 25 100 100 100 100 100 100 100 100 100 64 > ./data/ns_c_fair_list/app_10_ratio_25_100_100_100_100_100_100_100_100_100_duration_64
