import csv

def readdata(filepath):
    f = open(filepath, "r")
    reading = csv.reader(f)
    x_data = []
    y_data = []
    for row in reading:
        x_data.append(float(row[0]))
        y_data.append(float(row[1]))
    f.close()
    return [x_data, y_data]


def readdata_c(filepath):
    f = open(filepath, "r")
    reading = csv.reader(f)
    rt = []
    
    for row in reading:
        cache = []
        for i in range(len(row)):
            cache.append(float(row[i]))

        rt.append(cache)

    f.close()
    return rt


def readdata_x(filepath, rownum):
    f = open(filepath, "r")
    reading = csv.reader(f)
    
    i = 0
    for row in reading:
        if i == rownum:
            rt = row
            break
        i += 1

    rst = []

    for i in range(1, len(rt)):
        rst.append(float(rt[i]))
    return rst
    #return rt



if __name__ == "__main__":
    ret = readdata_x("50w.csv", 1)
    print(ret)