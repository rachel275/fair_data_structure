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

def write_to_table(threads, duration, type,  iratio, fratio, dratio):
    f = open("./tables/" + type + "_list_tables/threads_" + str(threads) + "_duration_" + str(duration) + "_ratio_" + str(iratio) + "," + str(fratio) + "," + str(dratio) + "_CLOUDLAB.csv", 'a+', newline="")
    writer = csv.writer(f)
    header = ["Type of thread", "Thread Id","Number of Operations", "Number of Entries", "Worst Case Time", "Total Time"]
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
        if dir.split('_')[-1] == "list":
            type = dir.split('_list')[0]
            for filename in os.listdir("./data/" + dir):
                with open(os.path.join("./data/" + dir, filename), 'r') as file:
                    data = []
                    if (filename.endswith("_CLOUDLAB") == False):
                        file.close()
                        continue
                    # information = file.readline()
                    # #find this information from the file name
                    nthreads = filename.split('_')[0].split("nthreads")[-1]#find_info(information, 1).lstrip().rstrip()
                    duration = filename.split('_')[1].split("duration")[-1]
                    ratios = filename.split('_')[2].split('ratio')[1]
                    iratio = ratios.split(",")[0]
                    fratio = ratios.split(",")[1]
                    dratio = ratios.split(",")[2]
                    #print(ratios + "\n")
                    #print(iratio + " " + fratio + " " + dratio + "\n")
                    # duration = int(filename.split('_')[2].split("duration")[-1]) #find_info(information, 1).lstrip().rstrip()

            #thread type, thread id, number of operations, number of entries, total cs time, worst case critical section time.
                    threadNum = int(nthreads) + 1
                    for i in range(threadNum):
                        text = file.readline().split('/')
                        thread_type = text[0].split(' ')[1]
                        if (thread_type == "id:"):
                            thread_type = text[0].split(' ')[0]
                        #bucket_id = int(text[0].split(' ')[0])
                        thread_id = int(text[0].split(':')[-1]) #int(find_info(text, 1).lstrip().rstrip())
                        #wc_time = float(text[1].split(':')[-1])
                        no_ops = int(text[1].split(':')[-1]) #int(find_info(text, 1).lstrip().rstrip())
                        #thread_bucket_id.append(bucket_id)
                        no_entries= int(text[2].split(':')[-1])#(find_info(text, 1).lstrip().rstrip())
                        #thread_wc_time.append(wc_time)
                        total_time = float(text[3].split(':')[-1]) #find_info(text, 1).lstrip().rstrip()
                        #thread_total_time.append(total_time)
                        wc_time= float(text[4].split(':')[-1])
                        #bucket_execution= int(text[4].split(':')[-1])#(find_info(text, 1).lstrip().rstrip())
                        #thread_executions.append(thread_execution)

                        #sd = round(statistics.stdev(thread_executions), 2)

                        data.append([thread_type, thread_id, no_ops, no_entries, wc_time, total_time])
                    
                    sort_data()
                    #sort_again()
                    write_to_table(nthreads, duration, type, iratio, fratio, dratio)
                    file.close()
                #print("close this file ")
            # sort_data()
            # sort_again()
            #write_to_table()
            #print("There are " + str(why) + " files!")	
        #print("next directory ")