import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D, HandlerTuple
import numpy as np
import os
import csv
import sys



path = "./tables/default_list_tables/"  #FILL THIS IN HERE
fileCount = 0;
for filename in os.listdir(path):
    with open(os.path.join(path, filename), 'r') as file:
        if (filename.endswith("_CLOUDLAB.csv") == False):
            file.close()
            continue
        nthreads = int(filename.split('_')[1]) #find_info(information, 1).lstrip().rstrip()
        ratios = filename.split('_')[5].split('.')
        duration = filename.split('_')[3]
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
        n_entries = []
        i_n_entries = []
        for row in reader:
            if i == -1:
                i = 1
            else:
                #need to ignore the first line!
                thread_type.append(row[int(0)])
                if (row[int(0)] == "malicious"):
                    insert_id.append(int(row[int(1)]))
                    i_wc_time.append(float(row[int(4)]))
                    i_tot_time.append(float(row[int(5)]))
                    i_n_ops.append(int(row[int(2)]))  
                    i_n_entries.append(int(row[int(3)]))  
                else:
                    genuine_id.append(int(row[int(1)]))
                    wc_time.append(float(row[int(4)]))
                    tot_time.append(float(row[int(5)]))
                    n_ops.append(int(row[int(2)]))
                    n_entries.append(int(row[int(3)]))  

    # #plot threads against their 
    # #plt.plot(futex_id, wc_time, color='b', linestyle='None', marker='o')
    # #plt.plot(insert_id, i_wc_time, color='r', linestyle='None', marker='o')
    # fig, ax = plt.subplots()
    # scatter = ax.bar(genuine_id, tot_time)
    # scatter2 = ax.bar(insert_id, i_tot_time)
    # #scatter = ax.bar(genuine_id, n_ops, color = 'blue')
    # #plt.ylim(0, 1.1)
    # plt.xlabel("thread id")
    # plt.ylabel("time (ms)")
    # if (max(genuine_id) == 63):
    #     plt.xticks(np.arange(min(genuine_id), max(genuine_id)+1, 4))  
    # else:
    #     plt.xticks(np.arange(min(genuine_id), max(genuine_id)+1, 2)) 
    # # Annotating a point
    # plt.text(insert_id[0], i_tot_time[0], 'insert thread', ha='left')

    # # # Add a colorbar to the plot to represent the 'z' variable
    # # plt.colorbar(label='Color Variable (z)')

    # #plt.plot(genuine_id, wc_time)
    # n = len(filename)
    # plt.title("Total lock hold per thread (CLOUDLAB," + str(duration) + "s)") 
    # figName = "./graphs/ns_c_list_graphs/threads" + str(nthreads)  + "_duration " + str(duration) + "_ratios_" + str(ratios)  + "_total_time_CLOUDLAB.png"
    # plt.savefig(figName)          
    # plt.close()

    #     #plot threads against their 
    # #plt.plot(futex_id, wc_time, color='b', linestyle='None', marker='o')
    # #plt.plot(insert_id, i_wc_time, color='r', linestyle='None', marker='o')
    # fig, ax = plt.subplots()
    # #scatter = ax.bar(genuine_id, n_ops)
    # scatter2 = ax.bar(insert_id, i_n_ops)
    # scatter = ax.bar(genuine_id, n_ops)
    # #plt.ylim(0, 1.1)
    # plt.xlabel("thread id")
    # plt.ylabel("number of operations")
    # if (max(genuine_id) == 63):
    #     plt.xticks(np.arange(min(genuine_id), max(genuine_id)+1, 4))  
    # else:
    #     plt.xticks(np.arange(min(genuine_id), max(genuine_id)+1, 2)) 
    # # Annotating a point
    # plt.text(insert_id[0], i_n_ops[0], 'insert thread', ha='left')

    # # # Add a colorbar to the plot to represent the 'z' variable
    # # plt.colorbar(label='Color Variable (z)')

    # #plt.plot(genuine_id, wc_time)
    # n = len(filename)
    # plt.title("Number of operations per thread (CLOUDLAB, " + str(duration) + "s)") 
    # figName = "./graphs/ns_c_list_graphs/threads" + str(nthreads)  + "_duration " + str(duration) + "_ratios_" + str(ratios)  + "_n_ops_CLOUDLAB.png"
    # plt.savefig(figName)          
    # plt.close()




            #plot threads against their 
    #plt.plot(futex_id, wc_time, color='b', linestyle='None', marker='o')
    #plt.plot(insert_id, i_wc_time, color='r', linestyle='None', marker='o')
    fig, ax = plt.subplots()
    #scatter = ax.bar(genuine_id, n_ops)
    scatter2 = ax.bar(insert_id, i_n_entries)
    scatter = ax.bar(genuine_id, n_entries)
    #plt.ylim(0, 1.1)
    plt.xlabel("thread id")
    plt.ylabel("number of entries")
    if (max(genuine_id) == 63):
        plt.xticks(np.arange(min(genuine_id), max(genuine_id)+1, 4))  
    else:
        plt.xticks(np.arange(min(genuine_id), max(genuine_id)+1, 2)) 
    # Annotating a point
    plt.text(insert_id[0], i_n_entries[0], 'insert thread', ha='left')

    # # Add a colorbar to the plot to represent the 'z' variable
    # plt.colorbar(label='Color Variable (z)')

    plt.plot(genuine_id, tot_time)
    n = len(filename)
    plt.title("Total critical section time and entries per thread (CLOUDLAB, " + str(duration) + "s)") 
    figName = "./graphs/default_list_graphs/threads" + str(nthreads)  + "_duration " + str(duration) + "_ratios_" + str(ratios)  + "_n_entries_CLOUDLAB.png"
    plt.savefig(figName)          
    plt.close()