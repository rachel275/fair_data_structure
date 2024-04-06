import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D, HandlerTuple
import numpy as np
import os
import csv
import sys


rootdir = "./data/dynamic"

for filename in os.listdir(rootdir):
    final_data = []
    with open(os.path.join(rootdir, filename), 'r') as file:
        type = filename.split('_linked_list')[0]
        print(type)
        applications = 8
        ratio = [2, 4, 6, 4, 6, 4, 2]
        throughput = 0 #[0, 0, 0, 0, 0, 0, 0]
        total_cs = 0#[0, 0, 0, 0, 0, 0, 0]
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
        for t in range(len(ratio)):
            for i in range(ratio[t]):
                text_line = file.readline()
                # if ((text_line.split(' ')[0] == "Spin_Lock_Opp:") or (not text_line) or (text_line == " ")or (text_line == "\n")):
                #     print("ignore")
                #     #do nothing with this line
                # else:
                text = text_line.split('/')
                thread_type = text[0].split(' ')[0]
                if (thread_type == "id:"):
                    thread_type = text[0].split(' ')[0]
                if (thread_type == 'find'):
                    thread_id = int(text[0].split(':')[-1]) #int(find_info(text, 1).lstrip().rstrip())
                    no_ops = int(text[1].split(':')[-1]) #int(find_info(text, 1).lstrip().rstrip())
                    total_time = float(text[2].split(':')[-1]) #find_info(text, 1).lstrip().rstrip()
                    throughput += no_ops
                    total_cs += total_time
            
            final_data.append([type, throughput , total_cs])

        
        f = open("./tables/dynamic/" + str(type) + "_linked_list.csv", 'a+', newline="")
        writer = csv.writer(f)
        header = ["Type", "throughput", "total_cs"]
        writer.writerow(header)
        writer.writerow(final_data)
        f.close()
