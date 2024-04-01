import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D, HandlerTuple
import numpy as np
import os
import csv
import sys

final_data = []

rootdir = "./data/"
for dir in os.listdir(rootdir):
    type = dir.split('_list')[0]
    print(type)
    for filename in os.listdir("./data/" + dir):
        with open(os.path.join("./data/" + dir, filename), 'r') as file:
            if filename == "dynamic_applications":
                applications = 8
                ratio = [25, 50, 75, 100, 25, 50, 75, 100]
                applications_tot_throughput = [0, 0, 0, 0, 0, 0, 0, 0]
                applications_tot_time = [0, 0, 0, 0, 0, 0, 0, 0]
                duration = 86
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
                text_line = file.readline()
                while text_line:
                    if ((text_line.split(' ')[0] == "Spin_Lock_Opp:") or (not text_line) or (text_line == " ")or (text_line == "\n")):
                        print("ignore")
                        #do nothing with this line
                    else:
                        text = text_line.split('/')
                        thread_type = text[0].split(' ')[0]
                        if (thread_type == "id:"):
                            thread_type = text[0].split(' ')[0]
                        if (thread_type == 'find'):
                            thread_id = int(text[0].split(':')[-1]) #int(find_info(text, 1).lstrip().rstrip())
                            no_ops = int(text[1].split(':')[-1]) #int(find_info(text, 1).lstrip().rstrip())
                            total_time = float(text[2].split(':')[-1]) #find_info(text, 1).lstrip().rstrip()
                            applications_tot_throughput[thread_id] += no_ops
                            applications_tot_time[thread_id] += tot_time
                    text_line = file.readline()
                    #text_line = file.readline()     
                final_data.append([type] + applications_tot_throughput + applications_tot_time)

        
f = open("./tables/default_fair_list_tables/dynamic_applications.csv", 'a+', newline="")
writer = csv.writer(f)
header = ["Type", "throughput 1", "throughput 1", "throughput 1", "throughput 1", "throughput 1", "throughput 1", "throughput 1", "throughput 1", "time 1", "time 1","time 1","time 1","time 1","time 1","time 1","time 1"]
writer.writerow(header)
writer.writerow(final_data)
f.close()
