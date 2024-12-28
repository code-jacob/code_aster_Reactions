"""
Created on Tue Mar 21 07:06:35 2023
Author: Jakub Trušina
Name: Reactions_All.py
"""

inpfile = r"C:\Users\trusinja\Desktop\ASTER_WORK\AG_WORK\GATE_VALVES\S33.6_NPS10_Class600\STUDY\F_max_cyclic\RESULTS_1\BJ_A.txt"
inpfile = r"C:\Users\trusinja\Desktop\ASTER_WORK\AG_WORK\GATE_VALVES\S33.6_NPS10_Class600\STUDY\F_max_cyclic_gasket\RESULTS\BJ_A.txt"

# component = "DX" 
component = "DY" 
# component = "DZ" 
# component = "D" 

t_1 = 0
time_1 = 1
print_labels = 0

axisymmetric = 0
symmetry = 2

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import io

lines = []
with open(inpfile, 'r') as input_file:
    for line in input_file:
        if 'FORC_NODA' in line or 'REAC_NODA' in line:
            lines.append(line.strip()) 
df1 = pd.read_csv(io.StringIO('\n'.join(lines)), sep='\s+', header=None)
print(df1)

lookup="TABLE_SDASTER"
file_name = open(inpfile)
for num, line in enumerate(file_name,1):
        if lookup in line:
            skiprow = num
df = pd.read_csv( inpfile , sep='\s+', skiprows= skiprow ) # delimiter=" ")
df1.columns = df.columns.values
# print(df.columns.values)
df = df1
# df["D"]= np.sqrt(df["DY"]**2 + df["DZ"]**2)
df["D"]= np.sqrt(df["DX"]**2 + df["DY"]**2 + df["DZ"]**2)
print(df)

print(df[["INTITULE", "INST", "DX", "DY", "DZ"]])
# print(df)

plt.close("all")
plt.style.use("dark_background")
for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
    plt.rcParams[param] = '0.9'  # very light grey
for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
    plt.rcParams[param] = '#212946'  # bluish dark grey
plt.rcParams['axes.edgecolor'] = "2A3459" # '#2A546D'
fig = plt.figure(num=None, figsize=(13,9), dpi=80 )
fig.canvas.manager.set_window_title(inpfile)

if axisymmetric == 1:
    plt.title( "Reaction Force - component " + component  + " - Axisymmetric", fontsize= 20, fontweight="bold" )
elif axisymmetric != 1:
    plt.title( "Reaction Force - component " + component  + " - Symmetry = " + "1/"+str(symmetry), fontsize= 20, fontweight="bold" )
else: plt.title( "Reaction Force - component " + component  , fontsize= 20)
    
pivoted_df = df.pivot(index='INST', columns='INTITULE', values= component)
pivoted_df.columns = [col for col in pivoted_df.columns]
pivoted_df = pivoted_df.reset_index()
print("\n", pivoted_df)


INST = pivoted_df["INST"]
INST = INST.to_numpy()
print(" --- " + component + " --- ")
for col in pivoted_df.columns[1:]:
    RNX = pivoted_df[col]
    RNX = RNX.to_numpy()
    if axisymmetric == 1:
        RNX = RNX*2*np.pi
    if symmetry != 1:
        RNX = RNX*symmetry
    idx1 = [list(INST).index(time_1)]
    plt.plot(INST, RNX,'o-', markersize= 5, label = col +" = "+  str("%.1f"%((RNX[idx1]))), linewidth= 3 )
    plt.text(INST[-1], RNX[-1], str( col ) + " = " + str("%.1f"%((RNX[-1])) )  , fontsize= 16 , weight="normal", horizontalalignment='left', verticalalignment='bottom', )
    plt.text(INST[t_1], RNX[t_1], str("%.1f"%((RNX[t_1])) )  , fontsize= 16 , weight="normal", horizontalalignment='left', verticalalignment='bottom', )
    plt.text(INST[idx1], RNX[idx1], str("%.1f"%((RNX[idx1])) )  , fontsize= 16 , weight="normal", horizontalalignment='left', verticalalignment='bottom', )
    
    
    fntsize = 12
    if print_labels == 1:
            for kk in range(0,len(INST)):
                plt.text(INST[kk], RNX[kk], "   [" + str(kk) + " ; " + str("%.2f"%(INST[kk]) ) + " ; " + str("%.0f"%(RNX[kk]) ) + "]", color = "k" , fontsize= fntsize, horizontalalignment='right', verticalalignment='bottom')


plt.rc('xtick', labelsize= 10)   	  # fontsize of the tick labels
plt.rc('ytick', labelsize= 10)   	  # fontsize of the tick labels
plt.ylabel('Force' + ' [N] ', fontsize = 16)
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















