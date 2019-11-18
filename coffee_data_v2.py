import pandas as pd
import re
import matplotlib.pyplot as plt
import numpy
import glob
import csv

final_cnt = 0
macro_cnt = 0
volume_final_cnt = 0
cnt = 0
sample_cnt = 0
percent_error = 0
dataString = ""

filename_pattern = r"(C:\\Users\\Owner\\Desktop\\Coffee Rigs\\Station 2\\RAW\\)(Station ([0-9]+)) (Unit ([0-9]+)) (Macro ([0-9]+)) (Tea|Coffee) (Travel XL|Travel|Half Carafe|Carafe|Cup XL|Cup) (Classic|Rich|Cold Brew|Over Ice|Speciality) (Integrated Flowmeter Validation) (Cycle ([0-9]+))(.csv)"
filename_pattern2 = r"(C:\\Users\\Owner\\Desktop\\Coffee Rigs\\Station 2\\)(Station ([0-9]+)) (Unit ([0-9]+)) (Macro ([0-9]+)) (Integrated Flowmeter Validation)(.csv)"

filedir = r"C:\Users\Owner\Desktop\Coffee Rigs\Station 2\RAW"
filedir2 = r"C:\Users\Owner\Desktop\Coffee Rigs\Station 2"

files = glob.glob(filedir+r'\*.csv')
files2 = glob.glob(filedir2+r'\*.csv')

numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

x = 3000*[0]
boiler_max = 3000*[0]
water_max = 3000*[0]
cycle_cnt = 3000*[0]
macro_number = 3000*[0]

volume_cnt = 3000*[0]
volume_cycle_cnt = 3000*[0]
volume_macro_cnt = 3000*[0]

for j in sorted(files2,key=numericalSort):
    df = pd.read_csv(j)
    n = re.match(filename_pattern2,j)

    if n is not None:
        for k in range(0,len(df["Weight (g)"])):
            volume_cnt[cnt] = df["Weight (g)"][k]
            volume_cycle_cnt[cnt] = df["Cycle"][k]
            volume_macro_cnt[cnt] = int(n.group(7)) + 1
            cnt+=1
    volume_final_cnt = cnt
cnt = 0

for i in sorted(files,key=numericalSort):

    df = pd.read_csv(i)
    m = re.match(filename_pattern,i)

    if m is not None:

        x[cnt] = cnt+1
        macro_number[cnt] = int(m.group(7))+1
        cycle_cnt[cnt] = int(m.group(13))
        boiler_max[cnt] = max(df["Boiler Temp"])
        water_max[cnt]=max(df["Water Temp"])
        final_cnt = int(m.group(13))
        cnt+=1

        if int(m.group(7)) == macro_cnt:
            continue

        else:
            plt.text(cnt, 140, 'Macro ' + str(macro_cnt))
            macro_cnt += 1

def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]

volume_cnt = remove_values_from_list(volume_cnt, 0)
volume_cycle_cnt = remove_values_from_list(volume_cycle_cnt, 0)
volume_macro_cnt = remove_values_from_list(volume_macro_cnt, 0)
for i in range(0,len(volume_macro_cnt)):
    volume_macro_cnt[i] = volume_macro_cnt[i] - 1

x = remove_values_from_list(x, 0)
boiler_max = remove_values_from_list(boiler_max, 0)
water_max = remove_values_from_list(water_max, 0)
cycle_cnt = remove_values_from_list(cycle_cnt, 0)
macro_number = remove_values_from_list(macro_number, 0)

for i in range(0,len(macro_number)):
    macro_number[i] = macro_number[i] - 1

f = open(filedir2 +' '+m.group(4)+ '.csv' , 'w+')
writer = csv.DictWriter(f, fieldnames=["SAMPLE#","MACRO","CYCLE","BOILER MAX","SCALE WEIGHT(g)","%ERROR"])
writer.writeheader()
f.close()

for i in range(0,volume_final_cnt):
    f = open(filedir2 +' '+m.group(4)+ '.csv' , 'ab')

    for j in range(0,cnt):
        if volume_macro_cnt[i] == macro_number[j] and volume_cycle_cnt[i] == cycle_cnt[j]:
            # dataString = 'Macro: '+ str(volume_macro_cnt[i]) +', Cycle: '+ str(volume_cycle_cnt[i]) + ', Boiler Max: ' + str(boiler_max[j]) + ', Scale Weight(g): ' + str(volume_cnt[i])
            sample_cnt += 1
            percent_error = (abs((1445 - float(volume_cnt[i]))/1445))*100
            dataString = str(sample_cnt) + ',' +str(volume_macro_cnt[i]) +','+ str(volume_cycle_cnt[i]) + ',' + str(boiler_max[j]) + ',' + str(volume_cnt[i]) + ',' + str(percent_error)
            b = (dataString + '\n').encode('utf-8')
            f.write(b)
            dataString =""
            percent_error = 0
f.close()
                # writer = csv.writer(writeFile, delimiter = '\n')
                # data.append(dataString)
                # writer.writerow(dataString)

plt.title(m.group(2)+' '+m.group(4))
plt.plot(x,boiler_max,color = 'red')
plt.plot(x,water_max,color = 'blue')

plt.xlabel('Cycle')
plt.ylabel('Max. Boiler Temp')

plt.show()
