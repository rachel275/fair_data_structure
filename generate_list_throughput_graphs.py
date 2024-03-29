import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D, HandlerTuple
import numpy as np
import os
import csv
import sys


rratio = [0, 25, 50, 75, 100]
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
                    new_n_ops = []
                    for i in n_ops:
                        new_n_ops.append(i/2)
                        new_n_ops.append(i/2)
                    new_n_ops.append(n_ops[0]/2)
                    print(new_n_ops)
                    count = count + 1
                    ax.plot(rratio, new_n_ops, label = "ideal linked list")
                    #v = v + 1
new_n_ops = []
for sarah in rratio:
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
                    if(applications == 2 and ratio[0] == 50 and ratio[1] == sarah):
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
                        new_n_ops = []
                        for i in range(len(genuine_id)):
                            if genuine_id[i] == 0:
                                new_n_ops.append(n_ops[i])
    print(new_n_ops)
    #ax.plot(rratio, new_n_ops, label = str(type) + "linked list")
                        #v = v + 1

                    # reverse the order
ax.set(ylabel="Time (ms)",  yscale = "log")#, #ylim=[1, 10**6])
handles, labels = ax.get_legend_handles_labels()

                        # if (applications == 2):
# ax.set_xticks([0.7, 3.3, 5.8])
# xlabels = ["Ideal linked list", "Default linked list ", "Fair linked list"]
# ax.set_xticklabels(xlabels, fontsize=15)
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
figName = "./graphs/ns_c_fair_list_graphs/applications_2_ratio_" + ratio_string + "duration_64_throughput.png"
plt.savefig(figName)          
plt.close()