import numpy as np
import pickle
import pandas as pd
import datetime
import sys
import os

# Number of time this script is ran (starts at 0)
IX = int(sys.argv[1])

# Set random seed
rs = np.random.RandomState(
        np.random.MT19937(
            np.random.SeedSequence([123456789,
                                    987654321,
                                    135792468,
                                    864297531,
                                    789456123,
                                    987654321,
                                    000,       
                                    000,
                                    794613258,
                                    852316497,
                                    0000,      
                                    0000,
                                    134679852,
                                    258976431,
                                    00000,
                                    00000,    
                                    77788899, 
                                    99888777,
                                    44455566,
                                    66555444, 
                                    0, 
                                    0,
                                    0,
                                    0, 
                                    ][IX])))

# Define the simulation's length
Mat = 42
N = 5000

# Define a container for the results
RESULTS = {'mu':[],'a':[],'b':[],'eta':[],'rho':[],
            **{f'V_{i}':[] for i in range(Mat)},
            **{f'S_{i}':[] for i in range(Mat)},
}

# Define the "dt" (time differential)
dt = 0.001
t_block = int(1/dt)
block = Mat*t_block

# Generate two random normal samples 
N1= np.random.normal(0,1,int(block*N+1))
N2 = np.random.normal(0,1,int(block*N+1))

# Generate the total possibilities for each parameter
mu_total = np.logspace(-3,0.5,50)
a_total = np.logspace(-2,0,50)
b_total = np.logspace(-2,0,50)
eta_total = np.logspace(-2,0,50)
rho_total = np.linspace(-1,1,50)



def generate_stock_and_volatility(p, v0, n1, n2):
    """
    Integrate using Euler
        dS / S = mu dt + sqrt(V) * dW_1
        dV = a (b-V) dt + eta * sqrt(V) * dW_2
    """    
    S_local,V_local = [p[-1]],[v0]
    for i in range(block):
        V_local.append(V_local[-1] + p[1] * (p[2] - V_local[-1]) * dt + p[-3] * np.sqrt(V_local[-1]*dt) * n1[i])
        S_local.append(S_local[-1] * np.exp(-0.5*dt*V_local[-2] + np.sqrt(V_local[-2]*dt) * (p[-2]*n1[i]+np.sqrt(1-p[-2]**2)*n2[i]) )  )
    return [[V_local[t_block*i] for i in range(Mat)],
            [S_local[t_block*i] for i in range(Mat)]]



for _ in range(N):

    # Start the timer
    if _%25==0:
        if _!=0:
            tf=datetime.datetime.now()
            print(f'So far so good: average time per functional lap is {round((tf-t0).total_seconds()/COUNTER*1000,2)} ms')
            print(f'---{round(100*_/N,2)}% complete---')
        COUNTER=0
        t0=datetime.datetime.now()

    # Instantiate params
    (mu, a, b, eta, rho) = (np.random.choice(mu_total),
                            np.random.choice(a_total),
                            np.random.choice(b_total),
                            np.random.choice(eta_total),
                            np.random.choice(rho_total),
                            )

    # Also instantiate an initial price for the stock
    S0 = np.random.choice(np.logspace(-2,1,100))
    V0 = np.random.choice(np.logspace(-3.6,-0.3,100))

    # Generate a strip    
    try:
        S_temp,V_temp = generate_stock_and_volatility((mu, a, b, eta, rho, S0),V0,
                                        N1[block*_:block*(_+1)],
                                        N2[block*_:block*(_+1)],
                                        )

        if np.nan in S_temp or np.nan in V_temp: continue

        # Save the data
        RESULTS['mu']+= [mu]
        RESULTS['a']+=[a]
        RESULTS['b']+=[b]
        RESULTS['eta']+=[eta]
        RESULTS['rho']+=[rho]
        for i in range(Mat):
            RESULTS[f'S_{i}'] += [S_temp[i]]    
            RESULTS[f'V_{i}'] += [V_temp[i]]    
        
        # Increase the counter
        COUNTER += 1

    except:
        continue




# Save
with open(f'data/results{IX+1}.csv', 'a') as f:
    pd.DataFrame(RESULTS).dropna().to_csv(f, header=f.tell()==0, index=False)
