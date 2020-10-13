import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#   Retrieve data from xlsx file

Cell= pd.read_excel("data.xlsx")
arr=[]
frequency=[110,111,112,113,114,115]

#   Assign the First Cell as the starting cell in this case A

for index, row in Cell.iterrows():
    arr.append(np.sqrt((row['Long']-Cell['Long'].iloc[0])**2+(row['Lat']-Cell['Lat'].iloc[0])**2))

#   Sort DF based on the closest values to the starting point

Cell['distance']=arr
Cell=Cell.sort_values(by=['distance'])

frqselect=pd.DataFrame()
pointdistance=[]

#   Loop through all the cells 

for index, row in Cell.iterrows():

    if(row['distance']==0):
        frqselect = frqselect.append({'Cell ID': row['Cell ID'],'Long': row['Long'],'Lat': row['Lat'],'Frequency': frequency[0]},ignore_index=True)
        
    else:
        closestfreq=pd.DataFrame()
        for k in frequency:
            temp=frqselect[frqselect['Frequency']==k]
            
            #   If an empty DF is returned it means the frequency has not yet been used and the
            #   closest cell with that frequency can be set to 0

            if not (temp.empty):

                for index1, row1 in temp.iterrows():
                    temp.at[index1,'distance']=np.sqrt((row['Long']-row1['Long'])**2+(row['Lat']-row1['Lat'])**2)

                temp=temp.sort_values(by=['distance'])
                closestfreq= closestfreq.append({'frequency': k,'distance':temp['distance'].iloc[0]}, ignore_index=True)
                
            else:
                closestfreq= closestfreq.append({'frequency': k,'distance':0}, ignore_index=True)
               
                
        #   If there is not yeas a cell operating on this frequency assign it to the cell
        #   Else locate for every frequency the closest cell and assign a frequency based 
        #   on the furthest cell of all the six frequencies 

        if (closestfreq['distance'].min()==0):
            minimum=closestfreq['distance'].min()
            closestfreq=closestfreq[closestfreq['distance']==minimum].iloc[0]
            frqselect = frqselect.append({'Cell ID': row['Cell ID'],'Long': row['Long'],'Lat': row['Lat'],'Frequency': closestfreq['frequency']},ignore_index=True)
        else:
            maximum=closestfreq['distance'].max()
            closestfreq=closestfreq[closestfreq['distance']==maximum].iloc[0]
            frqselect = frqselect.append({'Cell ID': row['Cell ID'],'Long': row['Long'],'Lat': row['Lat'],'Frequency': closestfreq['frequency']},ignore_index=True)

#   Assign a color to every cell based on the frequency it uses       
t=[]
for index, row in frqselect.iterrows():
    t.append(row['Frequency'])
    
#   Print the results of the frequencies that was assigned to the cell

print(frqselect.sort_values(by=['Cell ID'],ignore_index=True))


#   Plot the cells and their assigned frequencies

fig, ax = plt.subplots()
scatter=ax.scatter(frqselect['Lat'], frqselect['Long'],s=100,c=t,cmap='rainbow')
ax.legend(*scatter.legend_elements(),title="Frequencies")
plt.axis('equal')
plt.show()
