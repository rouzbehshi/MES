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

I = Set of units { $Machines_{fuel}, Machines_{el}, Machines_{th}, Machines_{elCons}$ }

T = Set of time

S = Set of storages { $Storages_{el}, Storages_{th}$ }

**Variables:**

$f_{i,t}$ = fuel input of unit i in time t

$q_{i,t}$ = heat output of unit i in time t

$e-out_{i,t}$ = electricity output of unit i in time t

$e-in_{i,t}$ = electricity input of unit i in time t

$u_{i,t}$ = state of unit i in time t (on/off) - Binary

$d_{SU_{i,t}}$ = state of start-up of unit i at time t - Binary


$u_{s,t}$ = level of energy (heat or electricity)of storage s at time t

$Charge_{s,t}$ = Energy charged to storage s at time t

$Discharge_{s,t}$ = Energy discharged from storage s at time t

$El_{buy_{t}}$ = Electricity bought from the grid at time t

$El_{sell_{t}}$ = Electrictiy sold to the grid at time t


**Parameters:**

$d_{el_t}$ = demand of electricity at time t

$d_{th_t}$ = demand of heat at time t

$El_{price_{sell,t}}$ = Electricity selling price to grid at time t (Constant)

$El_{price_{buy,t}}$ = Electricity buying price to grid at time t (Constant)

$NG_{Price}$ = Natural gas price (Constant)

$Biomass_{price}$ = Biomass price (Constant)

$Fuel-{Cost_{i}}$ = Fuel cost of unit i,for machine $i \in I_{f}$



_Heat production of units with fuel input:_

$q_{i,t} = a_{th_{i}}\cdot f_{i,t} + b_{th_{i}}\cdot z_{i,t}$

_Heat production of units with electricity input:_

$q_{i,t} = a_{th_i}\cdot el-{in_{i,t}} + b_{th_{i}}\cdot z_{i,t}$

$a_{th_{i}}$ = coefficient of heat production map of unit i

$b_{th_{i}}$ = constant term of heat production map of unit i

_Electricity production:_

$p_{i,t} = a_{el_{i}}\cdot f_{i,t} + b_{el_{i}}\cdot z_{i,t}$

$a_{el_{i}}$ = coefficient of power production map of unit i

$b_{el_{i}}$ = constant term of power production map of unit i

For machines $i\in I$:

$Min-{In_{i}}$ = minimum input of unit i (if on)

$Max-{In_{i}}$ = maximum input of unit i (if on)

$RUlim_{i}$ = ramp-up limit of unit i (Only for ORC)

$Max-n-{SU_{i}}$ = maximum number of daily start-ups of unit i (only for ORC)

$OM_{i}$ = fixed O&M costs of unit i

$SU_{i}$ = fixed start-up cost of unit i

_For storage:_

$maxC_{s}$ = maximum capacity (heat or electricity)of storage s

$eta_{ch_{s}}$, $eta_{disch_{s}}$ = charge/discharge efficiency of electric srorage s

$eta_{{diss}_{s}}$ = thermal loss efficiency of thermal storage s

**Objective function**

OBJ = machines-fuel-cost + machines-OM-cost + machines-SU-cost + grid-SellBuy

$machines-fuel-cost = \sum_{i\in I_f} \sum_{t\in T} Fuel-cost_{i}\cdot f_{i,t}$

$machines-OM-cost = \sum_{i\in I} \sum_{t\in T} OM_{i}\cdot z_{i,t}$

$machines-SU-cost = \sum_{i\in I} \sum_{t\in T} SU_{i}\cdot dSU_{i,t}$

$grid-Sell-Buy = \sum_{t\in T} El_{price_{buy}}\cdot El_{buy_{t}} - \sum_{t\in T} El_{price_{sell}}\cdot El_{sell_{t}}$


**Constraints**

Electricity balance:

$\sum_{i\in I_{el}} p_{i,t} - \sum_{i\in I_{el_{Cons}}}el-in_{i,t} + El_{buy_{t}} - El_{sell_{t}} + \sum_{s\in S_{el}} Discharge_{s,t}-\sum_{s\in S_{el}} Charge_{s,t} = d_{el_{t}}$

Heat balance:

$\sum_{i\in I_{th}} q_{i,t} + \sum_{s\in S_{th}} Discharge_{s,t} - \sum_{s\in S_{th}} Charge_{s,t} = d_{th_{s}}$

Operating range-min:

$f_{i,t} \geq minIn_{i}\cdot z_{i,t}$

$el-in_{i,t} \geq minIn_{i}\cdot z_{i,t}$

Operating range-max:

$f_{i,t}\leq maxIn_{i}\cdot z_{i,t}$

$el-in_{i,t}\leq maxIn_{i}\cdot z_{i,t}$

Logical constraints for start-up of units:

$z_{i,t} - z_{i,t-1}\leq dSU_{i,t}$

Ramp-up Constraints:

$f_{i,t} - f_{i,t-1}\leq RUlim_{i}\cdot z_{i,t}$

$el-in_{i,t} - el-in_{i,t-1}\leq RUlim_{i}\cdot z_{i,t}$

Max number of start-ups per day:

$\sum_{t\in T} dSU_{i,t} \leq 1$

Thermal storage energy balance:

$u_{s,t}-u_{s,t-1}\cdot eta_{diss,s} = Charge_{s,t} - Discharge_{s,t}$

Electric storage energy balance:

$u_{s,t}-u_{s,t-1} = Charge_{s,t}\cdot eta_{ch,s} - \frac{Discharge_{s,t}}{eta_{diss,s}}$

Storage capacity:

$u_{s,t}\leq MaxC_{s}$

# Results

**Case A: No electric and thermal storages available**

Model is infeasible.

**Case B: Thermal storage with capacity equal to 2 MWh, no battery**

<p align="center">
<img src="https://github.com/rouzbehshi/MES/blob/c4267eba5ad60132a84f760f78f6d465a8aac9d6/plots/caseB_1.png"  alt="Electricity profile" title="Electricity profile" width="400" >
</p>

<p align="center">
<img src="https://github.com/rouzbehshi/MES/blob/c4267eba5ad60132a84f760f78f6d465a8aac9d6/plots/caseB_2.png"  alt="Heat profile" title="Heat profile" width="400" >
</p>

**Case C: Thermal storage with capacity equal to 2 MWh, and battery with capacity equal to 1 MWh**

<p align="center">
<img src="https://github.com/rouzbehshi/MES/blob/c4267eba5ad60132a84f760f78f6d465a8aac9d6/plots/caseC_1.png"  alt="Electricity profile" title="Electricity profile" width="400" >
</p>

<p align="center">
<img src="https://github.com/rouzbehshi/MES/blob/c4267eba5ad60132a84f760f78f6d465a8aac9d6/plots/caseC_2.png"  alt="Heat profile" title="Heat profile" width="400" >
</p>

**Case D: Thermal storage with capacity equal to 4 MWh, and battery with capacity equal to 1 MWh**

<p align="center">
<img src="https://github.com/rouzbehshi/MES/blob/c4267eba5ad60132a84f760f78f6d465a8aac9d6/plots/caseD_1.png"  alt="Electricity profile" title="Electricity profile" width="400" >
</p>

<p align="center">
<img src="https://github.com/rouzbehshi/MES/blob/c4267eba5ad60132a84f760f78f6d465a8aac9d6/plots/caseD_2.png"  alt="Heat profile" title="Heat profile" width="400" >
</p>
















