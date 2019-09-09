import numpy as np

import matplotlib.pyplot as plt

import csi

import check_k


import readdata

import time


#x_data = readdata.readdata_c("50w.csv")[0]
#y_data = readdata.readdata_c("50w.csv")[1]

#x_ori = readdata.readdata_c("50w.csv")[0]
#y_ori = readdata.readdata_c("50w.csv")[1]

#x_ori = x_data
#y_ori = y_data

title = "Lighting7"

#x_data = readdata.readdata_x("UCR_TS_Archive_2015/" + title + "/" + title + "_TRAIN", 0)
y_data = readdata.readdata_x("UCR_TS_Archive_2015/" + title + "/" + title + "_TRAIN", 0)

#x_ori = readdata.readdata_x("UCR_TS_Archive_2015/" + title + "/" + title + "_TRAIN", 0)
y_ori = readdata.readdata_x("UCR_TS_Archive_2015/" + title + "/" + title + "_TRAIN", 0)

x_data = []
x_ori = []

x_data = np.linspace(0, len(y_data) - 1, len(y_data))
x_ori = x_data




t0 = time.clock()

for loop in range(1):


    receive_from_check_k = check_k.findtp(x_data, y_data, 0.05, 4)
    turningpts = receive_from_check_k[0]
    k_list = receive_from_check_k[1]

    general_arr = []
    #print(turningpts)

    if len(turningpts) > 0:

        if turningpts[0] == 0:
            #print(len(turningpts))
            for i in range(int(len(turningpts) / 2)):
                general_arr.append({'type': 0, 'begin': turningpts[2 * i], 'end': turningpts[2 * i + 1], 'coefficient': [k_list[i], y_data[turningpts[2 * i]] - k_list[i] * x_data[turningpts[2 * i]]]})
                
                #y_data[turningpts[2 * i + 1]] = k_list[i] * x_data[turningpts[2 * i + 1]] + y_data[turningpts[2 * i]] - k_list[i] * x_data[turningpts[2 * i]]
                y_data[turningpts[2 * i + 1]] = k_list[i] * (x_data[turningpts[2 * i + 1]] - x_data[turningpts[2 * i]]) + y_data[turningpts[2 * i]]
                #######

                if (2 * i + 2) < len(turningpts):
                    general_arr.append({'type': 1, 'begin': turningpts[2 * i + 1], 'end': turningpts[2 * i + 2], 'coefficient': ['11', k_list[i], k_list[i + 1]]})

        if turningpts[0] != 0:
            general_arr.append({'type': 1, 'begin': 0, 'end': turningpts[0], 'coefficient': ['01', 0, k_list[0]]}) #此处边界条件有些问题    # 现在没有了
            for i in range(int(len(turningpts) / 2)):
                general_arr.append({'type': 0, 'begin': turningpts[2 * i], 'end': turningpts[2 * i + 1], 'coefficient': [k_list[i], y_data[turningpts[2 * i]] - k_list[i] * x_data[turningpts[2 * i]]]})
                #y_data[turningpts[2 * i + 1]] = k_list[i] * x_data[turningpts[2 * i + 1]] + y_data[turningpts[2 * i]] - k_list[i] * x_data[turningpts[2 * i]]
                y_data[turningpts[2 * i + 1]] = k_list[i] * (x_data[turningpts[2 * i + 1]] - x_data[turningpts[2 * i]]) + y_data[turningpts[2 * i]]
                
                if (2 * i + 2) < len(turningpts):
                    general_arr.append({'type': 1, 'begin': turningpts[2 * i + 1], 'end': turningpts[2 * i + 2], 'coefficient': ['11', k_list[i], k_list[i + 1]]})
        if turningpts[-1] != len(x_data) - 1:
            general_arr.append({'type': 1, 'begin': turningpts[-1], 'end': len(x_data) - 1, 'coefficient': ['10', k_list[-1], 0]})
        
    else:
        #print("NO LINEAR")
        general_arr.append({'type': 1, 'begin': 0, 'end': len(x_data) - 1, 'coefficient': ['00',0,0]})

    #("\n\n")





    for i in range(len(general_arr)):
        #if general_arr[i]['type'] == 0:
            #plt.plot([x_data[general_arr[i]['begin']], x_data[general_arr[i]['end']]], [y_data[general_arr[i]['begin']], y_data[general_arr[i]['end']]], color = 'm')
            #plt.plot([])
        if general_arr[i]['type'] == 1:
            interp = csi.csi(x_data[general_arr[i]['begin'] : general_arr[i]['end'] + 1], y_data[general_arr[i]['begin'] : general_arr[i]['end'] + 1], general_arr[i]['coefficient'][0], general_arr[i]['coefficient'][1], general_arr[i]['coefficient'][2])
            interp.train()

            #y_dis = []
            #x_dis = np.linspace(x_data[general_arr[i]['begin']], x_data[general_arr[i]['end']], (x_data[general_arr[i]['end']] - x_data[general_arr[i]['begin']] + 1) * 5)
            #for i in range(len(x_dis)):
            #    y_dis.append(interp.query(x_dis[i]))
            #plt.plot(x_dis, y_dis, color = 'g')

