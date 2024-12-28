"""
Created on Tue Mar 21 07:06:35 2023
Author: Jakub Trušina
Name: Reactions_Moment.py
"""

inpfile = r"C:\Users\trusinja\Desktop\ASTER_WORK\AG_WORK\METALLURGICAL_VALVES\Goggle_Valve_DN1300_A48799_ZMK\STUDY\external_load_gravity\RESULTS\MOMENT.txt"



import matplotlib.pyplot as plt
import pandas as pd

lookup="TABLE_SDASTER"
file_name = open(inpfile)
for num, line in enumerate(file_name,1):
        if lookup in line:
            skiprow = num
df = pd.read_csv( inpfile , sep='\s+', skiprows= skiprow ) # delimiter=" ")
print(df)
# print(df.columns.values)

group = "MOMENT_2"

df = df[df['INTITULE'] == group]

# INST = df[df['INTITULE'] == group]['INST']
INST = df["INST"]
components = ['RESULT_X', 'RESULT_Y', 'RESULT_Z', 'MOMENT_X', 'MOMENT_Y', 'MOMENT_Z']
# components = ['MOMENT_Y']

plt.close("all")
fig = plt.figure(num=None, figsize=(12, 9), dpi=80, facecolor='w', edgecolor='k')
fig.canvas.manager.set_window_title(inpfile)

for item in components:
    plt.plot(INST, df[item],'o-', markersize= 5, label = item + " = "+  str("%.6E"%((df[item].iloc[-1]))), linewidth= 3 )
    print(item + " = "+  str("%.6E"%((df[item].iloc[-1]))))  
    
num_curves = len(plt.gca().get_lines())
import matplotlib as mpl
cmap = mpl.cm.get_cmap('viridis', num_curves)
lines = plt.gca().get_lines()
for ci, line in enumerate(lines):
    line.set_color(cmap(ci))
plt.grid(linestyle= '-', linewidth= 1 ) 
plt.rc('xtick', labelsize= 14)   
plt.rc('ytick', labelsize= 14) 
plt.ylabel('$Force$' + ' $[N]$ ' +' / '+ '$Torque$' + ' $[Nmm]$ ' , fontsize = 14)
plt.xlabel('$Time$' + ' $[-]$ ' , fontsize = 14)
plt.legend(loc='best', shadow= True,  ncol=1, fontsize= 13) 
plt.grid(linestyle= '--', linewidth= 1,)
plt.tight_layout()
plt.show()






