def average(arr):
    sum = 0
    for i in range(len(arr)):
        sum += arr[i]
    return sum / len(arr)


def findtp(x_data, y_data, threshold, minnum):
    if len(x_data) != len(y_data):
        print("no diff")
        return

    begin_index = 0
    turningpts = []
    k_list = []


    while True:
        if begin_index > len(x_data) - 1:
            break

        k_list_cache = []

        pointCount = 1
        for i in range(begin_index, len(x_data) - 1):
            k_list_cache.append((y_data[begin_index] - y_data[i + 1]) / (x_data[begin_index] - x_data[i + 1]))
            #if variance(k_list_cache) >= threshold:
            if abs((k_list_cache[-1] - k_list_cache[0]) / k_list_cache[0]) > threshold:
            #if abs(k_list_cache[-1] - k_list_cache[0]) > threshold:
                break
            
            pointCount += 1        
        #print("i:   ", i)
        

        if pointCount >= minnum:

            k_list.append(average(k_list_cache[0 : -1]))
            turningpts.append(begin_index)
            turningpts.append(begin_index + pointCount - 1)
            begin_index = begin_index + pointCount
        else:
            begin_index += 1    
        #print("begin_index:", begin_index)

    return [turningpts, k_list]
            
