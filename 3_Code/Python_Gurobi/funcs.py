from params import *


def read_problem(params_file):

    # fixed cost of truck 𝑘
    fv_df = pd.read_excel(params_file, sheet_name='fv', index_col=0)
    fv = {row: fv_df['fixed_cost'][row] for row in fv_df.index}

    # cost coefficient of traveling
    ct = pd.read_excel(params_file, sheet_name='ct', header=None).iloc[0, 0]

    # cost coefficient of opportunity
    co = pd.read_excel(params_file, sheet_name='co', header=None).iloc[0, 0]

    # demand for item g
    dm_df = pd.read_excel(params_file, sheet_name='dm', index_col=0)
    dm = {row: dm_df['demand'][row] for row in dm_df.index}
    total_demand = sum([dm[gg] for gg in dm])

    # volume of item g
    vl_df = pd.read_excel(params_file, sheet_name='vl', index_col=0)
    vl = {row: vl_df['volume'][row] for row in vl_df.index}

    # total quantity of item g that can be supplied by supplier r
    sc_df = pd.read_excel(params_file, sheet_name='sc', index_col=0)
    sc = {(row, col): sc_df[col][row] for row in sc_df.index for col in sc_df.columns}

    # capacity of truck k
    cp_df = pd.read_excel(params_file, sheet_name='cp', index_col=0)
    cp = {row: cp_df['capacity'][row] for row in cp_df.index}
    max_capacity = max([cp[kk] for kk in cp])

    # number of time slots required by truck 𝑘 for unloading items
    ns_df = pd.read_excel(params_file, sheet_name='ns', index_col=0)
    ns = {row: ns_df['no_slots'][row] for row in ns_df.index}

    # span of each time slot
    ts = pd.read_excel(params_file, sheet_name='ts', header=None).iloc[0, 0]

    # average travel time from node i to node j
    tt_df = pd.read_excel(params_file, sheet_name='tt', index_col=0)
    tt = {(row, col): tt_df[col][row] for row in tt_df.index for col in tt_df.columns}

    # average service time for node 𝑖
    st = pd.read_excel(params_file, sheet_name='st', header=None).iloc[0, 0]

    # earliest possible time for loading items from supplier
    el_df = pd.read_excel(params_file, sheet_name='el', index_col=0)
    el = {row: el_df['earliest'][row] for row in el_df.index}

    # latest possible time for loading items from supplier
    ll_df = pd.read_excel(params_file, sheet_name='ll', index_col=0)
    ll = {row: ll_df['latest'][row] for row in ll_df.index}

    # desired time of manufacturer for unloading
    du = pd.read_excel(params_file, sheet_name='du', header=None).iloc[0, 0]

    # latest possible time for unloading truck k
    lu_df = pd.read_excel(params_file, sheet_name='lu', index_col=0)
    lu = {row: lu_df['latest'][row] for row in lu_df.index}

    # a sufficiently large number
    LAMBDA = pd.read_excel(params_file, sheet_name='LAMBDA', header=None).iloc[0, 0]

    # a very small number
    epsilon = pd.read_excel(params_file, sheet_name='epsilon', header=None).iloc[0, 0]

    no_3pl = len([q for q in tt_df.index if 'd' in q])  # number of 3PL companies
    no_suppliers = len(el)  # number of suppliers
    no_trucks = len(fv)  # number of trucks
    no_items = len(dm)  # number of items

    parameters = {'no_3pl': no_3pl,
                  'no_suppliers': no_suppliers,
                  'no_trucks': no_trucks,
                  'no_items': no_items,
                  'fv': fv,
                  'ct': ct,
                  'co': co,
                  'dm': dm,
                  'total_demand': total_demand,
                  'vl': vl,
                  'sc': sc,
                  'cp': cp,
                  'max_capacity': max_capacity,
                  'ns': ns,
                  'ts': ts,
                  'tt': tt,
                  'st': st,
                  'el': el,
                  'll': ll,
                  'du': du,
                  'lu': lu,
                  'LAMBDA': LAMBDA,
                  'epsilon': epsilon}

    return parameters


