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


for e in 64
do
  for f in 75 100
  do
    for t in 0 25 50 75 100
    do
     # echo "./list_spin_main 1 $f 60 > ./data/default_spin_list/applications_1_ratio${f}_duration_60_no_mal"
     # ./list_spin_main 1 $f 60 > ./data/default_spin_list/app_1_ratio_${f}_duration_60_no_mal
     # echo "./list_fair_main 1 $f 60 > ./data/default_fair_list/applications_1_ratio${f}_duration_60_exp_${e}"
     # ./list_fair_main 1 $f 60 > ./data/default_fair_list/app_1_ratio_${f}_duration_60_no_mal
      #echo "./list_spin_main 2 $f $t $e > ./data/default_spin_list/applications_2_ratio${f}_${t}_duration_${e}"
      #./list_spin_main 2 $f $t $e > ./data/default_spin_list/app_2_ratio_${f}_${t}_duration_${e}
      #echo "./list_fair_main 2 $f $t $e > ./data/default_fair_list/applications_2_ratio${f}_${t}_duration_${e}"
      #./list_fair_main 2 $f $t $e > ./data/default_fair_list/app_2_ratio_${f}_${t}_duration_${e}
      #echo "./list_spin_main 3 $f $f $t 60 > ./data/default_spin_list/applications_3_ratio_${f}_${f}_${t}_duration_60_exp_${e}"
      #./list_spin_main 3 $f $f $t 60 > ./data/default_spin_list/app_3_ratio_${f}_${f}_${t}_duration_60_exp_${e}
      #echo "./list_fair_main 3 $f $f $t 60 > ./data/default_fair_list/applications_3_ratio_${f}_${f}_${t}_duration_60_exp_${e}"
      #./list_fair_main 3 $f $f $t 60 > ./data/default_fair_list/app_3_ratio_${f}_${f}_${t}_duration_60_exp_${e}
      #echo "./list_spin_main 4 $f $f $f $t $e > ./data/default_spin_list/applications_4_ratio_${f}_${f}_${f}_${t}_duration_${e}"
      #./list_spin_main 4 $t $f $f $f $e > ./data/default_spin_list/app_4_ratio_${f}_${f}_${f}_${t}_duration_${e}
      #echo "./list_fair_main 4 $f $f $f $t $e > ./data/default_fair_list/applications_4_ratio_${f}_${f}_${f}_${t}_duration_${e}"
      #./list_fair_main 4 $t $f $f $f $e > ./data/default_fair_list/app_4_ratio_${f}_${f}_${f}_${t}_duration_${e}

      #echo "./ns_c_list_spin_main 1 $f 64 > ./data/ns_c_spin_list/applications_1_ratio${f}_duration_64"
      #./ns_c_list_spin_main 1 $f 64 > ./data/ns_c_spin_list/app_1_ratio_${f}_duration_64
      #echo "./ns_c_list_fair_main 1 $f 64 > ./data/ns_c_fair_list/applications_1_ratio${f}_duration_64"
      #./ns_c_list_fair_main 1 $f 64 > ./data/ns_c_fair_list/app_1_ratio_${f}_duration_64
      #echo "./ns_c_list_spin_main 2 $f $t $e > ./data/ns_c_spin_list/applications_2_ratio_${f}_${t}_duration_${e}"
      #./ns_c_list_spin_main 2 $f $t $e > ./data/ns_c_spin_list/app_2_ratio_${f}_${t}_duration_${e}
      #echo "./ns_c_list_fair_main 2 $f $t $e > ./data/ns_c_fair_list/applications_2_ratio${f}_${t}_duration_${e}"
      #./ns_c_list_fair_main 2 $f $t $e > ./data/ns_c_fair_list/app_2_ratio_${f}_${t}_duration_${e}
      #echo "./ns_c_list_spin_main 3 $f $f $t 60 > ./data/ns_c_spin_list/applications_3_ratio_${f}_${f}_${t}_duration_60_exp_${e}"
      #./ns_c_list_spin_main 3 $f $f $t 60 > ./data/ns_c_spin_list/app_3_ratio_${f}_${f}_${t}_duration_60_exp_${e}
      #echo "./ns_c_list_fair_main 3 $f $f $t 60 > ./data/ns_c_fair_list/applications_3_ratio_${f}_${f}_${t}_duration_60_exp_${e}"
      #./ns_c_list_fair_main 3 $f $f $t 60 > ./data/ns_c_fair_list/app_3_ratio_${f}_${f}_${t}_duration_60_exp_${e}
      #echo "./ns_c_list_spin_main 4 $f $f $f $t 60 > ./data/ns_c_spin_list/applications_4_ratio_${f}_${f}_${f}_${t}_duration_60_exp_${e}"
      #./ns_c_list_spin_main 4 $t $f $f $f $e > ./data/ns_c_spin_list/app_4_ratio_${f}_${f}_${f}_${t}_duration_${e}
      #echo "./ns_c_fair_main 4 $f $f $f $t 60 > ./data/ns_c_fair_list/applications_4_ratio_${f}_${f}_${f}_${t}_duration_60_exp_${e}"
      #./ns_c_list_fair_main 4 $t $f $f $f $e > ./data/ns_c_fair_list/app_4_ratio_${f}_${f}_${f}_${t}_duration_${e}

      echo "./ns_c_list_lock_spin_main 1 $f 64 > ./data/ns_c_spin_lock_list/applications_1_ratio${f}_duration_64"
      ./ns_c_list_lock_fair_main 1 $f 64 > ./data/ns_c_lock_fair_list/app_1_ratio_${f}_duration_64
      #echo "./ns_c_list_lock_fair_main 1 $f 64 > ./data/ns_c_lock_fair_list/applications_1_ratio${f}_duration_60"
      #./ns_c_list_lock_fair_main 1 $f 64 > ./data/ns_c_lock_fair_list/app_1_ratio_${f}_duration_64
      #echo "./ns_c_list_lock_spin_main 2 $f $t $e > ./data/ns_c_lock_spin_list/applications_2_ratio${f}_${t}_duration_${e}"
      #./ns_c_list_lock_spin_main 2 $f $t $e > ./data/ns_c_lock_spin_list/app_2_ratio_${f}_${t}_duration_${e}
      echo "./ns_c_list_lock_fair_main 2 $f $t $e > ./data/ns_c_lock_fair_list/applications_2_ratio${f}_${t}_duration_${e}"
      ./ns_c_list_lock_fair_main 2 $f $t $e > ./data/ns_c_lock_fair_list/app_2_ratio_${f}_${t}_duration_${e}
      #echo "./ns_c_list_lock_spin_main 3 $f $f $t 60 > ./data/ns_c_lock_spin_list/applications_3_ratio_${f}_${f}_${t}_duration_60_exp_${e}"
      #./ns_c_list_lock_spin_main 3 $f $f $t 60 > ./data/ns_c_lock_spin_list/app_3_ratio_${f}_${f}_${t}_duration_60_exp_${e}
      #echo "./ns_c_list_lock_fair_main 3 $f $f $t 60 > ./data/ns_c_lock_fair_list/applications_3_ratio_${f}_${f}_${t}_duration_60_exp_${e}"
      #./ns_c_list_lock_fair_main 3 $f $f $t 60 > ./data/ns_c_lock_fair_list/app_3_ratio_${f}_${f}_${t}_duration_60_exp_${e}
      #  echo "./ns_c_list_lock_spin_main 4 $f $f $f $t 60 > ./data/ns_c_lock_spin_list/applications_4_ratio_${f}_${f}_${f}_${t}_duration_60_exp_${e}"
      #./ns_c_list_lock_spin_main 4 $f $f $f $t 60 > ./data/ns_c_lock_spin_list/app_4_ratio_${f}_${f}_${f}_${t}_duration_60_exp_${e}
      #echo "./ns_c_list_lock_fair_main 4 $f $f $f $t 60 > ./data/ns_c_lock_fair_list/applications_4_ratio_${f}_${f}_${f}_${t}_duration_60_exp_${e}"
      #./ns_c_list_lock_fair_main 4 $f $f $f $t 60 > ./data/ns_c_lock_fair_list/app_4_ratio_${f}_${f}_${f}_${t}_duration_60_exp_${e}
     # echo "./ns_c_list_lock_spin_main 4 $f $f $f $t 60 > ./data/ns_c_lock_spin_list/applications_4_ratio_${f}_${f}_${f}_${t}_duration_60_exp_${e}"
     # ./ns_c_list_lock_spin_main 4 $t $f $f $f $e > ./data/ns_c_lock_spin_list/app_4_ratio_${f}_${f}_${f}_${t}_duration_${e}
     # echo "./ns_c_lock_fair_main 4 $f $f $f $t 60 > ./data/ns_c_lock_fair_list/applications_4_ratio_${f}_${f}_${f}_${t}_duration_60_exp_${e}"
     # ./ns_c_list_lock_fair_main 4 $t $f $f $f $e > ./data/ns_c_lock_fair_list/app_4_ratio_${f}_${f}_${f}_${t}_duration_${e}


    done
  done
done
