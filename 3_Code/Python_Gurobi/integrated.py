from funcs import *
from params import *

parameters = read_problem(params_file=params_file)

# define index sets
indexes = indexes(no_3pl=parameters['no_3pl'],
                  no_suppliers=parameters['no_suppliers'],
                  no_trucks=parameters['no_trucks'],
                  no_items=parameters['no_items'],
                  no_docks=no_docks,
                  no_slots=no_slots)

problem, z, h = solve_model(parameters=parameters, indexes=indexes, relaxed=False, valid=True, open_3pls=[], open_suppliers=[])