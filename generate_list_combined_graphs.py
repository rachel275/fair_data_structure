import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D, HandlerTuple
import numpy as np
import os
import csv
import sys


colour_list = ["g", "b","g", "b","g", "b","g", "b"]
fig, ax = plt.subplots(figsize=(10,3))
count = 0
final_ratio = []
v = 0
jane = 25
fileCount = 0;
rootdir = "./tables/"
for dir in os.listdir(rootdir):
    type = dir.split('_list_tables')[0]
    #print(type)
    if type == "default_fair":
        for filename in os.listdir("./tables/" + dir):
            #print(filename)
            with open(os.path.join("./tables/" + dir, filename), 'r') as file:
                applications = int(filename.split('_')[1]) 
                ratio = []
                #print("reached here     ")
                for i in range(applications):
                    ratio.append(int(filename.split('_')[i + 3]))
                duration = filename.split('_')[i + 5]
                i = -1
                #print(applications)
                #print(ratio)
                if(applications == 1 and ratio[0]== 50):
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
                                i_wc_time.append(float(row[int(3)]))
                                i_tot_time.append(float(row[int(4)]))
                                i_n_ops.append(int(row[int(2)]))  
                                i_lock_opp.append(float(row[int(5)]))
                            else:
                                genuine_id.append(int(row[int(1)]))
                                tot_time.append(float(row[int(4)]))
                                n_ops.append(int(row[int(2)]))
                                lock_opp.append(float(row[int(5)])) 
                    counter_one = 0
                    counter_two = 0
                    counter_three = 0
                    counter_four = 0
                    new_insert_id = []
                    new_find_id = []

                    new_i_lock_opp = []
                    new_f_find_opp = []

                    new_i_ops = []
                    new_ops = []
                    for i in insert_id:
                        if i == 0:
                            if counter_one == 0:
                                new_insert_id.append(i - (counter_one + 0.05) + count)
                                counter_one = counter_one + 0.05
                            else:
                                new_insert_id.append(i - (counter_one + 0.1)+ count)
                                counter_one = counter_one + 0.1
                        elif i == 1:
                            if counter_two == 0:
                                new_insert_id.append(i - (counter_two + 0.05)+ count)
                                counter_two = counter_two + 0.05
                            else:
                                new_insert_id.append(i - (counter_two + 0.1)+ count)
                                counter_two = counter_two + 0.1
                        elif i == 2:
                            new_insert_id.append(i - (counter_three + 0.1)+ count)
                            counter_three = counter_three + 0.1
                        elif i == 3:
                            new_insert_id.append(i - (counter_four + 0.1)+ count)
                            counter_four = counter_four + 0.1

                    count_one = 0
                    count_two = 0
                    count_three = 0
                    count_four = 0

                    for i in genuine_id:
                        if i == 0:
                            if count_one == 0:
                                new_find_id.append(i + (count_one + 0.05)+ count)
                                count_one = count_one + 0.05
                            else:
                                new_find_id.append(i + (count_one + 0.1)+ count)
                                count_one = count_one + 0.1
                        elif i == 1:
                            if count_two == 0:
                                new_find_id.append(i + (count_two + 0.05)+ count)
                                count_two = count_two + 0.05
                            else:
                                new_find_id.append(i + (count_two + 0.1)+ count)
                                count_two = count_two + 0.1
                        elif i == 2:
                            new_find_id.append(i + (count_three + 0.1)+ count)
                            count_three = count_three + 0.1
                        elif i == 3:
                            new_find_id.append(i + (count_four + 0.1)+ count)
                            count_four = count_four + 0.1

                    count = count + 1
                    print(count)
                    print(filename)
                    ax.set(ylim=[1, 10**13], yscale='log', yticks=[])
                    ax.set_ylabel("Throughput", rotation=-90, labelpad=12)
                    #[plt.text(i, 200000000, f'{int(j  / 1000)}K', rotation=45, fontsize=15) for (i, j) in zip(new_find_id, n_ops)]
                    for (i, j) in zip(new_find_id, n_ops):
                        if (j > 1000000):
                            ax.text(i, max(lock_opp) + 10000, f'{round(float(j  / 2000000), 1)}M', rotation=80, fontsize=10)
                        else:
                            ax.text(i, max(lock_opp) + 10000, f'{round(float(j  / 2000), 1)}K', rotation=80, fontsize=10)
                    for (i, j) in zip(new_insert_id, i_n_ops):
                        if (j > 1000000):
                            ax.text(i, max(i_lock_opp) + 10000, f'{round(float(j  / 2000000), 1)}M', rotation=80, fontsize=10)
                        else:
                            ax.text(i, max(i_lock_opp) + 10000, f'{round(float(j  / 2000), 1)}K', rotation=80, fontsize=10)

                    pps1 = ax.bar(new_insert_id, i_lock_opp, align='center', width=0.09, color='r', alpha=0.25)#, label = "insert")
                    pps2 = ax.bar(new_find_id, lock_opp,  width=0.09, color='r', align='center', alpha=0.25, label = "lock opp")
                    ax.bar(new_find_id, tot_time, width=0.09, color=colour_list[v], align='center', label = "find")
                    v = v + 1
                    ax.bar(new_insert_id, i_tot_time, width=0.09, color=colour_list[v], align='center', label = "insert")
                    v = v + 1

