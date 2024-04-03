import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D, HandlerTuple
import numpy as np
import os
import csv
import sys

fig, axs = plt.subplots(3, figsize=(16, 12))

path = "./tables/default_fair_list_tables/"  #FILL THIS IN HERE
fileCount = 0;
for filename in os.listdir(path):
    #print(filename)
    with open(os.path.join(path, filename), 'r') as file:
        if (filename == "new_dynamic_applications.csv"):
            applications = 8

            count = -1
            colours = ['r', 'g', 'b', 'k', 'r', 'g', 'b', 'k']
            ratio = [25, 50, 75, 100, 25, 50, 75, 100]
            reader = csv.reader(file)
            i = -1
            for row in reader:
                stage_1_throughput = []
                stage_2 = []
                stage_3 = []
                app_thoughput = 0
                if i == -1:
                    i = 1
                else:
                    count = count + 1
                    type = row[int(0)]
                    apps = [[0, int(row[1]), int(row[5])], [0, int(row[2]), int(row[6])], [0, int(row[3]), int(row[7]), int(row[15])], [0, int(row[4]), int(row[8]), int(row[16])], [0, int(row[9])], [0, int(row[10])], [0, int(row[11])], [0, int(row[12])]]
                    time_1 = [0, 32, 64, 86]
                    time_2 = [32, 64]
                    time_3 = [0, 32, 64]
                    
                    for j in range(2):
                        print(apps[j])
                        axs[count].plot(time_3, apps[j], label = str(ratio[j]), color=colours[j])

                    for j in [2, 3]:
                        axs[count].plot(time_1, apps[j], label = str(ratio[j]), color=colours[j])

                    for j in [4, 5, 6, 7]:
                        axs[count].plot(time_2, apps[j], label = str(ratio[j]), color=colours[j])


#ax.set_xticks([0, 25, 50, 75, 100])
#x_label = ["100:0", "75:25", "50:50", "25:75", "0:100"]
#ax.set_xticklabels(x_label, fontsize=13)
                    #axs[count].set_ylim(0, 100000)
                    handles, labels = axs[count].get_legend_handles_labels()

                    axs[count].axvline(x = 0, color = 'k', label = 'axvline - full height')
                    axs[count].text(2, max(apps[0]), 'Four threads start',fontsize=13)

                    axs[count].axvline(x = 32, color = 'k', label = 'axvline - full height')
                    axs[count].text(32, max(apps[0]), 'Four more threads start', fontsize=13)

                    axs[count].axvline(x = 64, color = 'k', label = 'axvline - full height')
                    axs[count].text(64, max(apps[0]), 'Six threads stop', fontsize=13)
        
                    by_label = dict(zip(labels, handles))

                    axs[1].legend(by_label.values(), by_label.keys(), loc='upper center', bbox_to_anchor=(1.1, 0.7),
title="Insert Ratio", fancybox=True, shadow=True, fontsize=10)
#plt.title("Total lock hold per thread")
axs[1].set_ylabel("Throughput of application", fontsize=10)#,  yscale = "log")#, #ylim=[1, 10**6])
axs[2].set_xlabel("Time Running", fontsize=10)

plt.tight_layout()

figName = "./graphs/ns_c_lock_fair_list_graphs/new_dynamic_applications.png"
plt.savefig(figName)          
plt.close()