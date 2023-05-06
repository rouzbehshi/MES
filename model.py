# @author : Rouzbeh Shirvani
import pyomo.environ as pyo
import numpy as np
import matplotlib.pyplot as plt



# Declare Model

m = pyo.ConcreteModel('MES')

# Sets

m.I = pyo.Set(initialize=['ORC', 'Boiler1', 'Boiler2', 'HP'])
m.I_f = pyo.Set(within=m.I, initialize=['ORC', 'Boiler1', 'Boiler2'])
m.I_el = pyo.Set(within=m.I, initialize=['ORC'])
m.I_th = pyo.Set(within=m.I, initialize=['ORC', 'Boiler1', 'Boiler2', 'HP'])
m.I_el_cons = pyo.Set(within=m.I, initialize=['HP'])

T = 24
m.T = pyo.RangeSet(0, T - 1)

m.S = pyo.Set(initialize=['TES', 'BAT'])
m.S_el = pyo.Set(within=m.S, initialize=['BAT'])
m.S_th = pyo.Set(within=m.S, initialize=['TES'])

# Variables

m.f = pyo.Var(m.I_f, m.T, domain=pyo.PositiveReals)
m.q = pyo.Var(m.I_th, m.T, domain=pyo.PositiveReals)
m.p = pyo.Var(m.I_el, m.T, domain=pyo.PositiveReals)
m.el_in = pyo.Var(m.I_el_cons, m.T, domain=pyo.PositiveReals)
m.z = pyo.Var(m.I, m.T, domain=pyo.Binary)
m.dSU = pyo.Var(m.I, m.T, domain=pyo.Binary)
m.u = pyo.Var(m.S, m.T, domain=pyo.PositiveReals)
m.Charge = pyo.Var(m.S, m.T, domain=pyo.PositiveReals)
m.Discharge = pyo.Var(m.S, m.T, domain=pyo.PositiveReals)
m.El_buy = pyo.Var(m.T, domain=pyo.PositiveReals)
m.El_sell = pyo.Var(m.T, domain=pyo.PositiveReals)

# Data

d_el = [1371.7, 1377.2, 1369.9, 1371.8, 1378.8, 1426.3, 1508.9, 1637.2, 1930.8, 2229.9, 2163.1, 2212.8, 2224.6, 2196.0,
        2247.3, 2242.3, 2220.8, 2130.1, 2192.6, 1862.3, 1547.5, 1392.0, 1344.4, 1357.8]
d_th = [2082.5, 2291.6, 2500.7, 2605.3, 3125.9, 7500.0, 5835.7, 5938.1, 5522.0, 4478.7, 4169.3, 3958.0, 3437.4, 3439.5,
        3125.9, 3123.8, 3125.9, 3125.9, 3437.4, 1354.9, 938.8, 1145.8, 1352.8, 1773.1]

El_price_sell = [0.0561, 0.0494, 0.0457, 0.0438, 0.0431, 0.0465, 0.0550, 0.0621, 0.0750, 0.0675, 0.0602, 0.0582, 0.0562,
                 0.0556, 0.0561, 0.0598, 0.0630, 0.0632, 0.0667, 0.0737, 0.0746, 0.0725, 0.0632, 0.0550]
El_price_buy = [0.1272, 0.1272, 0.1272, 0.1272, 0.1272, 0.1272, 0.1272, 0.1496, 0.1514, 0.1514, 0.1514, 0.1514, 0.1514,
                0.1514, 0.1514, 0.1514, 0.1514, 0.1514, 0.1514, 0.1496, 0.1496, 0.1496, 0.1496, 0.1272]
Biomass_price = 0.025
NG_Price = 0.03

Fuel_cost = {'ORC': Biomass_price, 'Boiler1': NG_Price, 'Boiler2': NG_Price}
a_th = {'ORC': 0.651, 'Boiler1': 0.976, 'Boiler2': 0.945, 'HP': 3.590}
b_th = {'ORC': 47.09, 'Boiler1': -101.69, 'Boiler2': -63.09, 'HP': -34.19}
a_el = {'ORC': 0.154}
b_el = {'ORC': -53.831}
MinIn = {'ORC': 828.4, 'Boiler1': 794.5, 'Boiler2': 492.88, 'HP': 55.6}
MaxIn = {'ORC': 2238.8, 'Boiler1': 3178.0, 'Boiler2': 1971.52, 'HP': 427.4}
RUlim = {'ORC': 1119, 'Boiler1': 1589, 'Boiler2': 985.76, 'HP': 213.7}
Max_n_SU = {'ORC': 2, 'Boiler1': 2, 'Boiler2': 2, 'HP': 2}
OM_cost = {'ORC': 1.71, 'Boiler1': 0, 'Boiler2': 0, 'HP': 8.86}
SU_cost = {'ORC': 6.72, 'Boiler1': 4.8, 'Boiler2': 2.98, 'HP': 6.08}

MaxC = {'TES': 2000, 'BAT': 1000}  # different cases
eta_ch = {'BAT': 0.97}
eta_disch = {'BAT': 0.97}
eta_diss = {'TES': 0.995}