for dir in os.listdir(rootdir):
    type = dir.split('_list_tables')[0]
    #print(type)
    if type == "default_fair":
        for filename in os.listdir("./tables/" + dir):
            #print(filename)
            with open(os.path.join("./tables/" + dir, filename), 'r') as file:
                applications = int(filename.split('_')[1]) 
                ratio = []
                #print("reached here     ")
                for i in range(applications):
                    ratio.append(int(filename.split('_')[i + 3]))
                duration = filename.split('_')[i + 5]
                i = -1
                #print(applications)
                #print(ratio)
                if(applications == 1 and ratio[0]== jane):
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
                                i_wc_time.append(float(row[int(3)]))
                                i_tot_time.append(float(row[int(4)]))
                                i_n_ops.append(int(row[int(2)]))  
                                i_lock_opp.append(float(row[int(5)]))
                            else:
                                genuine_id.append(int(row[int(1)]))
                                tot_time.append(float(row[int(4)]))
                                n_ops.append(int(row[int(2)]))
                                lock_opp.append(float(row[int(5)])) 
                    counter_one = 0
                    counter_two = 0
                    counter_three = 0
                    counter_four = 0
                    new_insert_id = []
                    new_find_id = []

                    new_i_lock_opp = []
                    new_f_find_opp = []

                    new_i_ops = []
                    new_ops = []
                    for i in insert_id:
                        if i == 0:
                            if counter_one == 0:
                                new_insert_id.append(i - (counter_one + 0.05) + count)
                                counter_one = counter_one + 0.05
                            else:
                                new_insert_id.append(i - (counter_one + 0.1)+ count)
                                counter_one = counter_one + 0.1
                        elif i == 1:
                            if counter_two == 0:
                                new_insert_id.append(i - (counter_two + 0.05)+ count)
                                counter_two = counter_two + 0.05
                            else:
                                new_insert_id.append(i - (counter_two + 0.1)+ count)
                                counter_two = counter_two + 0.1
                        elif i == 2:
                            new_insert_id.append(i - (counter_three + 0.1)+ count)
                            counter_three = counter_three + 0.1
                        elif i == 3:
                            new_insert_id.append(i - (counter_four + 0.1)+ count)
                            counter_four = counter_four + 0.1

                    count_one = 0
                    count_two = 0
                    count_three = 0
                    count_four = 0

                    for i in genuine_id:
                        if i == 0:
                            if count_one == 0:
                                new_find_id.append(i + (count_one + 0.05)+ count)
                                count_one = count_one + 0.05
                            else:
                                new_find_id.append(i + (count_one + 0.1)+ count)
                                count_one = count_one + 0.1
                        elif i == 1:
                            if count_two == 0:
                                new_find_id.append(i + (count_two + 0.05)+ count)
                                count_two = count_two + 0.05
                            else:
                                new_find_id.append(i + (count_two + 0.1)+ count)
                                count_two = count_two + 0.1
                        elif i == 2:
                            new_find_id.append(i + (count_three + 0.1)+ count)
                            count_three = count_three + 0.1
                        elif i == 3:
                            new_find_id.append(i + (count_four + 0.1)+ count)
                            count_four = count_four + 0.1

                    count = count + 1.7
                    print(count)
                    print(filename)
                    ax.set(ylim=[1, 10**13], yscale='log', yticks=[])
                    ax.set_ylabel("Throughput", rotation=-90, labelpad=12)
                    #[plt.text(i, 200000000, f'{int(j  / 1000)}K', rotation=45, fontsize=15) for (i, j) in zip(new_find_id, n_ops)]
                    for (i, j) in zip(new_find_id, n_ops):
                        if (j > 1000000):
                            ax.text(i, max(lock_opp) + 10000, f'{round(float(j  / 2000000), 1)}M', rotation=80, fontsize=10)
                        else:
                            ax.text(i, max(lock_opp) + 10000, f'{round(float(j  / 2000), 1)}K', rotation=80, fontsize=10)
                    for (i, j) in zip(new_insert_id, i_n_ops):
                        if (j > 1000000):
                            ax.text(i, max(i_lock_opp) + 10000, f'{round(float(j  / 2000000), 1)}M', rotation=80, fontsize=10)
                        else:
                            ax.text(i, max(i_lock_opp) + 10000, f'{round(float(j  / 2000), 1)}K', rotation=80, fontsize=10)

                    pps1 = ax.bar(new_insert_id, i_lock_opp, align='center', width=0.09, color='r', alpha=0.25)#, label = "insert")
                    pps2 = ax.bar(new_find_id, lock_opp,  width=0.09, color='r', align='center', alpha=0.25, label = "lock opp")
                    ax.bar(new_find_id, tot_time, width=0.09, color=colour_list[v], align='center', label = "find")
                    v = v + 1
                    ax.bar(new_insert_id, i_tot_time, width=0.09, color=colour_list[v], align='center', label = "insert")
                    v = v + 1

