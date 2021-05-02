import pandas as pd
import numpy as np
import subprocess, os, sys
import datetime
import sys

# Open all the "results{i}.csv" files
data=[]
for x in os.listdir('../data'):
    if 'results-with-C-and-D' not in x and 'results-with-C' not in x and 'results' in x:
        data.append(pd.read_csv(f'../data/{x}'))
df = pd.concat(data)



# The fraction of the initial stock price that 
# defines the options' Strike
K = 0.9937366482139196

# The maturity using '1' as initial time
Mat = 42

# The interest rate
r = 0

# Define a key'ed container for the Call's price
C = {f'C_{i}':[] for i in range(Mat)}

# Convert the pandas dataframe to a numpy array
x = df.to_numpy()



# Define a string with the required MATLAB/Octave command
def stringer(i,j):
    return (
    #                            Call(1)   S(t)            Strike          Maturity  time   interest rate   
    f'Heston1993KahlJaeckelLordRev3(1, {x[i][5+Mat+j]}, {K*x[i][5+Mat+j]}, {Mat-1},  {j},     {r},' +
    #  dividends         "v0"         "b"        "a"       "eta"        "rho"
    f'  0,             {x[i][5]},  {x[i][2]},  {x[i][1]},  {x[i][3]},  {x[i][4]}), '
    )




# Define the MATLAB/Octave call evaluator
def return_call_value(i):
    # Define the command to run
    command = 'octave --eval "'
    for j in range(Mat):
        command += stringer(i,j)
    command += '"'
    try:
        output = subprocess.run(
        command,
        shell=True, 
        text=True,
        capture_output=True
        )
        print(output.stderr)
        if 'Err' not in output.stderr:
            return output.stdout
        else:
            # Octave script failed
            return False
    except Exception as ins:
        # An unexpected error occurred
        return False


# Compute the call values for each time
L = len(x)
for i in range(L):
    fail = False
    answer = return_call_value(i)
    if not answer:
        fail = True
    else: 
        answer = answer.split('\n')
    for j in range(Mat):            
        if fail:
            C[f'C_{j}'] += [np.nan]
        else:
            C[f'C_{j}'] += [float(answer[j].split('=')[1])]
    print(f'{i} of {L} complete ({round(100*i/L,2)})')

# Save
pd.concat([df,pd.DataFrame(C)],axis=1).dropna().to_csv(f'../data/results-with-C{IX+1}.csv', index=False)
