import numpy as np
from numpy import mat
import readdata

import time

class csi:

    def __init__(self, x_data, y_data, boundary_type, pre_k = 0.0, aft_k = 0.0):
        self.x_data = x_data
        self.pt_num = len(x_data)

        #初始化待定系数数组
        self.coe_mat = np.zeros((4 * (self.pt_num - 1), 1))

        #初始化x_mat数组
        self.x_mat = np.zeros((4 * (self.pt_num - 1), 4 * (self.pt_num - 1)))

        #边界条件   
        #二次导为0
        if boundary_type == '00':
            self.x_mat[0][0:2] = [6 * x_data[0], 2]
            self.x_mat[-1][-4:-2] = [6 * x_data[-1], 2]

        #一次导为上直线的斜率
        elif boundary_type == '11':
            self.x_mat[0][0 : 3] = [3 * x_data[0] ** 2, 2 * x_data[0], 1]
            self.x_mat[-1][-4:-1] = [3 * x_data[-1] ** 2, 2 * x_data[-1], 1]

        elif boundary_type == '01':
            self.x_mat[0][0:2] = [6 * x_data[0], 2]
            self.x_mat[-1][-4:-1] = [3 * x_data[-1] ** 2, 2 * x_data[-1], 1]


        elif boundary_type == '10':
            self.x_mat[0][0 : 3] = [3 * x_data[0] ** 2, 2 * x_data[0], 1]
            self.x_mat[-1][-4:-2] = [6 * x_data[-1], 2]


        else:
            print("err")


        for i in range(self.pt_num - 1):
            self.x_mat[4 * i + 1][4 * i : 4 * i + 4] = [x_data[i] ** 3, x_data[i] ** 2, x_data[i], 1]
            self.x_mat[4 * i + 1 + 1][4 * i : 4 * i + 4] = [x_data[i + 1] ** 3, x_data[i + 1] ** 2, x_data[i + 1] ** 1, 1]
            if(i != self.pt_num - 2):
                self.x_mat[4 * i + 2 + 1][4 * i : 4 * i + 8] = [3 * x_data[i + 1] ** 2, 2 * x_data[i + 1], 1, 0, -3 * x_data[i + 1] ** 2, -2 * x_data[i + 1], -1, 0]
                self.x_mat[4 * i + 3 + 1][4 * i : 4 * i + 8] = [6 * x_data[i + 1], 2, 0, 0, -6 * x_data[i + 1], -2, 0, 0]

        #初始化y_mat数组
        self.y_mat = np.zeros((4 * (self.pt_num - 1), 1))

        if boundary_type == '00':
            pass
        elif boundary_type == '01':
            self.y_mat[-1][0] = aft_k

        elif boundary_type == '10':
            self.y_mat[0][0] = pre_k
        
        elif boundary_type == '11':
            self.y_mat[0][0] = pre_k
            self.y_mat[-1][0] = aft_k
        else:
            print("err")

        for i in range(0, self.pt_num -1):
            self.y_mat[4 * i + 1][0] = y_data[i]
            self.y_mat[4 * i + 1 + 1][0] = y_data[i + 1]
            if(i != self.pt_num - 2):
                self.y_mat[4 * i + 2 + 1][0] = 0
                self.y_mat[4 * i + 3 + 1][0] = 0


    def train(self):
        self.c_mat = mat(self.coe_mat)
        x_mat = mat(self.x_mat)
        y_mat = mat(self.y_mat)
        
        self.c_mat = np.dot(x_mat.I, y_mat)
        #print(c_mat)

    def query(self, x):
        index = 0
        while True:
            index += 1
            if x <= self.x_data[index]:
                break
            
        index -= 1
        #print("index:   ", index)
        #print(self.c_mat[0][0])
        
        y = self.c_mat[4 * index, 0] * (x ** 3) + self.c_mat[4 * index + 1, 0] * (x ** 2) + self.c_mat[4 * index + 2, 0] * x + self.c_mat[4 * index + 3, 0]
        
        return y

