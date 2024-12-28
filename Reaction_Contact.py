"""
Created on Tue Mar 21 07:06:35 2023
Author: Jakub Trušina
Name: Contact_Reaction_Sum.py
"""



inpfile = r"C:\Users\trusinja\Desktop\ASTER_WORK\AG_WORK\BALL_VALVES\K92.22_DN1000_PN100_A46997\STUDY\Axisymmetric_Fluid_Pressure_Penetration\RESULTS\CONT.txt"



print_labels = 1
print_points = 1
axisymmetric = 1



# component_X = "RNX" ; component_Y = "RNY" ; component_Z = "RNZ" # component along DX of the normal contact reaction
# component_X = "RTAX" ; component_Y = "RTAY" ; component_Z = "RTAZ" # component along DX of the tangential force of adhesion
# component_X = "RTGX" ; component_Y = "RTGY" ; component_Z = "RTGZ" # omponent along DX of the tangential force of sliding
component_X = "RX" ; component_Y = "RY" ; component_Z = "RZ" # component along DX of the force of frictional contact (RNX+RTAX+RTGX)


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
grouped = df.groupby("INST").sum()
print(grouped.iloc[:11,8:12])
data = df.to_numpy()
INST = grouped.index.to_numpy()
RNX = grouped[component_X]
RNX = RNX.to_numpy() * A
RNY = grouped[component_Y]
RNY = RNY.to_numpy() * A
RNZ = grouped[component_Z]
RNZ = RNZ.to_numpy() * A
# RN = grouped["RN"] # Normal contact force, not magnitute!
# RN = RN.to_numpy()
RN = np.sqrt(RNX**2+RNY**2+RNZ**2)

data = np.array([RNX,RNY,RNZ,RN]).transpose()
df = pd.DataFrame(data, columns=[ "X","Y","Z","R" ])
print(df)

plt.close("all")
fig = plt.figure(num=None, figsize=(14, 10), dpi=80, facecolor='w', edgecolor='k')
fig.canvas.manager.set_window_title(inpfile)

# plt.axes( facecolor='#DBEDFD')
plt.title( "Contact Force"  , fontsize= 20)
plt.plot(INST, RNX,'r-', label= component_X, linewidth= 3 )
plt.plot(INST, RNY,'g-', label= component_Y , linewidth= 3 )
plt.plot(INST, RNZ,'b-', label= component_Z  , linewidth= 3 )
plt.plot(INST, RN, 'k-', label= "RN"  , linewidth= 3 )

if print_points == 1:
    plt.plot(INST, RNX, 'o', markersize= 5, color= 'r')
    plt.plot(INST, RNY, 'o', markersize= 5, color= 'g')
    plt.plot(INST, RNZ, 'o', markersize= 5, color= 'b')
    plt.plot(INST, RN, 'o', markersize= 5, color= 'k')

plt.text(INST[-1], RN[-1] , str("%.0f"%(RN[-1]) )  , fontsize= 16)
plt.text(INST[list(RN).index(max(RN))], max(RN), str("%.0f"%(max(RN)) )  , fontsize= 16)


fntsize = 12
if print_labels == 1:
        for kk in range(0,len(INST)):
            # plt.text(INST[kk], RNX[kk], "   [" + str(kk) + " ; " + str("%.2f"%(INST[kk]) ) + " ; " + str("%.0f"%(RNX[kk]) ) + "]", color = "r" , fontsize= fntsize)
            plt.text(INST[kk], RNY[kk], "   [" + str(kk) + " ; " + str("%.2f"%(INST[kk]) ) + " ; " + str("%.0f"%(RNY[kk]) ) + "]", color = "g" , fontsize= fntsize)
            # plt.text(INST[kk], RNZ[kk], "   [" + str(kk) + " ; " + str("%.2f"%(INST[kk]) ) + " ; " + str("%.0f"%(RNZ[kk]) ) + "]", color = "b" , fontsize= fntsize)
            # plt.text(INST[kk], RN[kk], "    [" + str(kk) + " ; " + str("%.2f"%(INST[kk]) ) + " ; " + str("%.0f"%(RN[kk]) ) + "]", color = "k" , fontsize= fntsize)        

plt.rc('xtick', labelsize= 10)   	  # fontsize of the tick labels
plt.rc('ytick', labelsize= 10)   	  # fontsize of the tick labels
plt.ylabel('Contact Force' + ' [N] ', fontsize = 16)
plt.xlabel('Time' + ' [s] ' , fontsize = 16)
plt.legend(loc='upper left', shadow= True, fontsize= 16)
plt.grid(linestyle= '--', linewidth= 1,)
plt.tight_layout()
plt.show()