def indexes(no_3pl, no_suppliers, no_trucks, no_items, no_docks, no_slots):

    D = ["d" + str(d + 1) for d in range(no_3pl)]  # set of 3PL companies
    R = ["r" + str(r + 1) for r in range(no_suppliers)]  # set of suppliers
    N1 = D + R  # set of 3PLs and suppliers
    N2 = ['mfr'] + R  # set of suppliers and the manufacturer
    K = ['k' + str(k + 1) for k in range(no_trucks)]  # set of trucks
    G = ['g' + str(g + 1) for g in range(no_items)]  # set of items
    P = ['p' + str(p + 1) for p in range(no_docks)]  # set of docks
    M = [m + 1 for m in range(no_slots)]  # set of time slots

    indexes = {'D': D, 'R': R, 'N1': N1, 'N2': N2, 'K': K, 'G': G, 'P': P, 'M': M}

    return indexes


def solve_model(parameters, indexes, relaxed, valid, open_3pls=[], open_suppliers=[]):

    no_3pl, no_suppliers, no_trucks, no_items, fv, ct, co, dm, total_demand, \
    vl, sc, cp, max_capacity, ns, ts, tt, st, el, ll, du, lu, LAMBDA, epsilon = (parameters[str(key)] for key in parameters)

    D, R, N1, N2, K, G, P, M = (indexes[str(key)] for key in indexes)

    ###################################################### define model ###################################################
    TSA = Model('TSA')
    TSA.setParam('TimeLimit', 3600)
    TSA.setParam('MIPFocus', 1)  # 1: finding good solcalutions; 2: proving optimality; 3: improving lower bound;
    # TSA.setParam('Heuristics', 0.5)

    ############################################ define decision variables ################################################

    x_tuplelist = []
    for i in N1:
        for j in N2:
            for k in K:
                x_tuplelist.append((i, j, k))
    x_tuplelist = tuplelist(x_tuplelist)
    x = TSA.addVars(x_tuplelist, lb=0, ub=1, vtype=GRB.BINARY, name='x')

    y_tuplelist = []
    for i in list(set(N1 + N2)):
        for k in K:
            y_tuplelist.append((i, k))
    y_tuplelist = tuplelist(y_tuplelist)
    y = TSA.addVars(y_tuplelist, lb=0, ub=1, vtype=GRB.BINARY, name='y')

    w_tuplelist = []
    for p in P:
        for m in M:
            for k in K:
                w_tuplelist.append((p, m, k))
    w_tuplelist = tuplelist(w_tuplelist)
    w = TSA.addVars(w_tuplelist, lb=0, ub=1, vtype=GRB.BINARY, name='w')

    t_tuplelist = []
    for i in list(set(N1 + N2)):
        for k in K:
            t_tuplelist.append((i, k))
    t_tuplelist = tuplelist(t_tuplelist)
    t = TSA.addVars(t_tuplelist, lb=0, vtype=GRB.CONTINUOUS, name='t')

    o_tuplelist = []
    for r in R:
        for g in G:
            for k in K:
                o_tuplelist.append((r, g, k))
    o_tuplelist = tuplelist(o_tuplelist)
    o = TSA.addVars(o_tuplelist, lb=0, vtype=GRB.CONTINUOUS, name='o')

    alpha1_tuplelist = []
    alpha2_tuplelist = []
    alpha1a_tuplelist = []
    alpha2a_tuplelist = []
    for k in K:
        alpha1_tuplelist.append(k)
        alpha2_tuplelist.append(k)
        alpha1a_tuplelist.append(k)
        alpha2a_tuplelist.append(k)
    alpha1_tuplelist = tuplelist(alpha1_tuplelist)
    alpha2_tuplelist = tuplelist(alpha2_tuplelist)
    alpha1a_tuplelist = tuplelist(alpha1a_tuplelist)
    alpha2a_tuplelist = tuplelist(alpha2a_tuplelist)
    alpha1 = TSA.addVars(alpha1_tuplelist, lb=0, vtype=GRB.CONTINUOUS, name='alpha1')
    alpha2 = TSA.addVars(alpha2_tuplelist, lb=0, vtype=GRB.CONTINUOUS, name='alpha2')
    alpha1a = TSA.addVars(alpha1a_tuplelist, lb=0, vtype=GRB.CONTINUOUS, name='alpha1a')
    alpha2a = TSA.addVars(alpha2a_tuplelist, lb=0, vtype=GRB.CONTINUOUS, name='alpha2a')

    psi_tuplelist = []
    for p in P:
        for m in M:
            for k in K:
                psi_tuplelist.append((p, m, k))
    psi_tuplelist = tuplelist(psi_tuplelist)
    psi = TSA.addVars(psi_tuplelist, lb=0, vtype=GRB.BINARY, name='psi')

    b_tuplelist = []
    for m in M:
        for k in K:
            b_tuplelist.append((m, k))
    b_tuplelist = tuplelist(b_tuplelist)
    b = TSA.addVars(b_tuplelist, lb=0, vtype=GRB.BINARY, name='b')

    l_tuplelist = []
    u_tuplelist = []
    for k in K:
        l_tuplelist.append(k)
        u_tuplelist.append(k)
    l_tuplelist = tuplelist(l_tuplelist)
    u_tuplelist = tuplelist(u_tuplelist)
    l = TSA.addVars(l_tuplelist, lb=1, vtype=GRB.INTEGER, name='l')
    u = TSA.addVars(u_tuplelist, ub=no_slots, vtype=GRB.INTEGER, name='u')

    z_tuplelist = []
    for i in D:
        z_tuplelist.append(i)
    z_tuplelist = tuplelist(z_tuplelist)
    z = TSA.addVars(z_tuplelist, lb=0, ub=1, vtype=GRB.BINARY, name='z')

    h_tuplelist = []
    for i in R:
        h_tuplelist.append(i)
    h_tuplelist = tuplelist(h_tuplelist)
    h = TSA.addVars(h_tuplelist, lb=0, ub=1, vtype=GRB.BINARY, name='h')

    ############################################### Set Objective Function ################################################
    TSA.setObjective(sum(fv[k] * y['mfr', k] for k in K) + ct * sum(
        tt[(i, j)] * x[i, j, k] for i in N1 for j in N2 for k in K) + co * sum(alpha1a[k] + alpha2a[k] for k in K),
                     GRB.MINIMIZE)

    ################################################# Setting Constraints #################################################

    # eq [20]
    for k in K:
        TSA.addConstr(alpha1[k] - alpha2[k] == du - t['mfr', k], name='eq20')

    # eq [21]
    for k in K:
        TSA.addConstr(alpha1a[k] <= LAMBDA * y['mfr', k], name='eq21')

    # eq [22]
    for k in K:
        TSA.addConstr(alpha1a[k] <= alpha1[k], name='eq22')

    # eq [23]
    for k in K:
        TSA.addConstr(alpha1a[k] >= alpha1[k] - LAMBDA * (1 - y['mfr', k]), name='eq23')

    # eq [24]
    for k in K:
        TSA.addConstr(alpha2a[k] <= LAMBDA * y['mfr', k], name='eq24')

    # eq [25]
    for k in K:
        TSA.addConstr(alpha2a[k] <= alpha2[k], name='eq25')

    # eq [26]
    for k in K:
        TSA.addConstr(alpha2a[k] >= alpha2[k] - LAMBDA * (1 - y['mfr', k]), name='eq26')

    # eq [2]
    for j in R:
        TSA.addConstr(sum(x[i, j, k] for i in N1 for k in K) <= 1, name='eq2')

    # eq [3]
    for i in R:
        TSA.addConstr(sum(x[i, j, k] for j in N2 for k in K) <= 1, name='eq3')

    # eq [4]
    for r in R:
        for k in K:
            TSA.addConstr(sum(x[i, r, k] for i in N1) == sum(x[r, j, k] for j in N2), name='eq4')

    # eq [5]
    for j in N2:
        for k in K:
            TSA.addConstr(sum(x[i, j, k] for i in N1) == y[j, k], name='eq5')

    # eq [6]
    for g in G:
        TSA.addConstr(sum(o[r, g, k] for r in R for k in K) >= dm[g], name='eq6')

    # eq [7]
    for k in K:
        TSA.addConstr(sum(vl[g] * o[r, g, k] for r in R for g in G) <= cp[k] * y['mfr', k], name='eq7')

    # eq [8]
    for g in G:
        for r in R:
            for k in K:
                TSA.addConstr(o[r, g, k] <= sc[(r, g)] * y[r, k], name='eq 8')

    # eq [9]
    for i in N1:
        for j in N2:
            for k in K:
                TSA.addConstr(t[i, k] + st + tt[(i, j)] - LAMBDA * (1 - x[i, j, k]) <= t[j, k], name='eq9')

    # eq [10]
    for r in R:
        for k in K:
            TSA.addConstr(el[r] * y[r, k] <= t[r, k], name='eq10')
            TSA.addConstr(t[r, k] <= ll[r] * y[r, k], name='eq10')

    # eq [11]
    for k in K:
        TSA.addConstr(t['mfr', k] <= lu[k] * y['mfr', k], name='eq11')

    # eq [36]
    for k in K:
        TSA.addConstr(ns[k] * y['mfr', k] <= sum(psi[p, m, k] for p in P for m in M), name='eq36')

    # eq [29][30][31][32]
    for k in K:
        TSA.addConstr(l[k] <= (t['mfr', k] / ts) + 1, name='eq29')
        TSA.addConstr(l[k] >= (t['mfr', k] / ts) + epsilon, name='eq30')
        TSA.addConstr(u[k] <= (t['mfr', k] / ts) + ns[k], name='eq31')
        TSA.addConstr(u[k] >= (t['mfr', k] / ts) + ns[k] - 1, name='eq32')

    # eq [37][38][39]
    for p in P:
        for m in M:
            for k in K:
                TSA.addConstr(psi[p, m, k] <= w[p, m, k], name='eq37')
                TSA.addConstr(psi[p, m, k] <= LAMBDA * b[m, k], name='eq38')
                TSA.addConstr(psi[p, m, k] >= w[p, m, k] - LAMBDA * (1 - b[m, k]), name='eq39')

    # eq [41][42]
    for m in M:
        for k in K:
            TSA.addConstr(b[m, k] <= 1 + (u[k] - m) / no_slots, name='eq41')
            TSA.addConstr(b[m, k] <= 1 + (m - l[k]) / no_slots, name='eq42')

    # eq [13]
    for m in M:
        for k in K:
            TSA.addConstr(sum(w[p, m, k] for p in P) <= y['mfr', k], name='eq13')

    # eq [14]
    for p in P:
        for m in M:
            TSA.addConstr(sum(w[p, m, k] for k in K) <= 1, name='eq14')

    # eq [44]
    for p in P:
        for m in M[:-1]:
            for k in K:
                TSA.addConstr(w[p, m + 1, k] <= w[p, m, k] + LAMBDA * (1 - b[m, k]), name='eq44')

    # ------------------------------- Valid Inequalities -------------------------------------------------------------------

    if valid:
        # eq [45]
        TSA.addConstr(sum(y['mfr', k] for k in K) >= 1, name='eq45')

        # eq [46]
        for k in K:
            TSA.addConstr(
                t['mfr', k] >= sum(tt[(i, j)] * x[i, j, k] for i in N1 for j in N2) + sum(st * y[i, k] for i in N1),
                name='eq46')

        # eq [47]
        TSA.addConstr(sum(y['mfr', k] for k in K) >= math.ceil(total_demand / max_capacity), name='eq47')

        # eq [48]
        for i in R:
            for j in R:
                TSA.addConstr(sum(x[i, j, k] + x[j, i, k] for k in K) <= 1, name='eq48')

    # ----------------------------------------------------------------------------------------------------------------------

    for i in D:
        TSA.addConstr(sum(x[i, j, k] for j in R for k in K) <= LAMBDA * z[i], name='eq_dec_1')
        TSA.addConstr(z[i] <= sum(x[i, j, k] for j in R for k in K), name='eq_dec_2')

    for i in R:
        TSA.addConstr(sum(y[i, k] for k in K) <= LAMBDA * h[i], name='eq_dec_3')
        TSA.addConstr(h[i] <= sum(y[i, k] for k in K), name='eq_dec_4')

    # ----------------------------------------------------------------------------------------------------------------------

    if len(open_3pls) > 0:
        for i in D:
            if i in open_3pls:
                z[i].lb = 1
            else:
                z[i].ub = 0

    if len(open_suppliers) > 0:
        for i in R:
            if i in open_suppliers:
                h[i].lb = 1
            else:
                h[i].ub = 0

    ################################################### Solve the Model ###################################################

    TSA.update()
    if relaxed:
        for v in TSA.getVars():
            v.setAttr('vtype', 'C')


    TSA.optimize()

    t_param = {(i, k): t[i, k].x for i in N2 for k in K}
    y_param = {(i, k): y[i, k].x for i in N2 for k in K}
    tot_arrival_time = sum([t['mfr', k].x for k in K])
    print(t_param)
    print(y_param)
    print(tot_arrival_time)
    for k in K:
        print(t['mfr', k].varName, t['mfr', k].x)

    return TSA, z, h


