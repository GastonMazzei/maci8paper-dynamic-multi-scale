import os,sys
import numpy as np

# Set the counter,
# instantiate a list where to keep all used values,
# and set all the available values of the risk aversion factor.
counter,LIM = 0,10
used = []
total_f = np.linspace(0.001,0.02,25)

while counter<LIM:

  # Set the transaction cost for the training database
  ct = 0.1
  #ct = np.random.choice(np.logspace(-3,1,10))

  # Set the risk aversion for the entire dataset
  f = np.random.choice(total_f)
  while f in used:
    f = np.random.choice(total_f)
  used.append(f)
  

  # Run the script that appends the period info and increase the counter
  os.system(f'python3 scripts/append_taucost_info_to_calls.py {f} {ct}')
  counter+=1


