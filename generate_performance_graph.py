import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D, HandlerTuple
import numpy as np
import os
import csv
import sys



fig, ax = plt.subplots(figsize=(7,7))


colours = ['b', 'r', 'g']
count = 0
max_4 = 0
min_4 = 10000000000000
max_8 = 0
min_8 = 10000000000000
max_10 = 0
min_10 = 10000000000000
o_max_4 = 0
o_min_4 = 10000000000000
o_max_8 = 0
o_min_8 = 10000000000000
o_max_10 = 0
o_min_10 = 10000000000000
path = "./tables/default_fair_list_tables/"  #FILL THIS IN HERE
fileCount = 0;
filename = "performance.csv"
with open(os.path.join(path, filename), 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        applications = int(row[0])
        if (applications != 2):
            throughput = []
            for i in range(applications):
                x_val = []
                y_val = []
                values = row[i+1].split('],')
                #print(values)
#                for i in values:
                val = values[0].split(',')
                #print(val)
                for j in val:
                    res = j.replace("]", "")
                    res2 = res.replace("[", "")
                    y_val.append(int(res2))
                x_val = [i for i in range(len(val))]
                #print(x_val)
                #print(y_val)
                if (applications == 4):
                    v_colour = 'b'
                    if (max(y_val) > max_4):
                        max_4 = max(y_val)
                    if (min(y_val) < min_4):
                        min_4 = min(y_val)
                elif (applications == 8):
                    v_colour = 'r'
                    if (max(y_val) > max_8):
                        max_8 = max(y_val)
                    if (min(y_val) < min_8):
                        min_8 = min(y_val)
                elif(applications == 10):
                    v_colour = 'g'
                    if (max(y_val) > max_10):
                        max_10 = max(y_val)
                        print(max_10)
                    if (min(y_val) < min_10):
                        min_10 = min(y_val)
                        print(min_10)
                count = len(x_val)
                denom = 4 * applications
                #ax.plot(x_val, y_val, color=v_colour, label=str(applications))

difference_4 = max_4 - min_4
diff_8 = max_8 - min_8
diff_10 = max_10 - min_10
diff = [difference_4, diff_8, diff_10]
print(diff)
#ax.axhspan(max_4, min_4, facecolor='b', alpha=0.5)
#ax.axhspan(min_8, max_8, facecolor='r', alpha=0.5)
#ax.axhspan(min_10, max_10, facecolor='g', alpha=0.5)
colours = ['b', 'r', 'g']
count = 0
max_4 = 0
min_4 = 10000000000000
max_8 = 0
min_8 = 10000000000000
max_10 = 0
min_10 = 10000000000000
o_max_4 = 0
o_min_4 = 10000000000000
o_max_8 = 0
o_min_8 = 10000000000000
o_max_10 = 0
o_min_10 = 10000000000000
path = "./tables/ns_c_fair_list_tables/"  #FILL THIS IN HERE
fileCount = 0;
filename = "performance.csv"
with open(os.path.join(path, filename), 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        applications = int(row[0])
        if (applications != 2):
            throughput = []
            for i in range(applications):
                x_val = []
                y_val = []
                values = row[i+1].split('],')
                #print(values)
#                for i in values:
                val = values[0].split(',')
                #print(val)
                for j in val:
                    res = j.replace("]", "")
                    res2 = res.replace("[", "")
                    y_val.append(int(res2))
                x_val = [i for i in range(len(val))]
                #print(x_val)
                #print(y_val)
                if (applications == 4):
                    v_colour = 'b'
                    if (max(y_val) > o_max_4):
                        o_max_4 = max(y_val)
                    if (min(y_val) < o_min_4):
                        o_min_4 = min(y_val)
                elif (applications == 8):
                    v_colour = 'r'
                    if (max(y_val) > o_max_8):
                        o_max_8 = max(y_val)
                    if (min(y_val) < o_min_8):
                        o_min_8 = min(y_val)
                elif(applications == 10):
                    v_colour = 'g'
                    if (max(y_val) > o_max_10):
                        o_max_10 = max(y_val)
                        print(o_max_10)
                    if (min(y_val) < o_min_10):
                        o_min_10 = min(y_val)
                        print(o_min_10)
                count = len(x_val)
                denom = 4 * applications
                #ax.plot(x_val, y_val, color=v_colour, label=str(applications))

o_difference_4 = o_max_4 - o_min_4
o_diff_8 = o_max_8 - o_min_8
o_diff_10 = o_max_10 - o_min_10
o_diff = [o_difference_4, o_diff_8, o_diff_10]
o_max = [o_max_4, o_max_8, o_max_10]


print(diff)
print(o_diff)

ax.set_ylabel("Max-min throughput difference", fontsize=15)
ax.set_xlabel("Number of applications running", fontsize=15)
x_val= [0.75, 1.75, 2.75]
o_x_val = [1.25, 2.25, 3.25]
ax.bar(x_val, diff, width=0.4, color='b', label = "Default linked list")
ax.bar(o_x_val, o_diff, width=0.4, color='r', label="Fair linked list")
#ax.set_yscale('log')
ax.set_ylim([1, max(diff) + 1000])
ax.set_xticks([1, 2, 3])
xlabels = ["4", "8", "10"]
#xlabels = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
ax.set_xticklabels(xlabels)
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys(), loc='upper center', bbox_to_anchor=(0.8, 0.9),
       fancybox=True, shadow=True, fontsize=15, ncol=1)
#plt.tight_layout()
ratio_string = ""
figName = "./graphs/default_fair_list_graphs/performance_combined.png"
plt.savefig(figName)          
plt.close()


