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

def write_to_table():
    ratio_string = ""
    header = ["Number of Applications", "Ratios", "Fairness Index"]
    # for i in range(len(ratio)):
    #     ratio_string = "Ratio "+ str(i)
    #     header.append(ratio_string)
    # header.append("Fairness Index")
    f = open("./tables/ns_c_fair_list_tables/fairness_index.csv", 'a+', newline="")
    writer = csv.writer(f)
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
        

def sort_again():
    n = len(data)
    for i in range(2, n, 4):
        temp = data[i]
        data.insert(i - 2, temp)
        data.pop(i + 1)


rootdir = "./data/"
for dir in os.listdir(rootdir):
    type = dir.split('_list')[0]
    if type == "default_fair":
        for filename in os.listdir("./data/" + dir):
            with open(os.path.join("./data/" + dir, filename), 'r') as file:
                ratio = []
                temp_data = []
                denominator = 0
                nominator = 0
                #print(filename)
                applications = int(filename.split('_')[1])
                for i in range(applications):
                    ratio.append(int(filename.split('_')[i + 3]))
                duration = filename.split('_')[i + 5]
                text_line = file.readline()
                while text_line:
                    if ((text_line.split(' ')[0] == "Spin_Lock_Opp:") or (text_line.split(' ')[0] == "lock_hold_opp(ms):") or(text_line.split(' ')[0] == '') or (not text_line) or (text_line == " ")or (text_line == "\n")):
                        print("ignore")
                        #do nothing with this line
                    else:
                        text = text_line.split('/')
                        #print(text)
                        thread_type = text[0].split(' ')[0]
                        if (thread_type == "id:"):
                            thread_type = text[0].split(' ')[0]
                        no_ops = int(text[1].split(':')[-1])
                        denominator += no_ops * no_ops
                        nominator += no_ops
                        text_line = file.readline()
                    text_line = file.readline()
            #print(nominator)
            #print(denominator)
            fairness_index = (nominator * nominator) / ((applications * 4) * denominator)
            #print(fairness_index)
            temp_data.append(applications)
            #data.append(applications)
            for i in ratio:
                temp_data.append(i)
            temp_data.append(fairness_index)
            data.append(temp_data)
sort_data()
write_to_table()
file.close()