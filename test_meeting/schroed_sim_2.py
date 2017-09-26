import numpy as np
import csv

dx = 0.005 #spacestep size FIT dx so that it matches maximum energy etc in the later code
N_x = 1000 #number of spacesteps
dt=0.001 #timestep size
N_t= 1000 #number of timesteps
k_1 = .5 #kappas and nus from CN scheme
v_1 = .5
k_2 = .5
v_2 = .5

########DEFINE POTENTIAL########
def V(n):
	return (1-((n-N_x/2)*dx)**2)**2 # centering potential


######INITIAL CONDITION#######

#define matrix for initial conditions
A=[]

for i in range(N_x):
	A.append([])
	for j in range(N_x):
		A[i].append(0)
		if j==i:
			A[i][j]=(1-((j-N_x/2)*dx)**2)**2-2
		elif j==i+2:
			A[i][j]=1
		elif j==i-2:
			A[i][j]=1
		else:
			pass

Mat=np.array(A)
Eigval, Eigvec = np.linalg.eigh(Mat) #This seems to give results that vary from the second decimal


#####COMPUTE dx#####

#while V(N_x)+Eigval[0]<0:
#	dx = 10*dx

#doesn't work like this


#####INITIALIZE WAVE FUNCTIONS
Psi = [] #will be the computing wave function (without time and space indices)
Psi_out = [np.ndarray.tolist(np.abs(Eigvec[0]))] #will be the output wave function in space and time (csv doesn't like arrays very much)

Psi_0=Eigvec[0] #initial condition

Psi.append(Psi_0)


########CRANK NICOLSON STEP#######
###SPACE###
A = -(1j*dt)/(2*dx**2) #A_j = B_j in PDF
C = []
for i in range(N_x):
	C.append(-1+2*A-1j*dt/2*(V(i)))

F = []
F.append(0) # FIX starting value
for i in range(1,N_x-1):
	F.append(-Psi_0[i]+A*(Psi_0[i-1]-2*Psi_0[i]+Psi_0[i+1])+1j*dt/2*V(i)*Psi_0[i]) #Randwerte i=0 und i=N nicht wohldefiniert, muessen extra hinzugefuegt werden, macht aber nichts, da fuer die Funktion sowieso irgendwelche Randwerte definiert werden muessen
F.append(0) # FIX end value

###TIME###
for t in range(N_t):
	y=np.zeros(N_x,dtype=complex	) # so that it supports complex entries

	alpha = [k_1]
	beta = [v_1]

	for i in range(1,N_x-1):
		alpha.append(A/(C[i-1]-alpha[i-1]*A))
		beta.append((A*beta[i-1]+F[i-1])/(C[i-1]-alpha[i-1]*A))

	y[N_x-1] = (v_2+k_2*beta[N_x-2])/(1-k_2*alpha[N_x-2])
	for i in range(2,N_x):
		y[N_x-i]=alpha[N_x-i-1]*y[N_x-i+1]+beta[N_x-i]

	Psi.append(y)

	y_bar = np.ndarray.tolist(y)
	Psi_out.append(np.abs(y_bar))

	F=[] #compute F for the next step
	F.append(0) #FIX starting value
	for i in range(1,N_x-1):
		F.append(-Psi[t-1][i]+A*(Psi[t-1][i-1]-2*Psi[t-1][i]+Psi[t-1][i+1])+1j*dt/2*V(i)*Psi[t-1][i])
	F.append(0) # FIX end value


end_data = open('simulated_data.txt','w')
x_grid = [j for j in range(N_x)]
csv.writer(end_data).writerow(x_grid)
csv.writer(end_data).writerows(Psi_out)
end_data.close()

#Normalize
#scheme diverges -> boundary conditions? -> fixed by setting 0<kappa<1 0< nu <1
#adiabatic boundary: derivative vanishes at the boundary (see eg wikipedia crank nicolson) (to be implemented)
#FIT x range to Eigenvalue: EV = Emax = V(xmax)
