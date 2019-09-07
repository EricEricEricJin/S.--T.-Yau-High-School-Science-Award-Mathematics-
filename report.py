import csv

class report:
    def __init__(self):
        self.all_data = []

    def add(self, data_list):  #data_list: 
        self.all_data.append(data_list)

    def write(self, filepath):
        f = open(filepath, "w")
        Writer = csv.writer(f)

        Writer.writerow(["data_source", "threshold", "min_num", "run_times", "csi_time", "my_method_time", "mean_error", "max_error", "linear", "curve"])

        for i in range(len(self.all_data)):
            Writer.writerow(self.all_data[i])
        f.close()

if __name__ == "__main__":
    a = report()
    a.add(["aaa", 1,2,3,4,5,6,7])
    a.write("trytry.csv")
