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

fixed_3pls = [d for d in indexes['D']]

for iter in range(iters):
    problem1, z1, h1 = solve_model(parameters=parameters, indexes=indexes, relaxed=False, valid=True, open_3pls=fixed_3pls, open_suppliers=[])
    fixed_suppliers = [r for r in indexes['R'] if h1[r].x >= thrs_sup]

    problem2, z2, h2 = solve_model(parameters=parameters, indexes=indexes, relaxed=False, valid=True, open_3pls=[], open_suppliers=fixed_suppliers)
    fixed_3pls = [d for d in indexes['D'] if z2[d].x >= thrs_3pl]