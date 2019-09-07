'''
def readmsg(fp):
    f = open(fp, "r")
    file_path = f.readline()[0 : -1]
    threshold = float(f.readline())
    min_num = int(f.readline())
    run_times = int(f.readline())
    save_to = f.readline()

    return [file_path, threshold, min_num, run_times, save_to]
'''

def readmsg(fp):
    f = open(fp, "r")

    rst = []

    while True:
        cache = [0, 0, 0, 0, 0]

        while True:

            

            ctt = f.readline()
            #print(ctt)

            if ":" in ctt:
                devpst = ctt.index(":")

            if "data_source" in ctt:
                cache[0] = ctt[devpst + 1 : -1]
            elif "threshold" in ctt:
                cache[1] = float(ctt[devpst + 1 : -1])
            elif "min_num" in ctt:
                cache[2] = int(ctt[devpst + 1 : -1])
            elif "run_times" in ctt:
                cache[3] = int(ctt[devpst + 1 : -1])
            elif "save_to" in ctt:
                cache[4] = ctt[devpst + 1 : -1]
            
            elif "end" in ctt:
                rst.append(cache)
                break

        if "all_end" in ctt:
            break
    return rst

if __name__ == "__main__":
    print(readmsg("input.in"))
    

    