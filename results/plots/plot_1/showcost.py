import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import gamma

f,ax = plt.subplots(1,2,figsize=(10,5))

x = pd.read_csv('cost-vs-f.csv')
print('original x shape is', x.shape)
x=x.dropna()
print('but after dropping nan rows it\'s', x.shape)
domain = [1,2,3,5,6,10,15,30]

print(x.head())

print('x shape is', x.shape)
x=x.to_numpy()[:,-len(domain):]/409
print('new x shape is', x.shape)

for i in range(len(x)):
    ax[0].scatter(domain,x[i,:],c='k')
    if i==len(x)-1:
        ax[0].plot(domain,x[i,:],c='k',lw=2,alpha=1,ls='-',label='simulation')
    else:
        ax[0].plot(domain,x[i,:],c='k',lw=2,alpha=0.3,ls=':')
ax[0].grid()


# Is it a poisson?
# from scipy.stats import poisson
# mu = np.sum([np.mean(x[:,i])*y for i,y in enumerate(domain)]) 
# print('mu is',mu)
# fdomain = np.linspace(min(domain),max(domain),30)
# ax[0].plot(fdomain, poisson.pmf(fdomain, mu), 'r', 
# #ms=8,
# label='poisson',lw=3,alpha=0.7)


# Regular fit
# import numpy as np
# import matplotlib.pyplot as plt
# import scipy.stats
# import scipy.optimize
# tot=len(x)
# dist = [scipy.stats.norm, scipy.stats.lognorm][0]
# y,x = x[:tot,:].flatten(),[j+np.random.rand()*0.1 for j in domain]*tot
# def tri_norm(x, *args):
#     m1, m2, s1, s2, k1, k2, m3,s3,k3 = args
#     ret = k1*dist.pdf(x, loc=m1 ,scale=s1)
#     ret += k2*dist.pdf(x, loc=m2 ,scale=s2)
#     ret += k3*dist.pdf(x, loc=m3 ,scale=s3)
#     return ret
# params = [1,5,1,3,0.3,0.3, 8,2,0.3]
# fitted_params,_ = scipy.optimize.curve_fit(tri_norm,x, y, p0=params, maxfev=10000)
# fp=fitted_params
# #xx = np.linspace(np.min(x), np.max(x), 1000)
# fdomain = np.linspace(min(fdomain), max(fdomain), 200)
# ax[0].plot(fdomain, tri_norm(fdomain, *fitted_params),c='dodgerblue',
# label='triple gaussian',lw=3,alpha=0.7)
# ax[1].fill_between(fdomain, 0, scipy.stats.norm.pdf(fdomain,
#  loc=fitted_params[0],scale=fitted_params[2]), 
#  color='dodgerblue',label=f'mu= {round(fp[0],1)}, sigma={round(fp[2],1)}, weight={round(fp[4],1)}',
#  alpha=fitted_params[4]/(max([fp[4],fp[5],fp[-1]])/0.5),
#  )
# ax[1].fill_between(fdomain, 0, scipy.stats.norm.pdf(fdomain,
#  loc=fitted_params[1],scale=fitted_params[3]), 
#  color='dodgerblue',
#  alpha=fitted_params[5]/(max([fp[4],fp[5],fp[-1]])/0.5), label=f'mu= {round(fp[1],1)}, sigma={round(fp[3],1)}, weight={round(fp[5],1)}',
#  )
# ax[1].fill_between(fdomain, 0, scipy.stats.norm.pdf(fdomain,
#  loc=fitted_params[-3],scale=fitted_params[-2]), 
#  color='dodgerblue',label=f'mu= {round(fp[-3],1)}, sigma={round(fp[-2],1)}, weight={round(fp[-1],1)}',
#  alpha=fitted_params[-1]/(max([fp[4],fp[5],fp[-1]])/0.5),
#  )
# print('fitted params are', fitted_params)


for axy in [ax[0],ax[1]]:
    axy.set_xscale('log')
    axy.set_xticks(domain)
    axy.set_xticklabels([str(x) for x in domain])
    axy.legend()
plt.show()