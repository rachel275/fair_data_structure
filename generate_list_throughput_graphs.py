import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D, HandlerTuple
import numpy as np
import os
import csv
import sys


rratio = [0, 1, 2, 3, 4, 5, 6, 7]
colour_list = ["g", "b","g", "b","g", "b","g", "b"]
fig, ax = plt.subplots(figsize=(12,6))
count = 0
final_ratio = []
v = 0
jane = 25
fileCount = 0;
rootdir = "./tables/"
# for dir in os.listdir(rootdir):
#     type = dir.split('_hash_tables')[0]
#     #print(type)
#     if type == "default_fair":
#         for filename in os.listdir("./tables/" + dir):
#             #print(filename)
#             with open(os.path.join("./tables/" + dir, filename), 'r') as file:
#                 applications = int(filename.split('_')[3]) 
#                 ratio = []
#                 #print("reached here     ")
#                 for i in range(applications):
#                     ratio.append(int(filename.split('_')[i + 5]))
#                 duration = filename.split('_')[i + 7]
#                 i = -1
#                 #print(applications)
#                 #print(ratio)
#                 if(applications == 4 and ratio[3]== 25):
#                     print(ratio)
#                     reader = csv.reader(file)
#                     no_threads = []
#                     thread_type = []
#                     genuine_id = []
#                     insert_id = []
#                     wc_time = []
#                     i_wc_time = []
#                     tot_time = []
#                     i_tot_time = []
#                     n_ops = []
#                     i_n_ops = []
#                     lock_opp = []
#                     i_lock_opp = []
#                     for row in reader:
#                         if i == -1:
#                             i = 1
#                         else:
#                             #need to ignore the first line!
#                             thread_type.append(row[int(0)])
#                             if (row[int(0)] == "insert"):
#                                 insert_id.append(int(row[int(1)]))
#                                 i_wc_time.append(float(row[int(3)]))
#                                 i_tot_time.append(float(row[int(4)]))
#                                 i_n_ops.append(int(row[int(2)]))  
#                                 i_lock_opp.append(float(row[int(5)]))
#                             else:
#                                 genuine_id.append(int(row[int(1)]))
#                                 tot_time.append(float(row[int(4)]))
#                                 n_ops.append(int(row[int(2)]))
#                                 lock_opp.append(float(row[int(5)])) 
#                     new_n_ops = []
#                     for i in n_ops:
#                         new_n_ops.append(i)
#                         new_n_ops.append(i)
#                     new_n_ops.append(n_ops[0])
#                     print(new_n_ops)
#                     count = count + 1
#                     ax.plot(rratio, new_n_ops, label = "ideal linked list")
                    
default_fair_index = []
ns_c_fair_index = []

dbl_rratio = [0, 0.01, 0.02 , 1, 1.01, 1.02, 2, 2.01, 2.02, 3, 3.01, 3.02, 4, 4.01, 4.02, 5, 5.01, 5.02, 6, 6.01, 6.02, 7, 7.01, 7.02]
for dir in os.listdir(rootdir):
    type = dir.split('_hash_tables')[0]
    if type == "ns_c_fair" or type == "default_fair":
        new_n_ops = []
        for sarah in rratio:
            for filename in os.listdir("./tables/" + dir):
            #print(filename)
                with open(os.path.join("./tables/" + dir, filename), 'r') as file:
                    applications = int(filename.split('_')[1]) 
                    ratio = []
                    no_hundreds = 0
                    #print("reached here     ")
                    for i in range(applications):
                        new_rat = int(filename.split('_')[i + 3])
                        ratio.append(new_rat)
                        if new_rat == 100:
                            no_hundreds = no_hundreds + 1
                    duration = filename.split('_')[i + 5]
                    i = -1
                    #print(applications)
                    #print(ratio)
                    if(applications == 8 and no_hundreds == sarah):
                        print(ratio)
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
                                    i_tot_time.append(float(row[int(3)]))
                                    i_n_ops.append(int(row[int(2)]))  
                                    #i_lock_opp.append(float(row[int(5)]))
                                else:
                                    genuine_id.append(int(row[int(1)]))
                                    tot_time.append(float(row[int(3)]))
                                    n_ops.append(int(row[int(2)]))
                                    #lock_opp.append(float(row[int(5)])) 
                        for i in range(len(genuine_id)):
                            if genuine_id[i] == 0:
                                new_n_ops.append(n_ops[i])
        print(new_n_ops)
        ax.plot(dbl_rratio, new_n_ops, label = str(type) + " linked list")

default_fair_index = []
ns_c_fair_index = []
dbl_rratio =[0, 0.01, 0.02 , 1, 1.01, 1.02, 2, 2.01, 2.02, 3, 3.01, 3.02, 4, 4.01, 4.02, 5, 5.01, 5.02, 6, 6.01, 6.02, 7, 7.01, 7.02]
for dir in os.listdir(rootdir):
    type = dir.split('_hash_tables')[0]
    if type == "ns_c_lock_fair":
        new_n_ops = []
        for sarah in rratio:
            for filename in os.listdir("./tables/" + dir):
            #print(filename)
                with open(os.path.join("./tables/" + dir, filename), 'r') as file:
                    applications = int(filename.split('_')[1]) 
                    ratio = []
                    no_hundreds = 0
                    #print("reached here     ")
                    for i in range(applications):
                        new_rat = int(filename.split('_')[i + 3])
                        ratio.append(new_rat)
                        if new_rat == 100:
                            no_hundreds = no_hundreds + 1
                    duration = filename.split('_')[i + 5]
                    i = -1
                    #print(applications)
                    #print(ratio)
                    if(applications == 8 and no_hundreds == sarah):
                        print(no_hundreds)
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
                                    i_tot_time.append(float(row[int(3)]))
                                    i_n_ops.append(int(row[int(2)]))  
                                else:
                                    genuine_id.append(int(row[int(1)]))
                                    tot_time.append(float(row[int(3)]))
                                    n_ops.append(int(row[int(2)]))
                        for i in range(len(genuine_id)):
                            if genuine_id[i] == 0:
                                new_n_ops.append(n_ops[i])
        print(new_n_ops)
        ax.plot(dbl_rratio, new_n_ops, label = str(type) + " linked list")
ax.set_ylabel("Throughput of application 1", fontsize=15)#,  yscale = "log")#, #ylim=[1, 10**6])
ax.set_xlabel("Number of high insert applications", fontsize=15)

ax.set_xticks([0, 1, 2, 3, 4, 5, 6, 7])
#x_label = ["100:0", "75:25", "50:50", "25:75", "0:100"]
#ax.set_xticklabels(x_label, fontsize=13)

handles, labels = ax.get_legend_handles_labels()

by_label = dict(zip(labels, handles))

ax.legend(by_label.values(), by_label.keys(), loc='upper center', bbox_to_anchor=(0.2, 0.7),
            fancybox=True, shadow=True, fontsize=15)
#plt.title("Total lock hold per thread")
plt.tight_layout()
ratio_string = ""
for i in final_ratio:
    ratio_string = ratio_string + str(i) + "_"
figName = "./graphs/ns_c_lock_fair_hash_graphs/applications_8_throughput.png"
plt.savefig(figName)          
plt.close()