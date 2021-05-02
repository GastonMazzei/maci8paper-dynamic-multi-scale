import os,sys
import numpy as np

counter,LIM = 0,200
while counter<LIM:
  f = 0.01#np.random.choice(np.logspace(-2.5,-1.5,15))
  ct = np.random.choice(np.logspace(-4,3,3000))
  os.system(f'python3 append_taucost_info_to_calls.py {f} {ct}')
  counter+=1


