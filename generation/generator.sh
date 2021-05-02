#!/bin/sh

# Script to generate data for the paper:
# "Delta Hedging with Transaction Costs: Dynamic Multi-Scale Strategy using Neural nets"


# **************************************PART 1********************************************************************
# Generate "results0.csv" "results1.csv" ... "resulst23.csv" files inside the "data" directory
#
# The columns are as follows:
#
# (5 heston parameters) (30 market days of a heston-modelled stock) (30 market days of a heston-modelled variance)
#
# The algorithm used to integrate the CIR-model is the Euler Maruyama algorithm

bash scripts/generatorA.sh


# **************************************PART 1********************************************************************
# Generate "results-with-C0.csv" "results-with-C1.csv" ... "resulst-with-C23.csv" files inside the "data" directory
#
# The columns are as follows:
#
# (5 heston parameters) (30 market days of a heston-modelled stock) (30 market days of a heston-modelled variance) (30 with a european call)
#
# Call's computation was implemented in https://github.com/jcfrei/Heston, according to Christian Kahl, Peter Jäckel and Roger Lord 1996

bash scripts/generatorB.sh


# **************************************PART 1********************************************************************
# Generate "results-with-C-and-D0.csv" "results-with-C-and-D1.csv" ... "resulst-with-C-and-D23.csv" files inside 
# the "data" directory
#
# The columns are as follows:
#
# (5 heston parameters) (30 market days of a heston-modelled stock) (30 market days of a heston-modelled variance) (30 with a european call) (30 with the Delta)
#
# Where the delta is defined as that which replicates the risk-neutral portfolio, 
# i.e. Pi(r,t) = Pi_0 e^(rt) = C - Delta * S
# Where C is a long European Call, in this case with initial moneyness ~0.98 and maturity 30 days  

(cd scripts; append_delta_info_to_calls.py)


# **************************************PART 1********************************************************************
# Generate "final-results.csv" inside the "data" directory
#
# The columns are as follows:
#
# (5 heston parameters) (30 stock days) (30 variance days) (30 call days) (30 delta days) (reward function for 8 different hedging periods)
#
# periods used where integer divisors of 30, i.e. 1,2,3,5,6,10,15 and 30.

python3 scripts/compute_several_costs.py

