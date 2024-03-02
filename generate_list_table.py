import os
import sys
import csv
import re
import statistics
from scipy.stats import skew
from scipy.stats import kurtosis

#rowInfo = {}
#rowNum = 0
data = []
def findnth(haystack, needle, n):
    parts = haystack.split(needle, n+1)
    if len(parts) <= n + 1:
        return -1
    return len(haystack) - len(parts[-1]) - len(needle)

def find_info(text, mode):
    startIndex = 0
    endIndex = 0
    if mode == 0:
        startIndex = findnth(text, ":", 3) + 1
        endIndex = findnth(text, "/", 3)
    elif mode == 1:
        startIndex = findnth(text, ":", 1) + 1
        endIndex = findnth(text, "/", 1)
    elif mode == 2:
        startIndex = findnth(text, " ", 4) + 1
        endIndex = len(text)
    elif mode == 3:
        startIndex = findnth(text, " ", 2) 
        endIndex = findnth(text, ")", 0)
    elif mode == 4:
        startIndex = findnth(text, ":", 2) + 1
        endIndex = findnth(text, "/", 2)
    elif mode == 5:
        startIndex = findnth(text, ":", 0) + 1
        endIndex = findnth(text, "/", 0)
    #this one is for finding the thread number of this execution
    elif mode == 5:
        startIndex = findnth(text, ":", 0) + 1
        endIndex = findnth(text, "/", 0)
    else:
        startIndex = findnth(text, ":", 0) + 2
        endIndex = len(text)
    return text[startIndex:endIndex]

def find_outliers_num(dataset, avg, sd):
    outlierCount = 0
    for data in dataset:
        if data >= (sd * 2 + avg):
            outlierCount += 1
        elif data <= (avg - sd * 2):
            outlierCount += 1
    return outlierCount

def write_to_table(applications, ratio, duration, type):
    ratio_string = ""
    print(ratio)
    for i in ratio:
        ratio_string = ratio_string + str(i) + "_"
    print(ratio_string)
    f = open("./tables/" + type + "_list_tables/applications_" + str(applications) + "_ratio_" + ratio_string + "duration_" + str(duration) + ".csv", 'a+', newline="")
    writer = csv.writer(f)
    header = ["Type of thread", "Thread Id","Number of Operations", "Worst Case Time", "LHT Time", "Lock Opportunity"]
    writer.writerow(header)
    writer.writerows(data)
    f.close()

def sort_data():
    n = len(data)
    swapped = False
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if data[j][0] > data[j + 1][0]:
                swapped = True
                data[j], data[j + 1] = data[j + 1], data[j]
            if data[j][0] == data[j + 1][0]:
                if int(data[j][1]) > int(data[j + 1][1]):   #add [:-1] back to each for Duration
                    swapped = True
                    data[j], data[j + 1] = data[j + 1], data[j]
        # if not swapped:
        #     return
        
def sort_thread_data():
    n = len(threadOrder)
    swapped = False
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if threadOrder[j] > threadOrder[j + 1]:
                swapped = True
                threadOrder[j], threadOrder[j + 1] = threadOrder[j + 1], threadOrder[j]
                executions[j], executions[j + 1] = executions[j + 1], executions[j]
            elif threadOrder[j] == threadOrder[j + 1]:
                if threadOrder[j] > threadOrder[j + 1]:
                    swapped = True
                    threadOrder[j], threadOrder[j + 1] = threadOrder[j + 1], threadOrder[j]
                    executions[j], executions[j + 1] = executions[j + 1], executions[j]
        if not swapped:
            return

def sort_again():
    n = len(data)
    for i in range(2, n, 4):
        temp = data[i]
        data.insert(i - 2, temp)
        data.pop(i + 1)


rootdir = "./data/"
for dir in os.listdir(rootdir):
        if dir.split('_')[-2] == "fair":
            type = dir.split('_list')[0]
            for filename in os.listdir("./data/" + dir):
                with open(os.path.join("./data/" + dir, filename), 'r') as file:
                    data = []
                    if ((filename.endswith("_exp_0")) == False): # or (filename.endswith("_basecase_CLOUDLAB") == True )):
                        file.close()
                        continue
                    ratio = []
                    applications = int(filename.split('_')[1])#find_info(information, 1).lstrip().rstrip()
                    for i in range(applications):
                        ratio.append(int(filename.split('_')[i + 3]))
                    duration = filename.split('_')[i + 5]
            #thread type, thread id, number of operations, number of entries, total cs time, worst case critical section time.
                    text_line = file.readline()
                    while text_line:
                        text = text_line.split('/')
                        thread_type = text[0].split(' ')[0]

                        if (thread_type == "id:"):
                            thread_type = text[0].split(' ')[0]
                        thread_id = int(text[0].split(':')[-1]) #int(find_info(text, 1).lstrip().rstrip())
                        no_ops = int(text[1].split(':')[-1]) #int(find_info(text, 1).lstrip().rstrip())
                        total_time = float(text[2].split(':')[-1]) #find_info(text, 1).lstrip().rstrip()
                        wc_time= float(text[3].split(':')[-1])

                        text_line = file.readline()
                        text = text_line.split('/')
                        print(text[0].split(' '))

                        lock_opportunity = float(text[0].split(' ')[3])


                        data.append([thread_type, thread_id, no_ops, wc_time, total_time, lock_opportunity])
                        text_line = file.readline()
                    
                    sort_data()
                    write_to_table(applications, ratio, duration, type)
                    file.close()
        #print("close this file ")
        # sort_data()
        # sort_again()
        #write_to_table()
        #print("There are " + str(why) + " files!")	
        #print("next directory ")