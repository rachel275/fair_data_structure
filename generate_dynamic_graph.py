import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D, HandlerTuple
import numpy as np
import os
import csv
import sys

fig, axs = plt.subplots(3, figsize=(16, 12))

path = "./tables/dynamic/"  #FILL THIS IN HERE
fileCount = 0;
for filename in os.listdir(path):
    #print(filename)
    with open(os.path.join(path, filename), 'r') as file:
            type = filename.split('_list')[0]
            print(type)
            count = -1
            colours = ['r', 'g', 'b', 'k', 'r', 'g', 'b', 'k']
            ratio = [1, 2, 3, 2, 3, 2, 1]
            reader = csv.reader(file)
            i = -1
            for row in reader:
                app_thoughput = [0]
                app_total_time = [0]
                if i == -1:
                    i = 1
                else:
                    app_thoughput.append(int(row[1]))
                    app_thoughput.append(int(row[1]))

                    app_total_time.append(int(row[2]))
                    app_total_time.append(int(row[2]))

                    time_1 = [0, 16, 16, 32, 32, 48, 48, 64, 64, 80, 80, 96, 96, 112, 112, 138, 138]
                    
                    print(app_thoughput)
                    axs[count].plot(time_1, app_thoughput, label = type)



                    handles, labels = axs[count].get_legend_handles_labels()


                    axs[count].text(time_1[0], max(app_thoughput), 'User 1 begins',fontsize=13)

                    #axs[count].axvline(x = 32, color = 'k', label = 'axvline - full height')
                    axs[count].text(time_1[2], max(app_thoughput), 'User 2 begins', fontsize=13)

                    #axs[count].axvline(x = 64, color = 'k', label = 'axvline - full height')
                    axs[count].text(time_1[4], max(app_thoughput), 'User 3 begins', fontsize=13)
                    axs[count].text(time_1[6], max(app_thoughput), 'User 3 ends',fontsize=13)

                    #axs[count].axvline(x = 32, color = 'k', label = 'axvline - full height')
                    axs[count].text(time_1[8], max(app_thoughput), 'User 4 begins', fontsize=13)

                    #axs[count].axvline(x = 64, color = 'k', label = 'axvline - full height')
                    axs[count].text(time_1[10], max(app_thoughput), 'User 4 ends', fontsize=13)
                    axs[count].text(time_1[12], max(app_thoughput), 'User 2 ends', fontsize=13)   
                    axs[count].text(time_1[14], max(app_thoughput), 'User 1 ends', fontsize=13)     
                    by_label = dict(zip(labels, handles))

                    count+= 1

                    axs[1].legend(by_label.values(), by_label.keys(), loc='upper center', bbox_to_anchor=(1.1, 0.7),
title="Insert Ratio", fancybox=True, shadow=True, fontsize=10)
#plt.title("Total lock hold per thread")
axs[1].set_ylabel("Throughput of application", fontsize=10)#,  yscale = "log")#, #ylim=[1, 10**6])
axs[2].set_xlabel("Time Running", fontsize=10)

plt.tight_layout()

figName = "./graphs/ns_c_lock_fair_list_graphs/new_dynamic_applications.png"
plt.savefig(figName)          
plt.close()