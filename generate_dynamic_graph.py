import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D, HandlerTuple
import numpy as np
import os
import csv
import sys

fig, axs = plt.subplots(3, figsize=(16, 12))
count = 0
path = "./tables/dynamic/"  #FILL THIS IN HERE
fileCount = 0;
for filename in os.listdir(path):
    #print(filename)
    with open(os.path.join(path, filename), 'r') as file:
            type = filename.split('_list')[0]
            print(type)
            colours = ['r', 'g', 'b', 'k', 'r', 'g', 'b', 'k']
            ratio = [1, 2, 3, 2, 3, 2, 1]
            reader = csv.reader(file)
            i = -1
            app_thoughput = []
            temp_app_throughput = []
            final_app_throughput  = [0]
            app_total_time = [0]
            for row in reader:
                if i == -1:
                    i = 1
                else:
                    app_thoughput.append(int(row[1]))
                    #app_thoughput.append(int(row[1]))

                    app_total_time.append(float(row[2]))
                    #app_total_time.append(float(row[2]))

                    time_1 = [16, 16, 32, 32, 48, 48, 64, 64, 80, 80, 96, 96, 112, 112, 128, 128]
            print(app_thoughput)
            for i in range(len(app_thoughput)):
                 if i == 0:
                    temp_app_throughput.append(app_thoughput[i])
                 else:
                    temp_app_throughput.append(app_thoughput[i] - app_thoughput[i-1] + app_thoughput[0])
            #print(temp_app_throughput)
            for i in temp_app_throughput:
                 final_app_throughput.append(i)
                 final_app_throughput.append(i)
            final_app_throughput.append(0)
            print(final_app_throughput)
            axs[count].plot(time_1, final_app_throughput, label = type)

            handles, labels = axs[count].get_legend_handles_labels()

            axs[count].text(time_1[0], final_app_throughput[1] + 100000, 'User 1 begins',fontsize=13)

            #axs[count].axvline(x = 32, color = 'k', label = 'axvline - full height')
            axs[count].text(time_1[3], final_app_throughput[3]+ 100000, 'User 2 begins', fontsize=13)

            #axs[count].axvline(x = 64, color = 'k', label = 'axvline - full height')
            axs[count].text(time_1[5], final_app_throughput[5]+ 100000, 'User 3 begins', fontsize=13)
            axs[count].text(time_1[7], final_app_throughput[7]+ 100000, 'User 3 ends',fontsize=13)

            #axs[count].axvline(x = 32, color = 'k', label = 'axvline - full height')
            axs[count].text(time_1[9], final_app_throughput[9]+ 100000, 'User 4 begins', fontsize=13)

            #axs[count].axvline(x = 64, color = 'k', label = 'axvline - full height')
            axs[count].text(time_1[11], final_app_throughput[11]+ 100000, 'User 4 ends', fontsize=13)
            axs[count].text(time_1[13], final_app_throughput[13]+ 100000, 'User 2 ends', fontsize=13)   
            axs[count].text(time_1[15], final_app_throughput[15]+ 100000, 'User 1 ends', fontsize=13)     
            #by_label = dict(zip(labels, handles))
            axs[count].set_ylim([1, max(final_app_throughput) + 100000 + 100000])
            axs[count].set_yticks([1000000, 2000000, 3000000, 4000000])
            #ylabels = ["1M", "2M", "3M", "4M"]
            axs[count].set_yticklabels(["1M", "2M", "3M", "4M"])
            list=["a) Default", "b) Fair", "c) Performance Fair"]
            axs[count].set_title(list[count]+ " linked list", fontsize=15)
            #axs[count].legend(by_label.values(), by_label.keys(), loc='upper center', bbox_to_anchor=(1.1, 0.7), title="Insert Ratio", fancybox=True, shadow=True, fontsize=10)

            count += 1
            print(count)#plt.title("Total lock hold per thread")
            axs[1].set_ylabel("Throughput of application", fontsize=13)#,  yscale = "log")#, #ylim=[1, 10**6])
            axs[2].set_xlabel("Time Running", fontsize=13)

plt.tight_layout()

figName = "./graphs/ns_c_lock_fair_list_graphs/new_dynamic_applications.png"
plt.savefig(figName)          
plt.close()