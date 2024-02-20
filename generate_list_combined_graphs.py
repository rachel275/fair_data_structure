import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D, HandlerTuple
import numpy as np
import os
import csv
import sys


rootdir = "./tables/"
for dir in os.listdir(rootdir):
        if dir.split('_')[-2] == "list":
            type = dir.split('_list')[0]
            for filename in os.listdir("./tables/" + dir):
                with open(os.path.join("./tables/" + dir, filename), 'r') as file:
                    if ((filename.endswith("_lock_CLOUDLAB.csv") == False) and ("ns_c_list" in dir)):# or (filename.endswith("_basecase_CLOUDLAB.csv") == True )):
                        ithreads = int(filename.split('_')[1]) 
                        fthreads = int(filename.split('_')[3]) 
                        duration = filename.split('_')[5]
                        if(int(ithreads) == 4 and int(fthreads) == 4 and int(duration) == 60):
                            print ("ns c  - got here")
                            reader = csv.reader(file)
                            i = -1
                            thread_type = []
                            genuine_id = []
                            insert_id = []
                            tot_time = []
                            i_tot_time = []
                            n_ops = []
                            i_n_ops = []

                            for row in reader:
                                if i == -1:
                                    i = 1
                                else:
                                    #need to ignore the first line!
                                    thread_type.append(row[int(0)])
                                    if (row[int(0)] == "insert"):
                                        insert_id.append(int(row[int(1)]))
                                        i_tot_time.append(float(row[int(5)]))
                                        i_n_ops.append(int(row[int(2)]))  
                                    else:
                                        genuine_id.append(int(row[int(1)]))
                                        tot_time.append(float(row[int(5)]))
                                        n_ops.append(int(row[int(2)]))

                    if ((filename.endswith("_sepCPU_CLOUDLAB.csv") == True) and ("default_list" in dir)):# or (filename.endswith("_basecase_CLOUDLAB.csv") == True )):
                        ithreads = int(filename.split('_')[1]) 
                        fthreads = int(filename.split('_')[3]) 
                        duration = filename.split('_')[5]
                        if (int(ithreads) == 4 and int(fthreads) == 4 and int(duration) == 60):
                            print ("default - got here")
                            reader = csv.reader(file)
                            i = -1

                            def_thread_type = []
                            def_genuine_id = []
                            def_insert_id = []
                            def_tot_time = []
                            def_i_tot_time = []
                            def_n_ops = []
                            def_i_n_ops = []

                            for row in reader:
                                if i == -1:
                                    i = 1
                                else:
                                    #need to ignore the first line!
                                    def_thread_type.append(row[int(0)])
                                    if (row[int(0)] == "insert"):
                                        def_insert_id.append(int(row[int(1)]))
                                        def_i_tot_time.append(float(row[int(5)]))
                                        def_i_n_ops.append(int(row[int(2)]))  
                                    else:
                                        def_genuine_id.append(int(row[int(1)]))
                                        def_tot_time.append(float(row[int(5)]))
                                        def_n_ops.append(int(row[int(2)]))


                    if (((filename.endswith("_lock_CLOUDLAB.csv")) and ("ns_c_list" in dir))):# or (filename.endswith("_basecase_CLOUDLAB.csv") == True )):
                        ithreads = int(filename.split('_')[1]) 
                        fthreads = int(filename.split('_')[3]) 
                        duration = int(filename.split('_')[5])
                        if (int(ithreads) == 4 and int(fthreads) == 4 and int(duration) == 60):

                            print ("lock - got here")
                            reader = csv.reader(file)
                            i = -1

                            lck_thread_type = []
                            lck_genuine_id = []
                            lck_insert_id = []
                            lck_tot_time = []
                            lck_i_tot_time = []
                            lck_n_ops = []
                            lck_i_n_ops = []

                            for row in reader:
                                if i == -1:
                                    i = 1
                                    print (" i is 1")
                                else:
                                    lck_thread_type.append(row[int(0)])
                                    print ("we have reached here")
                                    if (row[int(0)] == "insert"):
                                        lck_insert_id.append(int(row[int(1)]))
                                        lck_i_tot_time.append(float(row[int(5)]))
                                        lck_i_n_ops.append(int(row[int(2)]))  
                                    else:
                                        print("we are here doing something")
                                        lck_genuine_id.append(int(row[int(1)]))
                                        lck_tot_time.append(float(row[int(5)]))
                                        lck_n_ops.append(int(row[int(2)]))


