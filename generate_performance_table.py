import os
import sys
import csv
import re
import statistics
from scipy.stats import skew
from scipy.stats import kurtosis

#rowInfo = {}
#rowNum = 0

no_applications = [2, 4, 8, 10]
ratios = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
throughput = [[[], []], [[], [], [], []], [[], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], []]]
data = []
def write_to_table(applications, ratio, duration, type):
    f = open("./tables/default_fair_hash_tables/performance.csv", 'a+', newline="")
    writer = csv.writer(f)
    for i in range(len(no_applications)):
        temp = []
        temp.append(no_applications[i])
        temp.extend(throughput[i])
        data.append(temp)
        print(data)
    writer.writerows(data)
    f.close()

# def sort_data():
#     n = len(data)
#     swapped = False
#     for i in range(n - 1):
#         for j in range(0, n - i - 1):
#             if data[j][0] > data[j + 1][0]:
#                 swapped = True
#                 data[j], data[j + 1] = data[j + 1], data[j]
#             if data[j][0] == data[j + 1][0]:
#                 if int(data[j][1]) > int(data[j + 1][1]):   #add [:-1] back to each for Duration
#                     swapped = True
#                     data[j], data[j + 1] = data[j + 1], data[j]
#         # if not swapped:
#         #     return
        

# def sort_again():
#     n = len(data)
#     for i in range(2, n, 4):
#         temp = data[i]
#         data.insert(i - 2, temp)
#         data.pop(i + 1)


rootdir = "./data/"
for dir in os.listdir(rootdir):
    type = dir.split('_hash')[0]
    if type == "default_fair":
        for filename in os.listdir("./data/" + dir):
            with open(os.path.join("./data/" + dir, filename), 'r') as file:
                ratio = []
                no_ops = 0
                count = 0
                applications = int(filename.split('_')[3])
                for i in range(applications):
                    ratio_val = int(filename.split('_')[i + 5])
                    if (ratio_val == 100):
                        count += 1
                    ratio.append(ratio_val)
                if(applications == 1):
                    print("ignore this file")
                elif(applications == 2):
                    print("2 apps but no")
                else:
                    duration = filename.split('_')[i + 7]
                    #print(ratio)
                    text_line = file.readline()
                    no_ops = []
                    while text_line:
                        #print(text_line.split(' '))
                        if ((text_line.split(' ')[0] == "Lock_Opp_b_0:") or (not text_line) or (text_line == " ")or (text_line == "\n")):
                            print("ignore")
                            #do nothing with this line
                        else:
                            text = text_line.split('/')
                            thread_type = text[0].split(' ')[0]
                            if (thread_type == "id:"):
                                thread_type = text[0].split(' ')[0]
                            if thread_type == "find":
                                no_ops.append(int(text[1].split(':')[-1])) #int(find_info(text, 1).lstrip().rstrip()
                            #text_line = file.readline()

                        text_line = file.readline()
                        #print(text_line)
                    if (applications == 2):
                        throughput[0][count].append(no_ops)
                        #print(throughput[0][count])
                    elif (applications == 4):
                        throughput[1][count].append(no_ops)
                        #print(throughput[1][count])
                    elif (applications == 8):
                        throughput[2][count].append(no_ops)
                        #print(throughput[2][count])
                    elif (applications == 10):
                        throughput[3][count].append(no_ops)
                        #print(throughput[3][count])
# for i in range(len(no_applications)):
#     temp = []
#     temp.append(no_applications[i])
#     temp.extend(throughput[i])
#     data.append(temp)
#     print(temp)
write_to_table(applications, ratio, duration, type)
file.close()
