import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D, HandlerTuple
import numpy as np
import os
import csv
import sys

final_data = []

path = "./tables/default_fair_list_tables/"  #FILL THIS IN HERE
fileCount = 0;
for filename in os.listdir(path):
    print(filename)
    if filename == "performance.csv":
        continue
    with open(os.path.join(path, filename), 'r') as file:
        applications = int(filename.split('_')[1]) 
        ratio = []
        for i in range(applications):
            ratio.append(int(filename.split('_')[i + 3]))
        if applications == 2:
            duration = filename.split('_')[i + 5]
            i = -1
            reader = csv.reader(file)
            no_threads = []
            thread_type = []
            insert_id = 0
            find_id = 0
            tot_time = 0
            i_tot_time = 0
            n_ops = 0
            i_n_ops = 0
            app_tot_time = 0
            app_i_tot_time = 0
            app_n_ops = 0
            app_i_n_ops = 0
            for row in reader:
                if i == -1:
                    i = 1
                else:
                    if (row[int(0)] == "insert"):
                        if (int(row[int(1)]) == 0):
                            i_tot_time += (float(row[int(4)]))
                            i_n_ops += (int(row[int(2)]))
                        else:
                            app_i_tot_time += (float(row[int(4)]))
                            app_i_n_ops += (int(row[int(2)]))
                    else:
                        if (int(row[int(1)]) == 0):
                            tot_time += (float(row[int(4)]))
                            n_ops += (int(row[int(2)]))
                        else:
                            app_tot_time += (float(row[int(4)]))
                            app_n_ops += (int(row[int(2)]))
            ratio_string = ""
            for i in ratio:
                ratio_string = ratio_string + str(i) + "_"
            data = [ratio_string, tot_time, n_ops, i_tot_time, i_n_ops, app_tot_time, app_n_ops, app_i_tot_time, app_i_n_ops]
            final_data.append(data)
    
f = open("./tables/default_fair_list_tables/applications_2_total.csv", 'a+', newline="")
writer = csv.writer(f)
header = ["ratios", "Find Throughput", "Find n_operations","Insert throughput", "insert n_operations", "Find Throughput", "Find n_operations","Insert throughput", "insert n_operations"]
writer.writerow(header)
writer.writerow(final_data)
f.close()