new_insert_id = []
for i in insert_id:
    new_insert_id.append(i - len(genuine_id))

tot_n_ops = []
tot_id = []
# for i in range(len(new_insert_id) * 2):
#     if (i % 2 == 0):
#         tot_n_ops.append(n_ops[int(i/2)])
#     else:
#         tot_n_ops.append(i_n_ops[int((i-1)/2)])


#f_threads = [x - 0.2 for x in genuine_id]
#i_threads = [x - 0.15 for x in new_insert_id]

#default list
def_new_insert_id = []
for i in def_insert_id:
    def_new_insert_id.append(i - len(def_genuine_id))

def_tot_n_ops = []
def_tot_id = []
for i in range(len(def_new_insert_id) * 2):
    if (i % 2 == 0):
        def_tot_n_ops.append(def_n_ops[int(i/2)])
    else:
        def_tot_n_ops.append(def_i_n_ops[int((i-1)/2)])


for i in range(24):
    tot_id.append(i)

tot_n_ops = def_n_ops + def_i_n_ops + n_ops + i_n_ops + lck_n_ops + lck_i_n_ops

#def_f_threads = [x + 0.15 for x in def_genuine_id]
#def_i_threads = [x + 0.2 for x in def_new_insert_id]

#lock list
lck_new_insert_id = []
for i in lck_insert_id:
    lck_new_insert_id.append(i - len(lck_genuine_id))

lck_tot_n_ops = []
lck_tot_id = []
for i in range(len(lck_new_insert_id) * 2):
    if (i % 2 == 0):
        lck_tot_n_ops.append(lck_n_ops[int(i/2)])
    else:
        lck_tot_n_ops.append(lck_i_n_ops[int((i-1)/2)])


for i in lck_new_insert_id:
    lck_tot_id.extend([i - 0.05, i + 0.1])

#lck_f_threads = [x - 0.025 for x in lck_genuine_id]
#lck_i_threads = [x + 0.025 for x in lck_new_insert_id]

for i in range(len(genuine_id)):
    genuine_id[i] += 8

for i in range(len(insert_id)):
    insert_id[i] += 8

for i in range(len(lck_genuine_id)):
    lck_genuine_id[i] += 16

for i in range(len(lck_insert_id)):
    lck_insert_id[i] += 16

print (lck_insert_id)
fig, ax = plt.subplots()

twin1 = ax.twinx()
#twin2 = ax.twinx()

ax.bar(genuine_id, tot_time, width=0.5, color='b', align='center', label = "find (ns c)")
ax.bar(insert_id, i_tot_time, width=0.5, color='c', align='center', label = "insert (ns c)")

ax.bar(lck_genuine_id, lck_tot_time, width=0.5, color='r', align='center', label = "find (ns c lock)")
ax.bar(lck_insert_id, lck_i_tot_time, width=0.5, color='m', align='center', label = "insert (ns c lock)")

ax.bar(def_genuine_id, def_tot_time, width=0.5, color='y', align='center', label = "find (default)")
ax.bar(def_insert_id, def_i_tot_time, width=0.5, color='g', align='center', label = "insert (default)")

handles, labels = ax.get_legend_handles_labels()

# reverse the order
ax.set(xlabel="Thread id", ylabel="Time (ms)",  yscale = "log")    

twin1.plot(tot_id, tot_n_ops, linestyle='-', color='k')
twin1.set(ylabel="Number of operations", yscale = "log")
plt.text(tot_id[0], tot_n_ops[0], 'Throughput', ha='left')
plt.xticks(np.arange(min(def_genuine_id), max(insert_id)+1, 4)) 
# Annotating a point

# # Add a colorbar to the plot to represent the 'z' variable
# plt.colorbar(label='Color Variable (z)')
plt.legend(handles[::-1], labels[::-1])
#plt.plot(genuine_id, wc_time)
n = len(filename)
plt.title("Total lock hold per thread (CLOUDLAB," + str(duration) + "s)") 
figName = "./graphs/ns_c_list_graphs/threads" + str(ithreads) + "_" + str(fthreads)  + "_duration " + str(duration) + "_combined.png"
plt.savefig(figName)          
plt.close()