# Objective Function

def obj_fun(m):
    machines_fuel_cost = sum(Fuel_cost[i] * m.f[i, t] for i in m.I_f for t in [*range(0,T-1)])
    machines_OM_cost = sum(OM_cost[i] * m.z[i, t] for i in m.I for t in [*range(0,T-1)])
    machines_SU_cost = sum(SU_cost[i] * m.dSU[i, t] for i in m.I for t in [*range(0,T-1)])
    grid_SellBuy = sum(El_price_buy[t] * m.El_buy[t] - El_price_sell[t] * m.El_sell[t] for t in [*range(0,T-1)])
    return machines_fuel_cost + machines_OM_cost + machines_SU_cost + grid_SellBuy


m.obj = pyo.Objective(rule=obj_fun, sense=pyo.minimize)


# Constraint

# El balance

def el_balance_rule(m, t):
    return sum(m.p[i, t] for i in m.I_el) - sum(m.el_in[i, t] for i in m.I_el_cons) + m.El_buy[t] - m.El_sell[t] + sum(
        m.Discharge[s, t] for s in m.S_el) - sum(m.Charge[s, t] for s in m.S_el) == d_el[t]


m.el_balance_con = pyo.Constraint(m.T, rule=el_balance_rule)


# Thermal balance

def th_balance_rule(m, t):
    return sum(m.q[i, t] for i in m.I_th) + sum(m.Discharge[s, t] for s in m.S_th) - sum(
        m.Charge[s, t] for s in m.S_th) == d_th[t]


m.th_balance_con = pyo.Constraint(m.T, rule=th_balance_rule)


# El production

def el_prod_rule(m, i, t):
    return m.p[i, t] == a_el[i] * m.f[i, t] + b_el[i] * m.z[i, t]


m.el_prod_con = pyo.Constraint(m.I_el, m.T, rule=el_prod_rule)


# Th production

def th_prod_rule(m, i, t):
    if i in m.I_f:
        return m.q[i, t] == a_th[i] * m.f[i, t] + b_th[i] * m.z[i, t]
    elif i in m.I_el_cons:
        return m.q[i, t] == a_th[i] * m.el_in[i, t] + b_th[i] * m.z[i, t]


m.th_prod_con = pyo.Constraint(m.I_th, m.T, rule=th_prod_rule)


# Operating range

def min_input_rule(m, i, t):
    if i in m.I_f:
        return m.f[i, t] >= MinIn[i] * m.z[i, t]
    elif i in m.I_el_cons:
        return m.el_in[i, t] >= MinIn[i] * m.z[i, t]


m.min_input_con = pyo.Constraint(m.I, m.T, rule=min_input_rule)


def max_input_rule(m, i, t):
    if i in m.I_f:
        return m.f[i, t] <= MaxIn[i] * m.z[i, t]
    elif i in m.I_el_cons:
        return m.el_in[i, t] <= MaxIn[i] * m.z[i, t]


m.max_input_con = pyo.Constraint(m.I, m.T, rule=max_input_rule)


# Logical SU

def logical_SU_rule(m, i, t):
    if t > 0:
        return m.z[i, t] - m.z[i, t - 1] <= m.dSU[i, t]
    elif t == 0:
        return m.z[i, 0] - m.z[i, T - 1] <= m.dSU[i, 0]


m.logical_SU_con = pyo.Constraint(m.I, m.T, rule=logical_SU_rule)


# Ramp-up Limit

def ramp_up_rule(m, i, t):
    if i in m.I_f:
        if t > 0:
            return m.f[i, t] - m.f[i, t - 1] <= RUlim[i] * m.z[i, t]
        if t == 0:
            return m.f[i, 0] - m.f[i, T - 1] <= RUlim[i] * m.z[i, 0]
    elif i in m.I_el_cons:
        if t > 0:
            return m.el_in[i, t] - m.el_in[i, t - 1] <= RUlim[i] * m.z[i, t]
        if t == 0:
            return m.el_in[i, 0] - m.el_in[i, T - 1] <= RUlim[i] * m.z[i, 0]


m.ramp_up_con = pyo.Constraint(m.I, m.T, rule=ramp_up_rule)


# ORC dSU
def dSU_rule(m, i, t):
    return sum(m.dSU[i, t] for t in [*range(0,T-1)]) <= 1


dSU_con = pyo.Constraint(m.I, rule=dSU_rule)


# TH storage balance

def th_storage_rule(m, s, t):
    if t > 0:
        return m.u[s, t] - m.u[s, t - 1] * eta_diss[s] == m.Charge[s, t] - m.Discharge[s, t]
    if t == 0:
        return m.u[s, 0] - m.u[s, T - 1] * eta_diss[s] == m.Charge[s, 0] - m.Discharge[s, 0]


m.th_storage_con = pyo.Constraint(m.S_th, m.T, rule=th_storage_rule)


def el_storage_rule(m, s, t):
    if t > 0:
        return m.u[s, t] - m.u[s, t - 1] == m.Charge[s, t] * eta_ch[s] - m.Discharge[s, t] / eta_disch[s]
    if t == 0:
        return m.u[s, 0] - m.u[s, T - 1] == m.Charge[s, t] * eta_ch[s] - m.Discharge[s, 0] / eta_disch[s]


