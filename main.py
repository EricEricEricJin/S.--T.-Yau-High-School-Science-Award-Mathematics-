import my_method
import csi
import numpy as np
import time
import readdata
import report
import readmsg




def testing(x_data, y_data, threshold, minnum, run_times):


    csi_t0 = time.clock()
    for i in range(run_times):
        c = csi.csi(x_data, y_data, '00')
        c.train()
    csi_t1 = time.clock()
    csi_t = csi_t1 - csi_t0


    my_method_t0 = time.clock()
    for i in range(run_times):
        mm = my_method.my_method(x_data, y_data, threshold, minnum)
        mm.train()
        
    my_method_t1 = time.clock()
    my_method_t = my_method_t1 - my_method_t0


    #比较和插值的差
    #即 比较和原点的差

    max_err = 0
    sum_err = 0

    for i in range(len(x_data)):
        y_mm = mm.query(x_data[i])
        y_csi = c.query(x_data[i])
        if abs((y_csi - y_mm) / y_csi) > max_err:
            max_err = abs((y_csi - y_mm) / y_csi)
        sum_err += abs((y_csi - y_mm) / y_csi)

    mean_err = sum_err / len(x_data)



    linear = 0
    curve = 0

    for i in range(len(mm.general_arr)):
        if mm.general_arr[i]['type'] == 0:
            linear += 1
        elif mm.general_arr[i]['type'] == 1:
            curve += 1

    return [csi_t, my_method_t, mean_err, max_err, linear, curve]



input_msg = readmsg.readmsg("input.in")
print("file_num:    ", len(input_msg))


for i in range(len(input_msg)):

    filepath = input_msg[i][0]
    threshold = input_msg[i][1]
    minnum = input_msg[i][2]
    run_times = input_msg[i][3]
    save_to = input_msg[i][4]

    with open(filepath, "r") as f:
        total_row_num = (len(f.readlines()))

    print("fp:  ", filepath)
    print("threshold:   ", threshold)
    print("min_num: ", minnum)
    print("run_times:   ", run_times)
    print("save_to: ", save_to)

    print("total_row_num:   ", total_row_num)

    #threshold = 0.02
    #minnum = 3
    #run_times = 10




    rpt = report.report()
    for rownum in range(total_row_num):

        ##rownum = 0

        
        y_data = readdata.readdata_x(filepath, rownum)
        x_data = np.linspace(0, len(y_data) - 1, len(y_data))

        data_source = filepath + "[" + str(rownum) + "]"



        rt_value = testing(x_data, y_data, threshold, minnum, run_times)


        rpt.add([data_source, threshold, minnum, run_times] + rt_value)
        print("Finished row:    ", rownum)

    rpt.write(save_to)






    #print(csi_t, my_method_t)
