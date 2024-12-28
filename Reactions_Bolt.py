"""
Created on Tue Mar 21 07:06:35 2023
Author: Jakub Trušina
Name: Bolt_Reactions.py
"""
import os

file_name = "BJ_A"
folder_name = r"C:\Users\trusinja\Desktop\ASTER_WORK\AG_WORK\GATE_VALVES\S33.6_NPS10_Class600\STUDY\F_max\RESULTS"

inpfile = os.path.join(folder_name, file_name + ".txt" )

sigma = 0
d_out = 58 ; d_in = 18



t_1 = 0
time_1 = 1.0

print_labels = 0

# component = "DX" 
# component = "DY" 
# component = "DZ"
component = "D" 

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

A = (np.pi*(d_out**2-d_in**2))/4

lookup="TABLE_SDASTER"
file_name = open(inpfile)
for num, line in enumerate(file_name,1):
        if lookup in line:
            skiprow = num
df = pd.read_csv( inpfile , sep='\s+', skiprows= skiprow ) # delimiter=" ")
df["D"]= np.sqrt(df["DX"]**2 + df["DY"]**2 + df["DZ"]**2)

plt.close("all")

plt.style.use("dark_background")
for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
    plt.rcParams[param] = '0.9'  # very light grey
for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
    plt.rcParams[param] = '#212946'  # bluish dark grey
plt.rcParams['axes.edgecolor'] = "2A3459" # '#2A546D'

fig = plt.figure(num=None, figsize=(13,9), dpi=80 )
fig.canvas.manager.set_window_title(inpfile)
if sigma == 1:
    plt.title( "Bolt Stress - component " + component  , fontsize= 20)
else: plt.title( "Bolt Force - component " + component  , fontsize= 20)
# plt.axes( facecolor='#DBEDFD')
pivoted_df = df.pivot(index='INST', columns='INTITULE', values= component)
pivoted_df.columns = [col for col in pivoted_df.columns]
pivoted_df = pivoted_df.reset_index()
collist = [ (str(pivoted_df.columns[1])[:-1] + str(ii) ) for ii in range(1,len(pivoted_df.columns)) ]
collist.insert(0,"INST")
pivoted_df = pivoted_df.reindex(columns=collist)
print(pivoted_df)

print(pivoted_df)
number_of_bolts = len(pivoted_df.columns) - 1


sum_of_all = 0
INST = pivoted_df["INST"]
INST = INST.to_numpy()
print(" --- " + component + " --- ")
for col in pivoted_df.columns[1:]:
    RNX = pivoted_df[col]
    RNX = RNX.to_numpy()  / 1000 # kN
    if sigma == 1:
        RNX = RNX/A
    plt.plot(INST, RNX,'o-', markersize= 5, label = col , linewidth= 3 )
    plt.text(INST[-1], RNX[-1], str( col ) + " = " + str("%.3f"%((RNX[-1])) )  , fontsize= 16 , weight="normal", horizontalalignment='left', verticalalignment='bottom', )
    plt.text(INST[-1], RNX[-1], str( col )  , fontsize= 16 , weight="normal", horizontalalignment='left', verticalalignment='bottom', )
    
    if print_labels == 1:
        for kk in range(0,len(INST)):
            plt.text(INST[kk], RNX[kk], str("%.1f"%((RNX[kk])) )  , fontsize= 16 , weight="normal", horizontalalignment='left', verticalalignment='bottom', )

    idx1 = [list(INST).index(time_1)]
    plt.text(INST[idx1], RNX[idx1], str("%.3f"%((RNX[idx1])) )  , fontsize= 16 , weight="normal", horizontalalignment='left', verticalalignment='bottom', )
    plt.text(INST[t_1], RNX[t_1], str("%.3f"%((RNX[t_1])) )  , fontsize= 16 , weight="normal", horizontalalignment='left', verticalalignment='bottom', )
    
    sum_of_all = sum_of_all + RNX[-1]

plt.rc('xtick', labelsize= 10)   	  # fontsize of the tick labels
plt.rc('ytick', labelsize= 10)   	  # fontsize of the tick labels
if sigma == 1:
    plt.ylabel('Stress' + ' [MPa] ', fontsize = 16)
else: plt.ylabel('Force' + ' [kN] ', fontsize = 16)
plt.xlabel('Time' + ' [s] ' , fontsize = 16)

num_curves = len(plt.gca().get_lines())
import matplotlib as mpl
cmap = mpl.cm.get_cmap('coolwarm_r', num_curves)
lines = plt.gca().get_lines()
for ci, line in enumerate(lines):
    line.set_color(cmap(ci))

plt.legend(loc='best', shadow= True,  ncol=1, fontsize= 14)
plt.tight_layout()
plt.grid(linestyle= '--', linewidth= 1, color='#2A3459')
plt.show(block= False )  
fig.canvas.draw() 
plt.style.use("default")


print("Sum of All = ", sum_of_all)
print("Average = ", sum_of_all / number_of_bolts )
print("Number of Bolts = ", number_of_bolts)

# outfile = r"D:\ASTER_Results\RESULTS_TEST_P20\RQ_1\BOLTREAC___1___"
# pivoted_df.to_csv(outfile + component + ".csv") #, index=False)



