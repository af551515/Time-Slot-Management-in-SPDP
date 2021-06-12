from funcs import *

parameters = read_problem(params_file=params_file)

# define index sets
indexes = indexes\
    (no_3pl=parameters['no_3pl'],
                  no_suppliers=parameters['no_suppliers'],
                  no_trucks=parameters['no_trucks'],
                  no_items=parameters['no_items'],
                  no_docks=no_docks,
                  no_slots=no_slots)

print('\n', '**************************** T is set to {}'.format(T), '\n')
s1, t_param, y_param, tot_arrival_time = sub1(parameters=parameters, indexes=indexes, T=T, valid=True)
if s1.status in [2, 7, 8, 9, 10, 13]:
    s2 = sub2(parameters=parameters, indexes=indexes, t_param=t_param, y_param=y_param)

while (s1.status in [2, 7, 8, 9, 10, 13]) and (s2.status in [3]):
    T = (1 - discount) * T
    print('\n', '**************************** T is set to {}'.format(T), '\n')
    s1, t_param, y_param, tot_arrival_time = sub1(parameters=parameters, indexes=indexes, T=T, valid=True)
    if s1.status in [2, 7, 8, 9, 10, 13]:
        s2 = sub2(parameters=parameters, indexes=indexes, t_param=t_param, y_param=y_param)

if (s1.status in [2, 7, 8, 9, 10, 13]) and (s2.status in [2, 7, 8, 9, 10, 13]):
    print('\n')
    print('Subproblem 1 objective function is {}'.format(s1.objVal))
    print('Subproblem 2 objective function is {}'.format(s2.objVal))
    print('Total objective function value of the decomposed problem is {}'.format(s1.objVal + s2.objVal))
else:
    print('\n')
    print('NO FEASIBLE SOLUTION WAS FOUND')
