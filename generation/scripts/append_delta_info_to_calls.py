import pandas as pd
import numpy as np
import subprocess, os, sys
import datetime
import sys

# Number of time this script is ran (starts at 0)
IX = int(sys.argv[1])

# Open the file with the info
data=[]
for x in os.listdir('data'):
    if 'results-with-C-and-D' not in x and 'results-with-C' in x:
        data.append(pd.read_csv(f'data/{x}'))
df = pd.concat(data)



# State the maturity 
Mat=42

# Filter huge values
MIN,MAX = 1e-4,1e3
for l in ['C','S','V']:
    for i in range(Mat):
        df=df[(df[f'{l}_{i}']>MIN)&(df[f'{l}_{i}']<MAX)]

# Set a value fo the portfolio
Pi = 0.95

# Set the rate
r=0.001

# Scale the portfolio
Pi = [Pi * np.exp(r*t/(Mat-1)) for t in range (Mat)]


# Set a column for the portfolio
for i in range(Mat):
    df[f'P_{i}']= Pi[i]


# Set a column for the Delta
#
# Pi(t) = C(t) - Delta(t) S(t)
# 
# so... 
#       Delta(t) = [C(t)-Pi(t)]/S(t)
#
for i in range(Mat):
    df[f'D_{i}']= (df[f'C_{i}'] - df[f'P_{i}'])/df[f'S_{i}']


# Filter diverging values for Delta
print(f'BEFORE FILTERING DELTA, DATASET\'S SIZE IS: ',df.shape)
MIN,MAX = 1e-4,2e3
for l in ['D']:
    for i in range(Mat):
        df=df[(df[f'{l}_{i}'].apply(abs)>MIN)&(df[f'{l}_{i}'].apply(abs)<MAX)]
print(f'AFTER FILTERING DELTA, DATASET\'S SIZE IS: ',df.shape)


# Save
df.to_csv(f'data/results-with-C-and-D{IX}.csv')