m.el_storage_con = pyo.Constraint(m.S_el, m.T, rule=el_storage_rule)


def capacity_rule(m, s, t):
    return m.u[s, t] <= MaxC[s]


m.capacity_con = pyo.Constraint(m.S, m.T, rule=capacity_rule)

# Solve
# solverpath_folder = '/Users/roozbeh/Documents/GitHub/MES'
# solvername = 'cbc'
# solverpath_exe = '/Users/roozbeh/Documents/GitHub/MES/cbc'
# sys.path.append(solverpath_exe)
# register_executable(name='cbc')
# solver = pyo.SolverFactory('cbc', mipgap=0.005)

solvername = 'glpk'
solver = pyo.SolverFactory(solvername, mipgap=0.005)


solver.solve(m).write()


# Variable results
electricity = {}
electricity_cons = {}
electricity_ch = {}
electricity_dis = {}
heat = {}
heat_ch = {}
heat_dis = {}
level_th = {}
level_el = {}
bat_level={}


for i in m.I.value:
    if i in m.I_el:
        electricity[i] = np.array(list(m.p[i, :].value))
    if i in m.I_th:
        heat[i] = np.array(list(m.q[i, :].value))
    if i in m.I_el_cons:
        electricity_cons[i] = np.array(list(m.el_in[i, :].value))
for s in m.S.value:
    if s in m.S_el:
        electricity_ch[s] = np.array(list(m.Charge[s, :].value))
        electricity_dis[s] = np.array(list(m.Discharge[s, :].value))
        level_el[s] = np.array(list(m.u[s, :].value))
    if s in m.S_th:
        heat_ch[s] = np.array(list(m.Charge[s, :].value))
        heat_dis[s] = np.array(list(m.Discharge[s, :].value))
        level_th[s] = np.array(list(m.u[s, :].value))
electricity_buy = np.array(list(m.El_buy[:].value))
electricity_sell = np.array(list(m.El_sell[:].value))
sum_electricity = np.add(electricity_ch['BAT'], electricity_dis['BAT'])
sum_heat = np.add(heat_ch['TES'], heat_dis['TES'])
print('electricity_ch: ', electricity_ch)
print('electricity_dis: ', electricity_dis)



#plots

times=range(T)
#Electricity
barplot = plt.figure(figsize=(8,6))
#adding electricity produced by machines
cm_el=0
for i in m.I_el:
    plt.bar(times, height = electricity[i], bottom= cm_el, label=i, color='blue')
    cm_el += np.array(electricity[i])
cm_el_neg = 0
#grid
plt.bar(times, height = electricity_buy, bottom= cm_el, label='Grid Buy', color='purple')
cm_el += electricity_buy
plt.bar(times, height = -electricity_sell, bottom= -cm_el_neg, label='Grid Sell',color='yellow')
cm_el_neg += electricity_sell
plt.plot(times, d_el, label='El Demand', color='black',linestyle='--')
plt.plot(times, sum_electricity, label='BATT level', color='red',linestyle='--')
#adding battery charge/discharge
for s in m.S_el:
    plt.bar(times, height = electricity_dis[s], bottom = cm_el, label= s+'discharge',color='green')
    cm_el += np.array(electricity_dis[s])
    plt.bar(times, height = -electricity_ch[s], bottom = cm_el_neg, label= s+'Charge',color='red')
    cm_el_neg += np.array(electricity_ch[s])
plt.legend()
plt.title('Electricity profile')
plt.xlabel('time')
plt.ylabel('kWh')
plt.show()







barplot = plt.figure(figsize=(8,6))
#adding heat produced by machines
cm_th=0

plt.bar(times, height = heat['ORC'], bottom= cm_th, label='ORC', color='blue')
cm_th += np.array(heat['ORC'])
plt.bar(times, height=heat['Boiler1'], bottom=cm_th, label='Boiler1', color='green')
cm_th += np.array(heat['Boiler1'])
plt.bar(times, height=heat['Boiler2'], bottom=cm_th, label='Boiler2', color='red')
cm_th += np.array(heat['Boiler2'])
plt.bar(times, height=heat['HP'], bottom=cm_th, label='HP', color='orange')
cm_th += np.array(heat['HP'])
cm_th_neg = 0
plt.plot(times, d_th, label='Heating Demand', color='black',linestyle='--')
plt.plot(times, sum_heat, label='TES level', color='red',linestyle='--')
#adding TES charge/discharge

for s in m.S_th:
    plt.bar(times, height = heat_dis[s], bottom = cm_th, label= s+'discharge',color='pink')
    cm_th += np.array(heat_dis[s])
    plt.bar(times, height = -heat_ch[s], bottom = cm_th_neg, label= s+'Charge',color='brown')
    cm_th_neg += np.array(heat_ch[s])
plt.legend()
plt.title('Heating profile')
plt.xlabel('time')
plt.ylabel('kWh')
plt.show()















