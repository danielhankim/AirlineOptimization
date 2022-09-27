import myfunc
import os

#################
# Parameters 
#################

SAVE_PATH = '/home/mk139/WorkSpace/AirlineNW/SaveData/ToyModel'

n_sample = 500
N = 100
P_list = [10, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800]
c = 20
m = 8000

for P in P_list:
    list_of_satisfied = []
    list_of_unsatisfied = []
    list_of_wasted = []
    list_of_distance = []

    