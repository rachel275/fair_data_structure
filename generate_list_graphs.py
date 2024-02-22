import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D, HandlerTuple
import numpy as np
import os
import csv
import sys



path = "./tables/ns_c_fair_list_tables/"  #FILL THIS IN HERE
fileCount = 0;
for filename in os.listdir(path):
    with open(os.path.join(path, filename), 'r') as file:
        # if ((filename.split('_')[1] == str(2))):# or (filename.endswith("_basecase_CLOUDLAB.csv") == True )):
        #     file.close()
        #     continue
        applications = int(filename.split('_')[1]) 
        ratio = []
        for i in range(applications):
            ratio.append(int(filename.split('_')[i + 3]))
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
        n_entries = []
        i_n_entries = []
        for row in reader:
            if i == -1:
                i = 1
            else:
                #need to ignore the first line!
                thread_type.append(row[int(0)])
                if (row[int(0)] == "insert"):
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

# we want to group by application i.e thread ID
    #but we want to distingusih between insert and find threads


#for the insert thread, make it slightly less then the id
#for the find threads, make it more than the id

    # new_insert_id = []
    # for i in insert_id:
    #     new_insert_id.append(i - len(genuine_id))

    # print(insert_id)
    # print(new_insert_id)
    # print("\n")

    # tot_n_ops = []
    # tot_id = []
    # for i in range(len(new_insert_id) * 2):
    #     if (i % 2 == 0):
    #         tot_n_ops.append(n_ops[int(i/2)])
    #     else:
    #         tot_n_ops.append(i_n_ops[int((i-1)/2)])
    

    # for i in new_insert_id:
    #     tot_id.extend([i - 0.2, i + 0.2])
    counter_one = 0
    counter_two = 0
    counter_three = 0
    new_insert_id = []
    new_find_id = []

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

    count_one = 0
    count_two = 0
    count_three = 0

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


    # f_threads = [x - 0.2 for x in genuine_id]
    # i_threads = [x + 0.2 for x in new_insert_id]
    print(new_insert_id)
    print(new_find_id)


    fig, ax = plt.subplots()

    #twin1 = ax.twinx()
    #twin2 = ax.twinx()

    ax.bar(new_find_id, tot_time, width=0.09, color='b', align='center', label = "find")
    ax.bar(new_insert_id, i_tot_time, width=0.09, color='g', align='center', label = "insert")

    handles, labels = ax.get_legend_handles_labels()

    # reverse the order
    ax.set(xlabel="Threads", ylabel="Time (ms)",  yscale = "log")    

    # twin1.plot(tot_id, tot_n_ops, linestyle='-', color='k')
    # twin1.set(ylabel="Number of operations", yscale = "log")
    ax.set_ylim(bottom = 0)
    # plt.text(tot_id[0], tot_n_ops[0], 'Throughput', ha='left')
    plt.xticks([]) 
    # Annotating a point

    # # Add a colorbar to the plot to represent the 'z' variable
    # plt.colorbar(label='Color Variable (z)')
    plt.legend(handles[::-1], labels[::-1])
    #plt.plot(genuine_id, wc_time)
    n = len(filename)
    plt.title("Total lock hold per thread") 
    ratio_string = ""
    for i in ratio:
        ratio_string = ratio_string + str(i) + "_"
    figName = "./graphs/ns_c_fair_list_graphs/applications" + str(applications) + "_ratio_" + ratio_string + "_duration_" + str(duration) + "_total_time.png"
    plt.savefig(figName)          
    plt.close()

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
    # avg_find_time = []
    # for i in range(len(n_entries)):
    #     avg_find_time.append(tot_time[i]/n_entries[i])

    # fig, ax = plt.subplots(1, 2)
    # twin1 = ax[1].twinx()
    # #twin2 = ax.twinx()
    
    # ax[0].bar(insert_id, i_n_entries)

    # #scatter = ax.bar(genuine_id, n_ops)
    # #scatter2 = ax.bar(insert_id, i_n_entries)
    # scatter = ax[1].bar(genuine_id, n_entries)
    # twin1.plot(genuine_id, avg_find_time, color="green", label="Average lock hold time per entry")
    # twin1.plot(genuine_id, find_wc_time, color="red", label="Worst case lock hold time")
    # #plt.ylim(0, 1.1)
    # ax[0].set_xticks(np.arange(0, 1, 1))
    # ax[0].set( ylabel="Number of entries")
    # ax[0].set(xlabel="Thread ID")
    # ax[1].set(xlabel="Thread ID")
    # twin1.set(ylim=(0, max(find_wc_time)), ylabel="Lock hold time")
    # twin1.legend(loc='best')
    # #twin1.yaxis.label.set_color("green")

    # #twin2.set(ylim=(0, max(find_wc_time)), ylabel="Worst Case Lock Hold Time")
    # #twin2.yaxis.label.set_color("red")
    # if (max(genuine_id) == 63):
    #     plt.xticks(np.arange(min(genuine_id), max(genuine_id)+1, 4))  
    # else:
    #     plt.xticks(np.arange(min(genuine_id), max(genuine_id)+1, 2)) 
    # # Annotating a point
    # #plt.text(insert_id[0], i_n_entries[0], 'insert thread', ha='left')

    # # # Add a colorbar to the plot to represent the 'z' variable
    # # plt.colorbar(label='Color Variable (z)')


    # n = len(filename)
    # fig.title("Lock hold time for find operations (CLOUDLAB, basecase, " + str(duration) + "s)") 
    # figName = "./graphs/default_list_graphs/threads" + str(nthreads)  + "_duration " + str(duration) + "_n_entries_CLOUDLAB.png"
    # plt.savefig(figName)          
    # plt.close()