def sub1(parameters, indexes, T, valid=True):

    no_3pl, no_suppliers, no_trucks, no_items, fv, ct, co, dm, total_demand, \
    vl, sc, cp, max_capacity, ns, ts, tt, st, el, ll, du, lu, LAMBDA, epsilon = (parameters[str(key)] for key in
                                                                                 parameters)

    D, R, N1, N2, K, G, P, M = (indexes[str(key)] for key in indexes)

    ###################################################### define model ###################################################
    s1 = Model('s1')
    s1.setParam('TimeLimit', 600)
    s1.setParam('MIPFocus', 1)  # 1: finding good solutions; 2: proving optimality; 3: improving lower bound;
    # s2.setParam('Heuristics', 0.5)

    ############################################ define decision variables ################################################

    x_tuplelist = []
    for i in N1:
        for j in N2:
            for k in K:
                x_tuplelist.append((i, j, k))
    x_tuplelist = tuplelist(x_tuplelist)
    x = s1.addVars(x_tuplelist, lb=0, ub=1, vtype=GRB.BINARY, name='x')

    y_tuplelist = []
    for i in list(set(N1 + N2)):
        for k in K:
            y_tuplelist.append((i, k))
    y_tuplelist = tuplelist(y_tuplelist)
    y = s1.addVars(y_tuplelist, lb=0, ub=1, vtype=GRB.BINARY, name='y')

    w_tuplelist = []
    for p in P:
        for m in M:
            for k in K:
                w_tuplelist.append((p, m, k))
    w_tuplelist = tuplelist(w_tuplelist)
    w = s1.addVars(w_tuplelist, lb=0, ub=1, vtype=GRB.BINARY, name='w')

    t_tuplelist = []
    for i in list(set(N1 + N2)):
        for k in K:
            t_tuplelist.append((i, k))
    t_tuplelist = tuplelist(t_tuplelist)
    t = s1.addVars(t_tuplelist, lb=0, vtype=GRB.CONTINUOUS, name='t')

    o_tuplelist = []
    for r in R:
        for g in G:
            for k in K:
                o_tuplelist.append((r, g, k))
    o_tuplelist = tuplelist(o_tuplelist)
    o = s1.addVars(o_tuplelist, lb=0, vtype=GRB.CONTINUOUS, name='o')

    l_tuplelist = []
    u_tuplelist = []
    for k in K:
        l_tuplelist.append(k)
        u_tuplelist.append(k)
    l_tuplelist = tuplelist(l_tuplelist)
    u_tuplelist = tuplelist(u_tuplelist)
    l = s1.addVars(l_tuplelist, lb=1, vtype=GRB.INTEGER, name='l')
    u = s1.addVars(u_tuplelist, ub=no_slots, vtype=GRB.INTEGER, name='u')

    ############################################### Set Objective Function ################################################
    s1.setObjective(sum(fv[k] * y['mfr', k] for k in K) +
                    ct * sum(tt[(i, j)] * x[i, j, k] for i in N1 for j in N2 for k in K),
                    GRB.MINIMIZE)

    ################################################# Setting Constraints #################################################
    # eq [2]
    for j in R:
        s1.addConstr(sum(x[i, j, k] for i in N1 for k in K) <= 1, name='eq2')

    # eq [3]
    for i in R:
        s1.addConstr(sum(x[i, j, k] for j in N2 for k in K) <= 1, name='eq3')

    # eq [4]
    for r in R:
        for k in K:
            s1.addConstr(sum(x[i, r, k] for i in N1) == sum(x[r, j, k] for j in N2), name='eq4')

    # eq [5]
    for j in N2:
        for k in K:
            s1.addConstr(sum(x[i, j, k] for i in N1) == y[j, k], name='eq5')

    # eq [6]
    for g in G:
        s1.addConstr(sum(o[r, g, k] for r in R for k in K) >= dm[g], name='eq6')

    # eq [7]
    for k in K:
        s1.addConstr(sum(vl[g] * o[r, g, k] for r in R for g in G) <= cp[k] * y['mfr', k], name='eq7')

    # eq [8]
    for g in G:
        for r in R:
            for k in K:
                s1.addConstr(o[r, g, k] <= sc[(r, g)] * y[r, k], name='eq 8')

    # eq [9]
    for i in N1:
        for j in N2:
            for k in K:
                s1.addConstr(t[i, k] + st + tt[(i, j)] - LAMBDA * (1 - x[i, j, k]) <= t[j, k], name='eq9')

    # eq [10]
    for r in R:
        for k in K:
            s1.addConstr(el[r] * y[r, k] <= t[r, k], name='eq10')
            s1.addConstr(t[r, k] <= ll[r] * y[r, k], name='eq10')

    # eq [11]
    for k in K:
        s1.addConstr(t['mfr', k] <= lu[k] * y['mfr', k], name='eq11')

    # ------------------------------- Valid Inequalities -------------------------------------------------------------------

    if valid:
        # eq [45]
        s1.addConstr(sum(y['mfr', k] for k in K) >= 1, name='eq45')

        # eq [46]
        for k in K:
            s1.addConstr(
                t['mfr', k] >= sum(tt[(i, j)] * x[i, j, k] for i in N1 for j in N2) + sum(st * y[i, k] for i in N1),
                name='eq46')

        # eq [47]
        s1.addConstr(sum(y['mfr', k] for k in K) >= math.ceil(total_demand / max_capacity), name='eq47')

        # eq [48]
        for i in R:
            for j in R:
                s1.addConstr(sum(x[i, j, k] + x[j, i, k] for k in K) <= 1, name='eq48')

    # ------------------------------- Total Arrival Time -------------------------------------------------------------------

    #s1.addConstr(sum(t['mfr', k] for k in K) <= T)
    for k in K:
        s1.addConstr(t['mfr', k] <= T)

    ################################################### Solve the Model ###################################################

    s1.update()
    s1.optimize()

    t_param = {}
    y_param = {}
    tot_arrival_time = 0

    if s1.status in [2, 7, 8, 9, 10, 13]:

        t_param = {(i, k): t[i, k].x for i in N2 for k in K}
        y_param = {(i, k): y[i, k].x for i in N2 for k in K}
        tot_arrival_time = sum([t['mfr', k].x for k in K])
        #print(t_param)
        #print(y_param)
        #print(tot_arrival_time)
        #for k in K:
            #print(t['mfr', k].varName, t['mfr', k].x)

    return s1, t_param, y_param, tot_arrival_time


