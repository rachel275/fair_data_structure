import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D, HandlerTuple
import numpy as np
import os
import csv
import sys



fig, ax = plt.subplots(figsize=(12,9))


colours = ['b', 'r', 'g']
count = 0
max_4 = 0
min_4 = 10000000000000
max_8 = 0
min_8 = 10000000000000
max_10 = 0
min_10 = 10000000000000
path = "./tables/default_fair_hash_tables/"  #FILL THIS IN HERE
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
                        #print(max_10)
                    if (min(y_val) < min_10):
                        min_10 = min(y_val)
                        #print(min_10)
                count = len(x_val)
                denom = 4 * applications
                #ax.plot(x_val, y_val, color=v_colour, label=str(applications))

difference_4 = max_4 / min_4
diff_8 = max_8 / min_8
diff_10 = max_10 / min_10
diff = [difference_4, diff_8, diff_10]
maxx = [max_4, max_8, max_10]
print(diff)
#ax.axhspan(max_4, min_4, facecolor='b', alpha=0.5)
#ax.axhspan(min_8, max_8, facecolor='r', alpha=0.5)
#ax.axhspan(min_10, max_10, facecolor='g', alpha=0.5)
colours = ['b', 'r', 'g']
count = 0
o_max_4 = 0
o_min_4 = 10000000000000
o_max_8 = 0
o_min_8 = 10000000000000
o_max_10 = 0
o_min_10 = 10000000000000
path = "./tables/ns_c_fair_hash_tables/"  #FILL THIS IN HERE
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
                        #print(o_max_10)
                    if (min(y_val) < o_min_10):
                        o_min_10 = min(y_val)
                        #print(o_min_10)
                count = len(x_val)
                denom = 4 * applications
                #ax.plot(x_val, y_val, color=v_colour, label=str(applications))

o_difference_4 = o_max_4 / o_min_4
o_diff_8 = o_max_8 / o_min_8
o_diff_10 = o_max_10 / o_min_10
o_diff = [o_difference_4, o_diff_8, o_diff_10]
o_max = [o_max_4, o_max_8, o_max_10]


#print(diff)
print(o_diff)


#ax.axhspan(max_4, min_4, facecolor='b', alpha=0.5)
#ax.axhspan(min_8, max_8, facecolor='r', alpha=0.5)
#ax.axhspan(min_10, max_10, facecolor='g', alpha=0.5)
colours = ['b', 'r', 'g']
count = 0
i_max_4 = 0
i_min_4 = 10000000000000
i_max_8 = 0
i_min_8 = 10000000000000
i_max_10 = 0
i_min_10 = 10000000000000
path = "./tables/ns_c_lock_fair_hash_tables/"  #FILL THIS IN HERE
fileCount = 0;
filename = "performance.csv"
with open(os.path.join(path, filename), 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        applications = int(row[0])
        #print(row)
        #print(row[0])
        if (applications != 2):
            throughput = []
            #print(applications)
            for i in range(applications):
                x_val = []
                y_val = []
                ratio_max = 0
                ratio_min = 0
                #print(row[i+1])
                values = row[i + 1].split('],')
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
                    if (max(y_val) > i_max_4):
                        i_max_4 = max(y_val)
                    if (min(y_val) < i_min_4):
                        i_min_4 = min(y_val)
                elif (applications == 8):
                    v_colour = 'r'
                    if (max(y_val) > i_max_8):
                        i_max_8 = max(y_val)
                    if (min(y_val) < i_min_8):
                        i_min_8 = min(y_val)
                elif(applications == 10):
                    v_colour = 'g'
                    if (max(y_val) > i_max_10):
                        i_max_10 = max(y_val)
                        #print(i_max_10)
                    if (min(y_val) < i_min_10):
                        i_min_10 = min(y_val)
                        #print(i_min_10)
                count = len(x_val)
                denom = 4 * applications
                #ax.plot(x_val, y_val, color=v_colour, label=str(applications))

i_difference_4 = i_max_4 / i_min_4
i_diff_8 = i_max_8 / i_min_8
i_diff_10 = i_max_10 / i_min_10
#print(i_max_8)
#print(i_min_8)
i_diff = [i_difference_4, i_diff_8, i_diff_10]
i_max = [i_max_4, i_max_8, i_max_10]
print(i_diff)

print([min_4, min_8, min_10])
print([max_4,max_8, max_10])
print([o_min_4, o_min_8, o_min_10])
print([o_max_4,o_max_8, o_max_10])
print([i_min_4, i_min_8, i_min_10])
print([i_max_4,i_max_8, i_max_10])


ax.set_ylabel("Max throughput", fontsize=15)
ax.set_xlabel("Number of applications running", fontsize=15)
x_val= [0.66, 1.66, 2.66]
#x_val = [0.75, 1.75, 2.75]
#ax.set_yscale('log')
o_x_val = [1, 2, 3]
i_x_val = [1.33, 2.33, 3.33]
ax.bar(x_val, maxx, width=0.3, color='b', label = "Default linked list")
ax.bar(o_x_val, o_max, width=0.3, color='r', label="Fair linked list")
ax.bar(i_x_val, i_max, width=0.3, color='g', label="Performance fair linked list")
#ax.set_yscale('log')
ax.set_ylim([1, max(maxx) + 3000])
ax.set_xticks([1, 2, 3])
xlabels = ["4", "8", "10"]
#xlabels = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
ax.set_xticklabels(xlabels)
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys(), loc='upper center', bbox_to_anchor=(0.5, 0.09),
       fancybox=True, shadow=True, fontsize=15, ncol=3)
#plt.tight_layout()
ratio_string = ""
figName = "./graphs/ns_c_fair_hash_graphs/max_combined.png"
plt.savefig(figName)          
plt.close()


