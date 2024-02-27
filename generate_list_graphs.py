import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D, HandlerTuple
import numpy as np
import os
import csv
import sys



path = "./tables/default_fair_list_tables/"  #FILL THIS IN HERE
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
                    wc_time.append(float(row[int(3)]))
                    tot_time.append(float(row[int(4)]))
                    n_ops.append(int(row[int(2)]))
                    lock_opp.append(float(row[int(5)])) 

    print(lock_opp)
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
    counter_four = 0
    new_insert_id = []
    new_find_id = []

    new_i_lock_opp = []
    new_f_find_opp = []

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

    count_one = 0
    count_two = 0
    count_three = 0
    count_four = 0

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


    # total_entries_one = 0
    # total_entries_two = 0
    # total_entries_three = 0
    # total_entries_four = 0
    # for i in range(len(insert_id)):
    #     if insert_id[i] == 0:
    #         total_entries_one = total_entries_one + i_n_entries[i]
    #     if insert_id[i] == 1:
    #         total_entries_two = total_entries_two + i_n_entries[i]
    #     if insert_id[i] == 2:
    #         total_entries_three = total_entries_three + i_n_entries[i]
    #     if insert_id[i] == 3:
    #         total_entries_four = total_entries_four + i_n_entries[i]

    # total_entries = []

    # if total_entries_one != 0:
    #     total_entries.append(total_entries_one)
    # if total_entries_two!= 0:
    #     total_entries.append(total_entries_two)
    # if total_entries_three != 0:
    #     total_entries.append(total_entries_three)
    # if total_entries_four != 0:
    #     total_entries.append(total_entries_four)
    # f_threads = [x - 0.2 for x in genuine_id]
    # i_threads = [x + 0.2 for x in new_insert_id]



    fig, ax = plt.subplots()

    #twin1 = ax.twinx()
    #twin2 = ax.twinx()


    ax.bar(new_find_id, tot_time, width=0.09, color='b', align='center', label = "find")
    ax.bar(new_find_id, lock_opp, width=0.09, color='r', align='center', label = "lock opportunity")
    ax.bar(new_insert_id, i_tot_time, width=0.09, color='g', align='center', label = "insert")
    ax.bar(new_insert_id, i_lock_opp, width=0.09, color='r', align='center')#, label = "insert")

    handles, labels = ax.get_legend_handles_labels()

    # reverse the order
    ax.set(xlabel="Threads", ylabel="Time (ms)",  yscale = "log")    

    #twin1.plot(range(len(total_entries)), total_entries, linestyle='-', color='k')
    #twin1.set(ylabel="Total number of entries", yscale = "log")
    #ax.set_ylim(bottom = 0)
    #plt.text(new_insert_id[0], total_entries[0], 'No. entries', ha='left')
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
    figName = "./graphs/default_fair_list_graphs/applications" + str(applications) + "_ratio_" + ratio_string + "_duration_" + str(duration) + "_total_time.png"
    plt.savefig(figName)          
    plt.close()


