import numpy as np 
import matplotlib.pyplot as plt 

beta = [0.36,0.75,0.5,0.4]
theta = [21308746,7733,169272,1965868]
name = ["Structures","Battery/Cell","Electrical distribution","Solar Array Operating"]

fig,ax = plt.subplots(1,1)
T = np.arange(0.,10.01,0.01)
total = 1
for b,t,n in zip(beta,theta,name):
    ax.plot(T,np.exp(-(T/t)**b),label=n)
    total = total*np.exp(-(T/t)**b)
c = 1-np.exp(-(T/400982)**0.39)
c = 1-c*c
ax.plot(T,c ,label="Communication")
lf = 1-np.exp(-1*3*10**-5 * 24* T*365)
lf = 1-lf*lf
ax.plot(T,lf,label="Life Support")
total = total * 0.97*0.945*0.995*0.995*0.97*c*lf
ax.plot(T,total,label="Mission Reliability")
ax.set_xlim(0,1)
#ax.set_ylim(0.94,1.)
ax.set_xlabel("Time [years]")
ax.set_ylabel("Reliability")
ax.set_title("One year period")
ax.grid()
ax.legend()
plt.show()

print(total[-1])