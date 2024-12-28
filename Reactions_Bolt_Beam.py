"""
Created on Tue Mar 21 07:06:35 2023
Author: Jakub Trušina
Name: Bolt_Beam_Reactions.py
"""



inpfile = r"D:\ASTER_Results\BUTTERFLY_VALVE_DN3800PN18_A43767\LEVER_Q\R_60deg\1\REAC_BJA.txt"



sigma = 0


component = 'N'
# component = 'VY'
# component = 'VZ'
# component = 'MT'
# component = 'MFY'
# component = 'MFZ'

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

d = 40.778
# d = 14.124

A = (np.pi*d**2)/4

lookup="TABLE_SDASTER"
file_name = open(inpfile)
for num, line in enumerate(file_name,1):
        if lookup in line:
            skiprow = num
df = pd.read_csv( inpfile , sep='\s+', skiprows= skiprow ) # delimiter=" ")

print(df)

sf1 = df[(df == component ).any(axis=1)]
sf2 = sf1[(sf1 == 'MAX' ).any(axis=1)]

df = sf2
print(sf2)

value = "VALE" 
plt.close("all")
fig = plt.figure(num=None, figsize=(14, 10), dpi=80, facecolor='w', edgecolor='k')
fig.canvas.manager.set_window_title(inpfile)
if sigma == 1:
    plt.title( "Bolt Stress - value " + component  , fontsize= 20)
else: plt.title( "Bolt Force - value " + component  , fontsize= 20)
# plt.axes( facecolor='#DBEDFD')
pivoted_df = df.pivot(index='INST', columns='INTITULE', values= value)
pivoted_df.columns = [col for col in pivoted_df.columns]
pivoted_df = pivoted_df.reset_index()
collist = [ (str(pivoted_df.columns[1])[:-1] + str(ii) ) for ii in range(1,len(pivoted_df.columns)) ]
collist.insert(0,"INST")
pivoted_df = pivoted_df.reindex(columns=collist)

print(pivoted_df)
number_of_bolts = len(pivoted_df.columns) - 1


sum_of_all = 0
INST = pivoted_df["INST"]
INST = INST.to_numpy()
print(" --- " + component + " --- ")
for col in pivoted_df.columns[1:]:
    RNX = pivoted_df[col]
    RNX = RNX.to_numpy()
    if sigma == 1:
        RNX = RNX/A
    # plt.plot(INST, RNX, 'x', color="k",  linewidth= 3 )
    plt.plot(INST, RNX,'-o', markersize= 5, label = col , linewidth= 3 )
    plt.text(INST[-1], RNX[-1], str( col ) + " = " + str("%.1f"%((RNX[-1])) )  , fontsize= 16 , weight="normal", horizontalalignment='left', verticalalignment='bottom', )

    sum_of_all = sum_of_all + RNX[-1] 

ti = 1
plt.text(INST[ti], RNX[ti], str("%.1f"%((RNX[ti])) )  , fontsize= 16 , weight="normal", horizontalalignment='left', verticalalignment='bottom', )


plt.rc('xtick', labelsize= 10)   	  # fontsize of the tick labels
plt.rc('ytick', labelsize= 10)   	  # fontsize of the tick labels
if sigma == 1:
    plt.ylabel('Stress' + ' [MPa] ', fontsize = 16)
else: plt.ylabel('Force' + ' [N] ', fontsize = 16)
plt.xlabel('Time' + ' [s] ' , fontsize = 16)

num_curves = len(plt.gca().get_lines())
import matplotlib as mpl
cmap = mpl.cm.get_cmap('turbo', num_curves)
lines = plt.gca().get_lines()
for ci, line in enumerate(lines):
    line.set_color(cmap(ci))
plt.legend(loc='best', shadow= True, fontsize= 16, ncol = 2)
plt.grid(linestyle= '--', linewidth= 1,)
plt.tight_layout()
plt.show()

print("Sum of All = ", sum_of_all)
print("Average = ", sum_of_all / number_of_bolts )
print("Number of Bolts = ", number_of_bolts)

# outfile = r"C:\Users\trusinja\Desktop\MESH_LEVER\RESULTS\BOLTS___1___"
# pivoted_df.to_csv(outfile + component + ".csv") #, index=False)





