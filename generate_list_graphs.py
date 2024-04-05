import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D, HandlerTuple
import numpy as np
import os
import csv
import sys



path = "./tables/ns_c_lock_fair_hash_tables/"  #FILL THIS IN HERE
fileCount = 0;
for filename in os.listdir(path):
    print(filename)
    with open(os.path.join(path, filename), 'r') as file:
        applications = int(filename.split('_')[1]) 
        ratio = []
        #print("reached here     ")
        for i in range(applications):
            ratio.append(int(filename.split('_')[i + 3]))
        if applications == 8:
            duration = filename.split('_')[i + 5]
            i = -1
            reader = csv.reader(file)
            no_threads = []
            thread_type = []
            genuine_id = []
            insert_id = []
            wc_time = []
            i_wc_time = []
            tot_time = []
            i_tot_time = []
            n_ops = []
            i_n_ops = []
            lock_opp = []
            i_lock_opp = []
            for row in reader:
                if i == -1:
                    i = 1
                else:
                    #need to ignore the first line!
                    thread_type.append(row[int(0)])
                    if (row[int(0)] == "insert"):
                        insert_id.append(int(row[int(1)]))
                        #i_wc_time.append(float(row[int(3)]))
                        i_tot_time.append(float(row[int(3)]))
                        i_n_ops.append(int(row[int(2)]))  
                        #i_lock_opp.append(float(row[int(5)]))
                        i_lock_opp.append(10715)
                    else:
                        genuine_id.append(int(row[int(1)]))
                        #wc_time.append(float(row[int(3)]))
                        tot_time.append(float(row[int(3)]))
                        n_ops.append(int(row[int(2)]))
                        #lock_opp.append(float(row[int(5)])) 
                        lock_opp.append(10715)


                counter_one = 0
                counter_two = 0
                counter_three = 0
                counter_four = 0
                counter_five = 0
                counter_six = 0
                counter_seven = 0
                counter_eight = 0
                new_insert_id = []
                new_find_id = []

                #new_i_lock_opp = []
                new_f_find_opp = []

                new_i_ops = []
                new_ops = []
                for i in insert_id:
                    if i == 0:
                        if counter_one == 0:
                            new_insert_id.append(i - (counter_one + 0.05))
                            counter_one = counter_one + 0.05
                        else:
                            new_insert_id.append(i - (counter_one + 0.1))
                            counter_one = counter_one + 0.1
                    elif i == 1:
                        if counter_two == 0:
                            new_insert_id.append(i - (counter_two + 0.05))
                            counter_two = counter_two + 0.05
                        else:
                            new_insert_id.append(i - (counter_two + 0.1))
                            counter_two = counter_two + 0.1
                    elif i == 2:
                        new_insert_id.append(i - (counter_three + 0.1))
                        counter_three = counter_three + 0.1
                    elif i == 3:
                        new_insert_id.append(i - (counter_four + 0.1))
                        counter_four = counter_four + 0.1
                    elif i == 4:
                        if counter_five == 0:
                            new_insert_id.append(i - (counter_five + 0.05))
                            counter_five= counter_five + 0.05
                        else:
                            new_insert_id.append(i - (counter_five + 0.1))
                            counter_five = counter_five + 0.1
                    elif i == 5:
                        if counter_six == 0:
                            new_insert_id.append(i - (counter_six+ 0.05))
                            counter_six = counter_six + 0.05
                        else:
                            new_insert_id.append(i - (counter_six + 0.1))
                            counter_six = counter_six + 0.1
                    elif i == 6:
                        new_insert_id.append(i - (counter_seven + 0.1))
                        counter_seven = counter_seven + 0.1
                    elif i == 7:
                        new_insert_id.append(i - (counter_eight+ 0.1))
                        counter_eight= counter_eight + 0.1

                count_one = 0
                count_two = 0
                count_three = 0
                count_four = 0
                count_five = 0
                count_six = 0
                count_seven = 0
                count_eight = 0

                for i in genuine_id:
                    if i == 0:
                        if count_one == 0:
                            new_find_id.append(i + (count_one + 0.05))
                            count_one = count_one + 0.05
                        else:
                            new_find_id.append(i + (count_one + 0.1))
                            count_one = count_one + 0.1
                    elif i == 1:
                        if count_two == 0:
                            new_find_id.append(i + (count_two + 0.05))
                            count_two = count_two + 0.05
                        else:
                            new_find_id.append(i + (count_two + 0.1))
                            count_two = count_two + 0.1
                    elif i == 2:
                        new_find_id.append(i + (count_three + 0.1))
                        count_three = count_three + 0.1
                    elif i == 3:
                        new_find_id.append(i + (count_four + 0.1))
                        count_four = count_four + 0.1
                    elif i == 4:
                        if count_one == 0:
                            new_find_id.append(i + (count_five + 0.05))
                            count_five = count_five + 0.05
                        else:
                            new_find_id.append(i + (count_five + 0.1))
                            count_five = count_five + 0.1
                    elif i == 5:
                        if count_two == 0:
                            new_find_id.append(i + (count_six + 0.05))
                            count_six = count_six + 0.05
                        else:
                            new_find_id.append(i + (count_six + 0.1))
                            count_six= count_six+ 0.1
                    elif i == 6:
                        new_find_id.append(i + (count_seven + 0.1))
                        count_seven = count_seven + 0.1
                    elif i == 7:
                        new_find_id.append(i + (count_eight + 0.1))
                        count_eight = count_eight + 0.1


                fig, ax = plt.subplots(figsize=(14,6))

                #twin1 = ax.twinx()
                #twin2 = ax.twinx()

                #print("reached here     ")
                #ax.bar([0, 1], [0, 0], label = "applications")

                # twin1.scatter(new_insert_id, i_n_ops, marker='.', color='w', label="number of operations")
                # twin1.scatter(new_find_id, n_ops, marker='.', color='w')
                ax.set(ylim=[1, 10**13], yscale='log', yticks=[])
                ax.set_ylabel("Throughput", rotation=-90, labelpad=15)
                #[plt.text(i, 200000000, f'{int(j  / 1000)}K', rotation=45, fontsize=15) for (i, j) in zip(new_find_id, n_ops)]
                for (i, j) in zip(new_find_id, n_ops):
                    if (j > 1000000):
                        ax.text(i, max(lock_opp) + 10000, f'{round(float(j  / 1000000), 1)}M', rotation=80, fontsize=13)
                    else:
                        ax.text(i, max(lock_opp) + 10000, f'{round(float(j  / 1000), 1)}K', rotation=80, fontsize=13)
                for (i, j) in zip(new_insert_id, i_n_ops):
                    if (j > 1000000):
                        ax.text(i, max(i_lock_opp) + 10000, f'{round(float(j  / 1000000), 1)}M', rotation=80, fontsize=13)
                    else:
                        ax.text(i, max(i_lock_opp) + 10000, f'{round(float(j  / 1000), 1)}K', rotation=80, fontsize=13)
                #[plt.text(i, 200000000, f'{int(j / 1000)}K', rotation=45, fontsize=15) for (i, j) in zip(new_insert_id, i_n_ops)]
                # for i in range(len(n_ops)):
                #     x_values = [new_find_id[i], new_find_id[i]]
                #     y_values = [n_ops[i], n_ops[i] + 20000000]
                #     twin1.plot(x_values, y_values, color = 'w')

                # for i in range(len(i_n_ops)):
                #     x_values = [new_insert_id[i], new_insert_id[i]]
                #     y_values = [i_n_ops[i], i_n_ops[i] + 20000000]
                #     twin1.plot(x_values, y_values, color = 'w')

                pps1 = ax.bar(new_insert_id, i_lock_opp, align='center', width=0.09, color='r', alpha=0.25)#, label = "insert")
                pps2 = ax.bar(new_find_id, lock_opp,  width=0.09, color='r', align='center', alpha=0.25, label = "lock opp")
                ax.bar(new_find_id, tot_time, width=0.09, color='b', align='center', label = "find")
                ax.bar(new_insert_id, i_tot_time, width=0.09, color='g', align='center', label = "insert")
                handles, labels = ax.get_legend_handles_labels()

                # reverse the order
                ax.set(yscale = "log", ylim=[1, 10**6])
                ax.set_ylabel("Lock Hold Time (ms)", fontsize=13)
                ax.set_xlabel("Applications", fontsize=13)
                # if (applications == 2):
                plt.xticks([]) 
                #     //other_labels = ["Application 1", "Application 2", ""]
                # else:

                #ax.set_xticklabels([""])
                #ax.set_ylim(bottom = 0)
                #plt.text(new_insert_id[0], i_n_ops[0], 'Throughput', ha='left')
                #Annotating a point
                # Put a legend below current axis
                #ax.legend(loc='upper center', bbox_to_anchor=(0.5, 0.05),
                #        title='Critical Section Total Time', fancybox=True, shadow=True, ncol=5)
                #twin1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
                #        title='Throughput', fancybox=True, shadow=True, ncol=5)s
            
                ax.legend(loc='upper center', bbox_to_anchor=(0.5, 0.1),
                        fancybox=True, shadow=True, fontsize=13, ncol=5)
                # Add a colorbar to the plot to represent the 'z' variable
                #ax.legend()
                #plt.plot(genuine_id, wc_time)
                n = len(filename)
                #plt.title("Total lock hold per thread")
                plt.tight_layout()
                ratio_string = ""
                for i in ratio:
                    ratio_string = ratio_string + str(i) + "_"
                figName = "./graphs/ns_c_lock_fair_hash_graphs/applications" + str(applications) + "_ratio_" + ratio_string + "_duration_" + str(duration) + "_total_time.png"
                plt.savefig(figName)          
                plt.close()


