import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D, HandlerTuple
import numpy as np
import os
import csv
import sys


for n_apps in [2]:
    for ratio_a in [0, 25, 50, 75, 100]:
        for ratio_b in [0, 25, 50, 75, 100]:
            n_count = 0
            #fig, ax = plt.subplots()
            rootdir = "./tables/"
            fair_no_threads = []
            fair_thread_type = []
            fari_genuine_id = []
            fair_insert_id = []
            fair_wc_time = []
            i_fair_wc_time = []
            fairtot_time = []
            fair_i_tot_time = []
            fair_n_ops = []
            fair_i_n_ops = []
            fair_lock_opp = []
            fair_i_lock_opp = []
            new_fair_insert_id = []
            new_find_id = []
            new_fair_i_lock_opp = []
            new_fair_f_find_opp = []
            n_count_sum = []
            n_i_count_sum = []
            for dir in os.listdir(rootdir):
                    if dir.split('_')[-2] == "list":
                        type = dir.split('_list')[0]
                        for filename in os.listdir("./tables/" + dir):
                            with open(os.path.join("./tables/" + dir, filename), 'r') as file:
                                if (("default" in dir)):# or (filename.endswith("_basecase_CLOUDLAB.csv") == True )):
                                    applications = int(filename.split('_')[1]) 
                                    ratio = []
                                    for i in range(applications):
                                        ratio.append(int(filename.split('_')[i + 3]))
                                    duration = filename.split('_')[i + 5].split('.csv')[0]
                                    if(int(applications) == 2 and int(ratio[0]) == ratio_a and int(ratio[1]) == ratio_b and int(duration) == 64):
                                        print(filename)
                                        n_count = n_count + 1
                                        i = -1
                                        reader = csv.reader(file)
                                        for row in reader:
                                            if i == -1:
                                                i = 1
                                            else:
                                                #need to ignore the first line!
                                                fair_thread_type.append(row[int(0)])
                                                if (row[int(0)] == "insert"):
                                                    fair_insert_id.append(int(row[int(1)]))
                                                    i_fair_wc_time.append(float(row[int(3)]))
                                                    fair_i_tot_time.append(float(row[int(4)]))
                                                    fair_i_n_ops.append(int(row[int(2)]))  
                                                    fair_i_lock_opp.append(float(row[int(5)]))
                                                    n_i_count_sum.append(n_count + ((1/2) * int(row[int(1)])))

                                                else:
                                                    fari_genuine_id.append(int(row[int(1)]))
                                                    fair_wc_time.append(float(row[int(3)]))
                                                    fairtot_time.append(float(row[int(4)]))
                                                    fair_n_ops.append(int(row[int(2)]))
                                                    fair_lock_opp.append(float(row[int(5)]))
                                                    n_count_sum.append(n_count + ((1/2) * int(row[int(1)])))
                                        n_count = n_count + 1
                                    
            counter_one = 0
            counter_two = 0
            counter_three = 0
            counter_four = 0
            counter_five = 0

            for i in n_i_count_sum:
                if i == 1:
                    if counter_one == 0:
                        new_fair_insert_id.append((i*2 - (counter_one + 0.1) + n_count))
                        counter_one = counter_one + 0.1
                    else:
                        new_fair_insert_id.append((i*2 - (counter_one + 0.1)) + n_count)
                        counter_one = counter_one + 0.1
                elif i == 1.5:
                    if counter_two == 0:
                        new_fair_insert_id.append((i*2 - (counter_two + 0.1)) + n_count)
                        counter_two = counter_two + 0.1
                    else:
                        new_fair_insert_id.append((i*2 - (counter_two + 0.1)) + n_count)
                        counter_two = counter_two + 0.1
                elif i == 3:
                    if counter_three == 0:
                        new_fair_insert_id.append((i*2 - (counter_three + 0.1)) + n_count)
                        counter_three = counter_three + 0.1
                    else:
                        new_fair_insert_id.append((i*2 - (counter_three + 0.1)) + n_count)
                        counter_three = counter_three + 0.1
                elif i == 3.5:
                    if counter_four == 0:
                        new_fair_insert_id.append((i*2 - (counter_four + 0.1)) + n_count)
                        counter_four = counter_four + 0.1
                    else:
                        new_fair_insert_id.append((i*2 - (counter_four + 0.1)) + n_count)
                        counter_four = counter_four + 0.1
                elif i == 4:
                    if counter_five == 0:
                        new_fair_insert_id.append((i*2 - (counter_five + 0.05)) + n_count)
                        counter_five = counter_five + 0.05
                    else:
                        new_fair_insert_id.append((i*2 - (counter_five + 0.1)) + n_count)
                        counter_five = counter_five + 0.1

            count_one = 0
            count_two = 0
            count_three = 0
            count_four = 0
            count_five = 0

            for i in n_count_sum:
                if i == 1:
                    if count_one == 0:
                        new_find_id.append((i*2 + (count_one + 0.1)) + n_count)
                        count_one = count_one + 0.1
                    else:
                        new_find_id.append((i*2 + (count_one + 0.1)) + n_count)
                        count_one = count_one + 0.1
                elif i == 1.5:
                    if count_two == 0:
                        new_find_id.append((i*2 + (count_two + 0.1)) + n_count)
                        count_two = count_two + 0.1
                    else:
                        new_find_id.append((i*2 + (count_two + 0.1)) + n_count)
                        count_two = count_two + 0.1
                elif i == 3:
                    if count_three == 0:
                        new_find_id.append((i*2 + (count_three + 0.1)) + n_count)
                        count_three = count_three + 0.1
                    else:
                        new_find_id.append((i*2 + (count_three + 0.1)) + n_count)
                        count_three = count_three + 0.1
                elif i == 3.5:
                    if count_four == 0:
                        new_find_id.append((i*2 + (count_four + 0.1)) + n_count)
                        count_four = count_four + 0.1
                    else:
                        new_find_id.append((i*2 + (count_four + 0.1)) + n_count)
                        count_four = count_four + 0.1
                elif i == 4:
                    if count_five == 0:
                        new_find_id.append((i*2 + (count_five + 0.05)) + n_count)
                        count_five = count_five + 0.05
                    else:
                        new_find_id.append((i*2 + (count_five + 0.1)) + n_count)
                        count_five = count_five + 0.1
            
            #print(new_find_id)

            print(n_i_count_sum)
            print(new_fair_insert_id)
            print(n_count_sum)
            print(new_find_id)
            print(fair_lock_opp)
            plt.bar(new_fair_insert_id, fair_i_lock_opp, align='center', width=0.09, color='r', alpha=0.25)#, label = "insert")
            plt.bar(new_find_id, fair_lock_opp,  width=0.09, color='r', align='center', alpha=0.25, label = "lock opportunity")
            plt.bar(new_find_id, fairtot_time, width=0.09, color='b', align='center', label = "find")
            plt.bar(new_fair_insert_id, fair_i_tot_time, width=0.09, color='g', align='center', label = "insert")
                    #handles, labels = plt.set_legend_handles_labels()

            plt.xlabel("Experiment Types") 
            plt.ylabel("Time (ms)") 
            plt.yscale("log") 
            x = np.arange(5,12,1)
            x_ticks_labels = [ '', '','Spin lock','','Fair lock', '', '']
            plt.xticks(ticks=x, labels=x_ticks_labels)
            plt.legend()
            #plt.plot(genuine_id, wc_time)
            n = len(filename)
            plt.title("Total lock hold per thread") 
            ratio_string = ""
            for i in ratio:
                ratio_string = ratio_string + str(i) + "_"
            figName = "./graphs/default_spin_list_graphs/applications" + str(applications) + "_ratio_" + str(ratio_a) + "_" + str(ratio_b) + "_duration_" + str(duration) + "_combined.png"
            plt.savefig(figName)          
            plt.close()