for dir in os.listdir(rootdir):
    type = dir.split('_list_tables')[0]
    #print(type)
    if type == "ns_c_fair" or type == "default_fair":
        for filename in os.listdir("./tables/" + dir):
            #print(filename)
            with open(os.path.join("./tables/" + dir, filename), 'r') as file:
                applications = int(filename.split('_')[1]) 
                ratio = []
                #print("reached here     ")
                for i in range(applications):
                    ratio.append(int(filename.split('_')[i + 3]))
                duration = filename.split('_')[i + 5]
                i = -1
                #print(applications)
                #print(ratio)
                if(applications == 2 and ratio[0] == 50 and ratio[1] == jane):
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
                                i_wc_time.append(float(row[int(3)]))
                                i_tot_time.append(float(row[int(4)]))
                                i_n_ops.append(int(row[int(2)]))  
                                i_lock_opp.append(float(row[int(5)]))
                            else:
                                genuine_id.append(int(row[int(1)]))
                                tot_time.append(float(row[int(4)]))
                                n_ops.append(int(row[int(2)]))
                                lock_opp.append(float(row[int(5)])) 

                    counter_one = 0
                    counter_two = 0
                    counter_three = 0
                    counter_four = 0
                    new_insert_id = []
                    new_find_id = []

                    new_i_lock_opp = []
                    new_f_find_opp = []

                    new_i_ops = []
                    new_ops = []
                    for i in insert_id:
                        if i == 0:
                            if counter_one == 0:
                                new_insert_id.append(i - (counter_one + 0.05) + count)
                                counter_one = counter_one + 0.05
                            else:
                                new_insert_id.append(i - (counter_one + 0.1)+ count)
                                counter_one = counter_one + 0.1
                        elif i == 1:
                            if counter_two == 0:
                                new_insert_id.append(i - (counter_two + 0.05)+ count)
                                counter_two = counter_two + 0.05
                            else:
                                new_insert_id.append(i - (counter_two + 0.1)+ count)
                                counter_two = counter_two + 0.1
                        elif i == 2:
                            new_insert_id.append(i - (counter_three + 0.1)+ count)
                            counter_three = counter_three + 0.1
                        elif i == 3:
                            new_insert_id.append(i - (counter_four + 0.1)+ count)
                            counter_four = counter_four + 0.1

                    count_one = 0
                    count_two = 0
                    count_three = 0
                    count_four = 0

                    for i in genuine_id:
                        if i == 0:
                            if count_one == 0:
                                new_find_id.append(i + (count_one + 0.05)+ count)
                                count_one = count_one + 0.05
                            else:
                                new_find_id.append(i + (count_one + 0.1)+ count)
                                count_one = count_one + 0.1
                        elif i == 1:
                            if count_two == 0:
                                new_find_id.append(i + (count_two + 0.05)+ count)
                                count_two = count_two + 0.05
                            else:
                                new_find_id.append(i + (count_two + 0.1)+ count)
                                count_two = count_two + 0.1
                        elif i == 2:
                            new_find_id.append(i + (count_three + 0.1)+ count)
                            count_three = count_three + 0.1
                        elif i == 3:
                            new_find_id.append(i + (count_four + 0.1)+ count)
                            count_four = count_four + 0.1

                    count = count + 2.7
                    print(count)
                    print(filename)
                    ax.set(ylim=[1, 10**13], yscale='log', yticks=[])
                    ax.set_ylabel("Throughput", rotation=-90, labelpad=12)
                    #[plt.text(i, 200000000, f'{int(j  / 1000)}K', rotation=45, fontsize=15) for (i, j) in zip(new_find_id, n_ops)]
                    for (i, j) in zip(new_find_id, n_ops):
                        if (j > 1000000):
                            ax.text(i, max(lock_opp) + 10000, f'{round(float(j  / 1000000), 1)}M', rotation=80, fontsize=10)
                        else:
                            ax.text(i, max(lock_opp) + 10000, f'{round(float(j  / 1000), 1)}K', rotation=80, fontsize=10)
                    for (i, j) in zip(new_insert_id, i_n_ops):
                        if (j > 1000000):
                            ax.text(i, max(i_lock_opp) + 10000, f'{round(float(j  / 1000000), 1)}M', rotation=80, fontsize=10)
                        else:
                            ax.text(i, max(i_lock_opp) + 10000, f'{round(float(j  / 1000), 1)}K', rotation=80, fontsize=10)

                    pps1 = ax.bar(new_insert_id, i_lock_opp, align='center', width=0.09, color='r', alpha=0.25)#, label = "insert")
                    pps2 = ax.bar(new_find_id, lock_opp,  width=0.09, color='r', align='center', alpha=0.25, label = "lock opp")
                    ax.bar(new_find_id, tot_time, width=0.09, color=colour_list[v], align='center', label = "find")
                    v = v + 1
                    ax.bar(new_insert_id, i_tot_time, width=0.09, color=colour_list[v], align='center', label = "insert")
                    v = v + 1

                    final_ratio = ratio

                    # reverse the order
ax.set(ylabel="Time (ms)",  yscale = "log", ylim=[1, 10**6])
handles, labels = ax.get_legend_handles_labels()

                        # if (applications == 2):
ax.set_xticks([0.7, 3.3, 5.8])
xlabels = ["Ideal linked list", "Default linked list ", "Fair linked list"]
ax.set_xticklabels(xlabels, fontsize=15)
by_label = dict(zip(labels, handles))
# .legend(by_label.values(), by_label.keys(), loc='upper center', bbox_to_anchor=(0.8, 0.2),
#        fancybox=True, shadow=True, fontsize=15, ncol=8)
ax.legend(by_label.values(), by_label.keys(), loc='upper center', bbox_to_anchor=(0.5, 0.2),
            fancybox=True, shadow=True, fontsize=10, ncol=6)
#plt.title("Total lock hold per thread")
plt.tight_layout()
ratio_string = ""
for i in final_ratio:
    ratio_string = ratio_string + str(i) + "_"
figName = "./graphs/ns_c_fair_list_graphs/applications_2_ratio_" + ratio_string + "duration_64_shared_time.png"
plt.savefig(figName)          
plt.close()