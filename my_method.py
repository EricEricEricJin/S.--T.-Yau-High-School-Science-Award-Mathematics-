import check_k
import csi
import readdata
import numpy as np

class my_method:

    def __init__(self, x_data, y_data, threshold, minnum):
        self.x_data = x_data
        self.y_data = y_data
        self.threshold = threshold
        self.minnum = minnum
        self.general_arr = []


    def train(self):
        receive_from_check_k = check_k.findtp(self.x_data, self.y_data, self.threshold, self.minnum)
        turningpts = receive_from_check_k[0]
        k_list = receive_from_check_k[1]


        #print(turningpts)

        if len(turningpts) > 0:

            if turningpts[0] == 0:
                #print(len(turningpts))
                for i in range(int(len(turningpts) / 2)):
                    self.general_arr.append({'type': 0, 'begin': turningpts[2 * i], 'end': turningpts[2 * i + 1], 'coefficient': [k_list[i], self.y_data[turningpts[2 * i]] - k_list[i] * self.x_data[turningpts[2 * i]]]})
                    
                    #y_data[turningpts[2 * i + 1]] = k_list[i] * x_data[turningpts[2 * i + 1]] + y_data[turningpts[2 * i]] - k_list[i] * x_data[turningpts[2 * i]]
                    self.y_data[turningpts[2 * i + 1]] = k_list[i] * (self.x_data[turningpts[2 * i + 1]] - self.x_data[turningpts[2 * i]]) + self.y_data[turningpts[2 * i]]
                    #######

                    if (2 * i + 2) < len(turningpts):
                        self.general_arr.append({'type': 1, 'begin': turningpts[2 * i + 1], 'end': turningpts[2 * i + 2], 'coefficient': ['11', k_list[i], k_list[i + 1]]})

            if turningpts[0] != 0:
                self.general_arr.append({'type': 1, 'begin': 0, 'end': turningpts[0], 'coefficient': ['01', 0, k_list[0]]}) #此处边界条件有些问题    # 现在没有了
                for i in range(int(len(turningpts) / 2)):
                    self.general_arr.append({'type': 0, 'begin': turningpts[2 * i], 'end': turningpts[2 * i + 1], 'coefficient': [k_list[i], self.y_data[turningpts[2 * i]] - k_list[i] * self.x_data[turningpts[2 * i]]]})
                    #y_data[turningpts[2 * i + 1]] = k_list[i] * x_data[turningpts[2 * i + 1]] + y_data[turningpts[2 * i]] - k_list[i] * x_data[turningpts[2 * i]]
                    self.y_data[turningpts[2 * i + 1]] = k_list[i] * (self.x_data[turningpts[2 * i + 1]] - self.x_data[turningpts[2 * i]]) + self.y_data[turningpts[2 * i]]
                    
                    if (2 * i + 2) < len(turningpts):
                        self.general_arr.append({'type': 1, 'begin': turningpts[2 * i + 1], 'end': turningpts[2 * i + 2], 'coefficient': ['11', k_list[i], k_list[i + 1]]})
            if turningpts[-1] != len(self.x_data) - 1:
                self.general_arr.append({'type': 1, 'begin': turningpts[-1], 'end': len(self.x_data) - 1, 'coefficient': ['10', k_list[-1], 0]})
            
        else:
            #print("NO LINEAR")
            self.general_arr.append({'type': 1, 'begin': 0, 'end': len(self.x_data) - 1, 'coefficient': ['00',0,0]})


        #Xishu yong shuzu cun

        self.curve_coe_arr = []
        for i in range(len(self.general_arr)):
            if self.general_arr[i]['type'] == 1:
                interp = csi.csi(self.x_data[self.general_arr[i]['begin'] : self.general_arr[i]['end'] + 1], self.y_data[self.general_arr[i]['begin'] : self.general_arr[i]['end'] + 1], self.general_arr[i]['coefficient'][0], self.general_arr[i]['coefficient'][1], self.general_arr[i]['coefficient'][2])
                interp.train()
                self.curve_coe_arr.append(interp.c_mat)

        #整理数组   Use Dict

        for i in range(len(self.curve_coe_arr)):
            every_dev = []
            for j in range(int(self.curve_coe_arr[i].shape[0] / 4)):
                every_dev.append([self.curve_coe_arr[i][j * 4, 0], self.curve_coe_arr[i][j * 4 + 1, 0], self.curve_coe_arr[i][j * 4 + 2, 0], self.curve_coe_arr[i][j * 4 + 3, 0]])
            self.curve_coe_arr[i] = every_dev

        #print("\n\n\n DICT: ", self.curve_coe_arr)
        

#    def time_test(self):
#        for i in range(len(self.general_arr)):
#            if self.general_arr[i]['type'] == 1:
#                interp = csi.csi(self.x_data[self.general_arr[i]['begin'] : self.general_arr[i]['end'] + 1], self.y_data[self.general_arr[i]['begin'] : self.general_arr[i]['end'] + 1], self.general_arr[i]['coefficient'][0], self.general_arr[i]['coefficient'][1], self.general_arr[i]['coefficient'][2])
#                interp.train()

    def query(self, x):
        #locate X in the dict
        #二分查找
        '''
        low = 0
        high = len(self.general_arr) - 1
        mid =  int((len(self.general_arr) - 1) / 2)

        while True:
            if (self.x_data[self.general_arr[mid]['begin']] <= x) and (self.x_data[self.general_arr[mid]['end']] >= x):
                break

            if self.x_data[self.general_arr[mid]['begin']] > x:
                high = mid

                if (high + low) / 2 != int((high + low) / 2):
                    mid = int((high + low) / 2)
                else:
                    mid = int((high + low) / 2)
                #print(">")

            if self.x_data[self.general_arr[mid]['end']] < x:
                low = mid

                if (high + low) / 2 != int((high + low) / 2):
                    mid = int((high + low) / 2) + 1
                else:
                    mid = int((high + low) / 2)
                #print("<")
        '''

        curve_num = 0

        for mid in range(len(self.general_arr)):
            if (self.x_data[self.general_arr[mid]['begin']] <= x) and (self.x_data[self.general_arr[mid]['end']] >= x):
                break
            if self.general_arr[mid]['type'] == 1:
                curve_num += 1

        #print("low: ", low, "mid:   ", mid, "high:", high)

        if self.general_arr[mid]['type'] == 0:
            y = self.general_arr[mid]['coefficient'][0] * x + self.general_arr[mid]['coefficient'][1]


        elif self.general_arr[mid]['type'] == 1:

            index = 0
            while True:
                index += 1
                if x <= self.x_data[index]:
                    break  
            index -= 1

            #print("JIAN:    ", (x - self.general_arr[mid][]))
            a = self.curve_coe_arr[curve_num][int(index - self.general_arr[mid]['begin'])][0]
            b = self.curve_coe_arr[curve_num][int(index - self.general_arr[mid]['begin'])][1]
            c = self.curve_coe_arr[curve_num][int(index - self.general_arr[mid]['begin'])][2]
            d = self.curve_coe_arr[curve_num][int(index - self.general_arr[mid]['begin'])][3]
            y = a * (x ** 3) + b * (x ** 2) + c * x + d

        #print("i:   ", i)
        
        return y


