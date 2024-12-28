"""
Created on Tue Mar 21 07:06:35 2023
Author: Jakub Trušina
Name: Force_Reaction_Sum.py
"""

inpfile = r"C:\Users\trusinja\Desktop\ASTER_WORK\AG_WORK\BALL_VALVES\K92.22_DN1000_PN100_A46997\STUDY\Axisymmetric_Fluid_Pressure_Penetration\RESULTS\REAC.txt"

group_name = 'fix'
axisymmetric = 1


print_labels = 1
print_points = 1

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

if axisymmetric == 1:
    A = 2*np.pi
else: 1

lookup="TABLE_SDASTER"
file_name = open(inpfile)
for num, line in enumerate(file_name,1):
        if lookup in line:
            skiprow = num

df = pd.read_csv( inpfile , sep='\s+', skiprows= skiprow ) # delimiter=" ")
print(df.iloc[:11,1:])
# print(df[["INST","DX", "DY", "DZ"]])

df = df[(df == group_name ).any(axis=1)]
print(df)


   
INST = df["INST"]
INST = INST.to_numpy()
DX = df["DX"]
DX = DX.to_numpy() * A
DY = df["DY"]
DY = DY.to_numpy() * A
DZ = df["DZ"]
DZ = DZ.to_numpy() * A


D = np.sqrt(DX**2+DY**2+DZ**2)


plt.close("all")
fig = plt.figure(num=None, figsize=(14, 10), dpi=80, facecolor='w', edgecolor='k')
fig.canvas.manager.set_window_title(inpfile)

# plt.axes( facecolor='#DBEDFD')
plt.title( "Reaction Force of Group - " + group_name  , fontsize= 20)
plt.plot(INST, DX,'r-', label= "DX", linewidth= 3 )
plt.plot(INST, DY,'g-', label= "DY" , linewidth= 3 )
plt.plot(INST, DZ,'b-', label= "DZ"  , linewidth= 3 )
plt.plot(INST, D,'k-', label= "D"  , linewidth= 3 )

if print_points == 1:
    plt.plot(INST, DX, 'o', markersize= 5, color= 'r')
    plt.plot(INST, DY, 'o', markersize= 5, color= 'g')
    plt.plot(INST, DZ, 'o', markersize= 5, color= 'b')
    plt.plot(INST, D, 'o', markersize= 5, color= 'k')

# plt.text(INST[-1], D[-1],"  [" + str("%.2f"%(INST[-1]) ) + " ; " + str("%.0f"%(D[-1]) ) + "]", fontsize= 16)
plt.text(INST[list(D).index(max(D))] , max(D), str("%.0f"%(max(D)) )  , fontsize= 16)


fntsize = 12
if print_labels == 1:
        for kk in range(0,len(INST)):
            plt.text(INST[kk], DX[kk], "   [" + str(kk) + " ; " + str("%.2f"%(INST[kk]) ) + " ; " + str("%.0f"%(DX[kk]) ) + "]", color = "r" , fontsize= fntsize)
            plt.text(INST[kk], DY[kk], "   [" + str(kk) + " ; " + str("%.2f"%(INST[kk]) ) + " ; " + str("%.0f"%(DY[kk]) ) + "]", color = "g" , fontsize= fntsize)
            plt.text(INST[kk], DZ[kk], "   [" + str(kk) + " ; " + str("%.2f"%(INST[kk]) ) + " ; " + str("%.0f"%(DZ[kk]) ) + "]", color = "b" , fontsize= fntsize)
            plt.text(INST[kk], D[kk], "    [" + str(kk) + " ; " + str("%.2f"%(INST[kk]) ) + " ; " + str("%.0f"%(D[kk]) ) + "]", color = "k" , fontsize= fntsize)        

plt.rc('xtick', labelsize= 10)   	  # fontsize of the tick labels
plt.rc('ytick', labelsize= 10)   	  # fontsize of the tick labels
plt.ylabel('Force' + ' [N] ', fontsize = 16)
plt.xlabel('Time' + ' [s] ' , fontsize = 16)
plt.grid(linestyle= '--', linewidth= 1,)
plt.legend(loc='upper left', shadow= True, fontsize= 16)
plt.tight_layout()
plt.show()