#plt.scatter(x_data, y_data, color = 'b')

#plt.show()

#print(x_data, y_data)

t1 = time.clock()

print("time:    ", t1 - t0)


if y_data == y_ori:
    print("EQUAL")

Flag = True
for i in range(len(y_data)):
    if y_data[i] != y_ori[i]:
        Flag = False

print(Flag)


print(y_data, y_ori)




#print(general_arr)

#print(turningpts)




#遍历所有字典 general—_arr


#写人可以读的文件
'''
def write_file():
    f = open("a.func", "a")

    for i in range(len(general_arr)):

        if general_arr[i]['type'] == 0:
            #是直线
            str = ("y = " + str(general_arr[i]['coefficient'][0]) + " * x + " + str(general_arr[i]['coefficient'][1]) + " (" + str(general_arr[i]['begin']) + "<= x <=" + str(general_arr[i]['end']) + ")\n")
            f.write(str)

        elif general_arr[i]['type'] == 1:

            #是曲线
            curve = csi.csi(x_data[general_arr[i]['begin'] : general_arr[i]['end'] + 1], y_data[general_arr[i]['begin'] : general_arr[i]['end'] + 1], general_arr[i]['coefficient'][0], general_arr[i]['coefficient'][1], general_arr[i]['coefficient'][2])
            curve.train()
            f.write(str(curve.returnfunc()))   #没有写完    有错
            f.write("\n")

    f.close()
'''


#存为numpy数组

#x_test = np.linspace(-1, 1, 20)

#PLOT





plt.figure()

for i in range(len(general_arr)):
    if general_arr[i]['type'] == 0:

        

        plt.plot([x_data[general_arr[i]['begin']], x_data[general_arr[i]['end']]], [y_data[general_arr[i]['begin']], y_data[general_arr[i]['end']]], color = 'm')
        #plt.plot([])
    if general_arr[i]['type'] == 1:
        interp = csi.csi(x_data[general_arr[i]['begin'] : general_arr[i]['end'] + 1], y_data[general_arr[i]['begin'] : general_arr[i]['end'] + 1], general_arr[i]['coefficient'][0], general_arr[i]['coefficient'][1], general_arr[i]['coefficient'][2])
        interp.train()

        y_dis = []
        x_dis = np.linspace(x_data[general_arr[i]['begin']], x_data[general_arr[i]['end']], (x_data[general_arr[i]['end']] - x_data[general_arr[i]['begin']] + 1) * 10)
        for i in range(len(x_dis)):
            y_dis.append(interp.query(x_dis[i]))
        plt.plot(x_dis, y_dis, color = 'g')

plt.scatter(x_ori, y_ori, color = 'b', s = 3)
plt.title(title + "_TRAIN")
plt.show()

#print(x_data, y_data)