def sub2(parameters, indexes, t_param, y_param):

    no_3pl, no_suppliers, no_trucks, no_items, fv, ct, co, dm, total_demand, \
    vl, sc, cp, max_capacity, ns, ts, tt, st, el, ll, du, lu, LAMBDA, epsilon = (parameters[str(key)] for key in parameters)

    D, R, N1, N2, K, G, P, M = (indexes[str(key)] for key in indexes)

    ###################################################### define model ###################################################
    s2 = Model('s2')
    s2.setParam('TimeLimit', 5000)
    s2.setParam('MIPFocus', 1)  # 1: finding good solutions; 2: proving optimality; 3: improving lower bound;
    # s2.setParam('Heuristics', 0.5)

    ############################################ define decision variables ################################################

    w_tuplelist = []
    for p in P:
        for m in M:
            for k in K:
                w_tuplelist.append((p, m, k))
    w_tuplelist = tuplelist(w_tuplelist)
    w = s2.addVars(w_tuplelist, lb=0, ub=1, vtype=GRB.BINARY, name='w')

    alpha1_tuplelist = []
    alpha2_tuplelist = []
    alpha1a_tuplelist = []
    alpha2a_tuplelist = []
    for k in K:
        alpha1_tuplelist.append(k)
        alpha2_tuplelist.append(k)
        alpha1a_tuplelist.append(k)
        alpha2a_tuplelist.append(k)
    alpha1_tuplelist = tuplelist(alpha1_tuplelist)
    alpha2_tuplelist = tuplelist(alpha2_tuplelist)
    alpha1a_tuplelist = tuplelist(alpha1a_tuplelist)
    alpha2a_tuplelist = tuplelist(alpha2a_tuplelist)
    alpha1 = s2.addVars(alpha1_tuplelist, lb=0, vtype=GRB.CONTINUOUS, name='alpha1')
    alpha2 = s2.addVars(alpha2_tuplelist, lb=0, vtype=GRB.CONTINUOUS, name='alpha2')
    alpha1a = s2.addVars(alpha1a_tuplelist, lb=0, vtype=GRB.CONTINUOUS, name='alpha1a')
    alpha2a = s2.addVars(alpha2a_tuplelist, lb=0, vtype=GRB.CONTINUOUS, name='alpha2a')

    psi_tuplelist = []
    for p in P:
        for m in M:
            for k in K:
                psi_tuplelist.append((p, m, k))
    psi_tuplelist = tuplelist(psi_tuplelist)
    psi = s2.addVars(psi_tuplelist, lb=0, vtype=GRB.BINARY, name='psi')

    b_tuplelist = []
    for m in M:
        for k in K:
            b_tuplelist.append((m, k))
    b_tuplelist = tuplelist(b_tuplelist)
    b = s2.addVars(b_tuplelist, lb=0, vtype=GRB.BINARY, name='b')

    l_tuplelist = []
    u_tuplelist = []
    for k in K:
        l_tuplelist.append(k)
        u_tuplelist.append(k)
    l_tuplelist = tuplelist(l_tuplelist)
    u_tuplelist = tuplelist(u_tuplelist)
    l = s2.addVars(l_tuplelist, lb=1, vtype=GRB.INTEGER, name='l')
    u = s2.addVars(u_tuplelist, ub=no_slots, vtype=GRB.INTEGER, name='u')

    ############################################### Set Objective Function ################################################
    s2.setObjective(co * sum(alpha1a[k] + alpha2a[k] for k in K), GRB.MINIMIZE)

    ################################################# Setting Constraints #################################################

    # eq [20]
    for k in K:
        s2.addConstr(alpha1[k] - alpha2[k] == du - t_param[('mfr', k)], name='eq20')

    # eq [21]
    for k in K:
        s2.addConstr(alpha1a[k] <= LAMBDA * y_param[('mfr', k)], name='eq21')

    # eq [22]
    for k in K:
        s2.addConstr(alpha1a[k] <= alpha1[k], name='eq22')

    # eq [23]
    for k in K:
        s2.addConstr(alpha1a[k] >= alpha1[k] - LAMBDA * (1 - y_param[('mfr', k)]), name='eq23')

    # eq [24]
    for k in K:
        s2.addConstr(alpha2a[k] <= LAMBDA * y_param[('mfr', k)], name='eq24')

    # eq [25]
    for k in K:
        s2.addConstr(alpha2a[k] <= alpha2[k], name='eq25')

    # eq [26]
    for k in K:
        s2.addConstr(alpha2a[k] >= alpha2[k] - LAMBDA * (1 - y_param[('mfr', k)]), name='eq26')

    # eq [36]
    for k in K:
        s2.addConstr(sum(psi[p, m, k] for p in P for m in M) >= ns[k] * y_param[('mfr', k)], name='eq36')

    # eq [29][30][31][32]
    for k in K:
        s2.addConstr(l[k] <= (t_param[('mfr', k)] / ts) + 1, name='eq29')
        s2.addConstr(l[k] >= (t_param[('mfr', k)] / ts) + epsilon, name='eq30')
        s2.addConstr(u[k] <= (t_param[('mfr', k)] / ts) + ns[k], name='eq31')
        s2.addConstr(u[k] >= (t_param[('mfr', k)] / ts) + ns[k] - 1, name='eq32')

    # eq [37][38][39]
    for p in P:
        for m in M:
            for k in K:
                s2.addConstr(psi[p, m, k] <= w[p, m, k], name='eq37')
                s2.addConstr(psi[p, m, k] <= LAMBDA * b[m, k], name='eq38')
                s2.addConstr(psi[p, m, k] >= w[p, m, k] - LAMBDA * (1 - b[m, k]), name='eq39')

    # eq [41][42]
    for m in M:
        for k in K:
            s2.addConstr(b[m, k] <= 1 + (u[k] - m) / no_slots, name='eq41')
            s2.addConstr(b[m, k] <= 1 + (m - l[k]) / no_slots, name='eq42')

    # eq [13]
    for m in M:
        for k in K:
            s2.addConstr(sum(w[p, m, k] for p in P) <= y_param[('mfr', k)], name='eq13')

    # eq [14]
    for p in P:
        for m in M:
            s2.addConstr(sum(w[p, m, k] for k in K) <= 1, name='eq14')

    # eq [44]
    for p in P:
        for m in M[:-1]:
            for k in K:
                s2.addConstr(w[p, m + 1, k] <= w[p, m, k] + LAMBDA * (1 - b[m, k]), name='eq44')

    ################################################### Solve the Model ###################################################

    s2.update()
    s2.optimize()

    return s2