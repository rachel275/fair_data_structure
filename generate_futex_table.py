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

def write_to_table(threads, buckets):
    f = open("./tables/futex_example_tables/buckets_threads_" + str(threads) + "_buckets_" + str(buckets) + "_CLOUDLAB.csv", 'a+', newline="")
    writer = csv.writer(f)
    header = ["Type of thread", "Thread Id", "Total Time", "Worst Case Bucket", "Worst Case Time", "Number of Operations"]
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

path = "./data/futex_hashtable_example"
fileCount = 0
for filename in os.listdir(path):
    with open(os.path.join(path, filename), 'r') as file:
        data = []
        # information = file.readline()
        # #find this information from the file name
        if (filename.endswith("_CLOUDLAB") == False or filename.split('_')[0] != "bucket"):
            file.close()
            continue
        else:
            nthreads = filename.split('_')[1].split("nfutex")[-1]#find_info(information, 1).lstrip().rstrip()
            malthreads = filename.split('_')[2].split("ninsert")[-1] #find_info(information, 1).lstrip().rstrip()
        # duration = int(filename.split('_')[2].split("duration")[-1]) #find_info(information, 1).lstrip().rstrip()
            buckets = int(filename.split('_')[4].split("buckets")[-1]) #find_info(information, 1).lstrip().rstrip()

#bucket id, worst case lock hold, total lock hold, no_entries, no_operations
        threadNum = int(nthreads) + int(malthreads)
        for i in range(threadNum):
            text = file.readline().split('/')
            thread_type = text[0].split(' ')[0]
            #bucket_id = int(text[0].split(' ')[0])
            thread_id = int(text[0].split(':')[-1]) #int(find_info(text, 1).lstrip().rstrip())
            #wc_time = float(text[1].split(':')[-1])
            bucket_id = int(text[1].split(':')[-1]) #int(find_info(text, 1).lstrip().rstrip())
            #thread_bucket_id.append(bucket_id)
            thread_wc_time= float(text[2].split(':')[-1])#(find_info(text, 1).lstrip().rstrip())
            #thread_wc_time.append(wc_time)
            thread_total_time = float(text[3].split(':')[-1]) #find_info(text, 1).lstrip().rstrip()
            #thread_total_time.append(total_time)
            thread_entries= int(text[4].split(':')[-1])
            #thread_execution= int(text[4].split(':')[-1])#(find_info(text, 1).lstrip().rstrip())
            #thread_executions.append(thread_execution)

            #sd = round(statistics.stdev(thread_executions), 2)

            data.append([thread_type, thread_id, thread_total_time, thread_wc_time, bucket_id, thread_entries])
        
        sort_data()
        #sort_again()
    write_to_table(nthreads, buckets)
    file.close()
# sort_data()
# sort_again()
#write_to_table()
#print("There are " + str(why) + " files!")	
