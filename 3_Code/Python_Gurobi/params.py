import numpy as np
from numpy import nan
import matplotlib.pyplot as plt
import math
import random
import pandas as pd
import copy
from gurobipy import *
import time as tm
np.set_printoptions(linewidth=np.inf)
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
status_codes = {1: 'LOADED', 2: 'OPTIMAL', 3: 'INFEASIBLE', 4: 'INF_OR_UNBD', 5: 'UNBOUNDED', 6: 'CUTOFF',
                7: 'ITERATION_LIMIT', 8: 'NODE_LIMIT', 9: 'TIME_LIMIT', 10: 'SOLUTION_LIMIT', 11: 'INTERRUPTED',
                12: 'NUMERIC', 13: 'SUB.1OPTIMAL', 14: 'INPROGRESS', 15: 'USER_OBJ_LIMIT'}

#  problem spec
no_docks = 6  # number of docks
no_slots = 10  # number of time slots (fixed in our model)

# parameters
params_file = 'paramsL377.xlsx'
thrs_3pl = 0.5
thrs_sup = 0.5
iters = 2
T = 360
discount = 0.1

