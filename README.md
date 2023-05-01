# MES
This repository is a part of the "LOW-CARBON TECHNOLOGIES" course project in Politecnico di Milano. The aim of this project is to find the optimal operating strategy of a Multi-energy system (MES) that minimizes the total operating costs.
The MES is composed of the following components:
1. 1 CHP consist of an Organic Rankine Cycle (ORC) fueled with biomass, producing heat and electricity.
2. 1 heat pump, producing heat by consuming using electricity.
3. 2 boilers, producing heat by consuming Natural gas (NG).
4. A thermal storage system.
5. An electric storage system (battery). 
## Model
**Sets:**

I = Set of units

T = Set of time

S = Set of storages

**Variables:**

$f_{i,t}$ = fuel input of unit i in time t

$q_{i,t}$ = heat output of unit i in time t

$e-out_{i,t}$ = electricity output of unit i in time t

$e-in_{i,t}$ = electricity input of unit i in time t

$u_{i,t}$ = state of unit i in time t (on/off) - Binary

$d_{SU_{i,t}}$ = state of start-up of unit i at time t - Binary
