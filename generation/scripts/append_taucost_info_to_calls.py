# Imports
import numpy as np 
import pandas as pd 
import sys, os

import matplotlib.pyplot as plt

# Open the files
data=[]
for x in os.listdir('data'):
    if 'results-with-C-and-D' in x: 
        data.append(pd.read_csv(f'data/{x}'))
df = pd.concat(data)
df_days = pd.read_csv('real-data/marchprice.csv')

# Correct an index error in the database
for s in ['S','C','P','D']:
    df[f'{s}_42'] = df[f'{s}_41']

# Store the days that are "trading days"
td = df_days.days.tolist()

# Define a transaction cost, eg 0.005 means 0.5%
f=float(sys.argv[1])

# Compute the actual days per period
days ={}
for T in [1, 2, 3, 5, 6, 10, 15, 30]:
    days[T]= df_days['days'].to_numpy()[[i*T for i in range(int(round(30/T,0))+1) if i*T<=29]].tolist()

# Fix the last day that isnt appended in some cases
days[5].append(40)
days[6].append(40)
days[10].append(42)
days[15].append(42)
days[30].append(42)

# Define a constant to make the solution non-singular?
#Constant = df['P_41']
Constant = float(sys.argv[2])

# Iterate appending the cost of all possible periods
for T in [1, 2, 3, 5, 6, 10, 15, 30]:
    df[f'cost_{T}'] = (df['P_41'] * (1-f) - 
                        f * sum(
                                [(df[f'S_{days[T][i+1]}'] * 
                                  abs(df[f'D_{days[T][i]}']-df[f'D_{days[T][i+1]}'])
                                ) for i in range(len(days[T])-1)]
                            )
                        )

    df[f'cost_{T}'] = df[f'cost_{T}'] / (
                            Constant +
                            sum([
                              sum([(
                                   (df[f'D_{days[T][i]}'] - df[f'D_{days[T][i]}'] * df[f'S_{days[T][i]}']) -  
                                   (df[f'D_{t}'] - df[f'D_{t}'] * df[f'S_{t}'])
                                  )**2 for t in td if t>=days[T][i] and t<days[T][i+1]])
                             for i in range(len(days[T])-1)]).apply(np.sqrt)
                    ) * np.sqrt(len(td)-len(days[T]))

    df[f'cost_{T}'] = df[f'cost_{T}'] * -1

# Save and Plot
if True:
    df.to_csv('data/final-database.csv', index=False)
    plt.hist(np.argmax(df.iloc[:,-8:].to_numpy(),1))
    plt.xticks(range(8), [str(x) for x in [1,2,3,5,6,10,15,30]])
    plt.show()

# Store the results in a new .CSV to plot how the cost function may vary
else:
    unique, counts = np.unique(np.argmin(df.iloc[:,-8:].to_numpy(),1), return_counts=True)
    countsdf = pd.DataFrame({ 'const':[Constant], 'f':[f]})
    for i in range(8):
        if i in unique:
            countsdf[i] = counts[np.argmin(np.where(unique==i,0,1))]
        else:
            countsdf[i] = np.nan
    with open('data/cost-vs-f.csv', 'a') as f:
        countsdf.to_csv(f, mode='a', header=f.tell()==0)


