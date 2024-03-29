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


base_case = []

rootdir = "./tables/"
for dir in os.listdir(rootdir):
    type = dir.split('_list_tables')[0]
    if (type.__contains__("default_fair")):
        for filename in os.listdir("./tables/" + dir):
            with open(os.path.join("./tables/" + dir, filename), 'r') as file:
                    if(int(filename.split('_')[1]) == 1):#find_info(information, 1).lstrip().rstrip()
                        ratio = int(filename.split('_')[3])
                        lines = file.read().splitlines()
                        for line in lines:
                            if (line.split('/')[0].split(' ')[0] == "Find"):
                                text = line.split('/')
                                no_ops = int(text[1].split(':')[-1]) #int(find_info(text, 1).lstrip().rstrip())
                                base_case[ratio] += no_ops
                            


for dir in os.listdir(rootdir):
    type = dir.split('_list')[0]
    for type in ['default_fair', 'ns_c_fair', 'nc_c_lock_fair']:
        for filename in os.listdir("./data/" + dir):
            with open(os.path.join("./data/" + dir, filename), 'r') as file:
                data = []
                ratio = []

                applications = int(filename.split('_')[1])#find_info(information, 1).lstrip().rstrip()
                if (applications > 1):
                    for i in range(applications):
                        ratio.append(int(filename.split('_')[i + 3]))
                    duration = filename.split('_')[i + 5]
                    text_line = file.readline()
                    while text_line:
                        #print(text_line.split(' '))
                        if ((text_line.split(' ')[0] == "Spin_Lock_Opp:") or (not text_line) or (text_line == " ")or (text_line == "\n")):
                            print("ignore")
                            #do nothing with this line
                        else:
                            text = text_line.split('/')
                            thread_type = text[0].split(' ')[0]
                            if (thread_type == "id:"):
                                thread_type = text[0].split(' ')[0]
                            if (thread_type == 'Find'):
                                no_ops += int(text[1].split(':')[-1]) 


                            text_line = file.readline()
                            #text = text_line.split('/')
                            #print(text[0].split(' '))

                            lock_opportunity = float(text_line.split(': ')[1])

                    data.append([ratio[0], applications, no_ops])

    sort_data()
    write_to_table(applications, ratio, duration, type)
    file.close()
        #print("close this file ")
        # sort_data()
        # sort_again()
        #write_to_table()
        #print("There are " + str(why) + " files!")	
        #print("next directory ")