import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D, HandlerTuple
import numpy as np
import os
import csv
import sys

#argument 1 = different columns: fairness index, total executions, winner and victim threads, clustering

#plot 1: fairness index of different thread amounts
#plot 2: total executions of each thread amounts
#plot 3: 

path = "./tables/futex_example_tables"
fileCount = 0;
for filename in os.listdir(path):
    with open(os.path.join(path, filename), 'r') as file:
        if (filename.split('_')[0] == "buckets"):
            file.close()
            continue
        else:
            nthreads = int(filename.split('_')[1])#find_info(information, 1).lstrip().rstrip()
            buckets = int(filename.split('_')[3].split('.')[0])#find_info(information, 1).lstrip().rstrip()
            i = -1
            reader = csv.reader(file)
            no_threads = []
            thread_type = []
            futex_id = []
            insert_id = []
            wc_bucket = []
            i_wc_bucket = []
            wc_time = []
            i_wc_time = []
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
                        i_wc_bucket.append(int(row[int(2)]))
                        i_wc_time.append(float(row[int(3)]))
                        i_tot_time.append(float(row[int(4)]))
                        i_n_ops.append(int(row[int(5)]))  
                    else:
                        futex_id.append(int(row[int(1)]))
                        wc_bucket.append(int(row[int(2)]))
                        wc_time.append(float(row[int(3)]))
                        tot_time.append(float(row[int(4)]))
                        n_ops.append(int(row[int(5)]))

    bucket_true = []
    for i in wc_bucket:
        if i == 1:
            bucket_true.append(1)
        else:
            bucket_true.append(0)
    #plot threads against their 
    #plt.plot(futex_id, wc_time, color='b', linestyle='None', marker='o')
    #plt.plot(insert_id, i_wc_time, color='r', linestyle='None', marker='o')
    fig, ax = plt.subplots()
    scatter = ax.scatter(futex_id, wc_time, s=50,  c=bucket_true, cmap='Reds')
    scatter2 = ax.scatter(insert_id, i_wc_time, s=50,  c=1, cmap='Reds_r')
    #plt.ylim(0, 1.1)
    plt.xlabel("futex thread id")
    plt.ylabel("critical section (ms)")
    plt.xticks(np.arange(min(futex_id), max(futex_id)+1, 4))  
    # Annotating a point
    plt.text(insert_id[0], i_wc_time[0], 'insert thread', ha='left')

    # # Add a colorbar to the plot to represent the 'z' variable
    # plt.colorbar(label='Color Variable (z)')

    # Add a legend for the scatterplot
    plt.legend([' False', 'True'], title="Bucket 1")
    plt.plot(futex_id, wc_time)
    n = len(filename)
    plt.title("Worst case critical section per thread") 
    figName = "./graphs/futex_example_graphs/threads" + str(nthreads) + "_buckets" + str(buckets) +"_worst_case_time.png"
    plt.savefig(figName)          
    plt.close()