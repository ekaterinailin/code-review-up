#https://matplotlib.org/2.1.0/users/event_handling.html

import numpy as np
import matplotlib.pyplot as plt

#Kepler EPIC ID for the light curve I want to look at:
cluster='M44'
objectid='205071984'

#Read in data and convert to lists:

time,flux_gap,error,flux_model=np.loadtxt(objectid+'.txt',delimiter=',',unpack=True)
istart, istop=np.loadtxt(objectid+'_flares.txt',delimiter=',',unpack=True,dtype=np.dtype(np.int16))
time,flux_gap,error,flux_model,istart, istop=list(time),list(flux_gap),list(error),list(flux_model),list(istart), list(istop)


#Set up a plot with matplotlib:

A, ax =plt.subplots()
bx=ax.plot(time, flux_gap,'o',alpha=0.8, lw=0.4, picker=5) #observation
plt.errorbar(time, flux_gap,yerr=error,alpha=0.8, lw=1) #statistical error
for g,start in enumerate(istart):
	xregion=time[istart[g]:istop[g]+1]
	yregion=flux_gap[istart[g]:istop[g]+1]
	plt.plot(xregion,yregion,color='red', lw=2) #detected flares in observations
	#Shade the region where a flare is detected by Appaloosa:
	plt.axvspan(xregion[0],xregion[-1],edgecolor='black', alpha=0.2,linewidth=2)

plt.plot(time, flux_model, 'blue', lw=0.5) #model light curve from which the flare signatures deviate

#Cosmetics

plt.title('EPIC '+ objectid)
plt.xlabel('Time (BJD - 2454833 days)')
plt.ylabel(r'Flux ($e^-$ sec$^{-1}$)')

#Plot range specification

xdur0 = min(time)
xdur1 = max(time)
xdurok = np.where((time >= xdur0) & (time <= xdur1))
xdurok=xdurok[0] #xdurok is a tuple with a list: conversion needed
plt.xlim(xdur0, xdur1) 
plt.ylim(min([flux_gap[x] for x in xdurok]), max([flux_gap[x] for x in xdurok]))


#THIS IS THE INTERESTING PART!-------------------------------------------------------------
count=0
myflare_start,myflare_stop,myflare_start_flux,myflare_stop_flux=[],[],[],[]


def on_pick(event):  #event => matplotlib.backend_bases.PickEvent

	#Is there a more elegant solution instead of defining these variables as global?
	
	global count, myflare_start, myflare_stop, myflare_start_flux, myflare_stop_flux
	
	#What happens if I click on a data point:

	#Line is picked:

	thisline = event.artist #matplotlib.lines.Line2D => A line in matplotlib
	
	#The chosen data point is extracted:

	#First info for ALL data point on this line are extracted:

	xdata = thisline.get_xdata()
	ydata = thisline.get_ydata()

	#Then the specific event is chosen by index and the data are read out:

	ind = event.ind
	time = xdata[ind]
	flux = ydata[ind]
	
	#Sometimes the choice by clicking is ambiguous:

	if len(time)>1:
		print('ATTENTION!\nYou picked more than one data point at once. Try again.\nATTENTION\n')
	
	#If not, I can safely interact with the figure as I wish:

	else:
		print('onpick time:', time)

		# I only want to save flares that have START and END, so I pick events in pairs and count on the go:
		count+=1
		
		#If I only have one event, I add it to the starts of flares list:
		
		if count%2==1:

			myflare_start.append(time)
			myflare_start_flux.append(flux)

			#I also want to see the point I registered as start of a flare:

			plt.plot(myflare_start,myflare_start_flux,'o',alpha=0.8, lw=0.4,color='green')

		#If I collected two events, I can choose to save this pair as a flare and write the data into a file:

		elif count%2==0:

			myflare_stop.append(time)
			myflare_stop_flux.append(flux)

			#I also want to see the point I registered as start of a flare:

			plt.plot(myflare_stop,myflare_stop_flux,'o',alpha=0.8, lw=0.4,color='red')
			
			#Here I may trigger a save-and-proceed or remove-and-proceed event:

			print('Press \"enter\" to confirm flare events. Press \"x\" to remove.')
	
	#This command shows the changes to the figure:

	plt.draw()

	return

#If I trigger a save-and-proceed or remove-and-proceed event I end up here:

def on_key(event):

	#Again: is there a more elegant solution?

	global count, myflare_start, myflare_stop, myflare_start_flux, myflare_stop_flux

	#Here I write in my pairs of flare starts and ends:

	myflares=open(objectid+'_my_flares.txt','a')
	
	#So that you know:

	print('You pressed', event.key)
	
	#If I choose to save the marked pairs:

	if event.key=='enter':
	
		print('The following events are added to the list:\n')
		for i in range(count//2):
			line=str(myflare_start[i][0])+','+ str(myflare_stop[i][0])
			print(line)
			print()
			myflares.write(line+'\n')
	
	#Elif I choose to discard and try again:

	elif event.key=='x':

		print('The following events are removed from the list:\n')
		for i in range(count//2):

			plt.plot(myflare_stop,myflare_stop_flux,'o',alpha=0.8, lw=0.4,color='blue')
			plt.plot(myflare_start,myflare_start_flux,'o',alpha=0.8, lw=0.4,color='blue')
			plt.draw()
			line=str(myflare_start[i][0])+','+ str(myflare_stop[i][0])+'\n'
			print(line)
	
	#In any case I set back the counter and empty the lists:
	#QUESTION: 
	count=0
	myflare_start,myflare_stop,myflare_start_flux,myflare_stop_flux=[],[],[],[]
	myflares.close()
	return

#Here is where I link the interactive figure to the code:
#The FigureCanvas method mpl_connect() returns a connection id which is simply an integer.

#Connect event with string 'key_press_event' to function on_key:

cid = A.canvas.mpl_connect('key_press_event', on_key) 

#Connect event with string 'pick_event' to function on_pick:

cid2=A.canvas.mpl_connect('pick_event', on_pick)

plt.show()

