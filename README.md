# S.--T.-Yau-High-School-Science-Award-Mathematics
Simulation code for the fast approach

## Environment required by this program
1. Python3
2. Python3 third-party modules
  * numpy
  * matplotlib (only for visualization)
  
## How each program works
* check_k.py: Check weather the given set of points has linear properties
* csi.py: Cubic spline interpolation
* main.py: The program run as the enterance of the simulation
* my_method.py: The new fast approach
* readdata.py: Read the datas from CSV files
* readmsg.py: Read input command file
* report.py: Write experiment results into CSV files
* visualize.py: visualize datas

## Run this program
* Git clone all files under the same filepath
* Write the command file input.in in the same filepath as the following example:
    data_source :UCR_TS_Archive_2015/Haptics/Haptics_TRAIN
    threshold :0.02
    min_num :3
    run_times :10
    save_to :Haptics_TRAIN_2.csv
    end
    data_source :UCR_TS_Archive_2015/Lighting7/Lighting7_TRAIN
    threshold :0.02
    min_num :3
    run_times :10
    save_to :Lighting7_TRAIN_2.csv
    all_end
  
* run main.py
