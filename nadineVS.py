# for plotting the chart
import matplotlib.pyplot as plt
# for creating a proxy artist for the legend
import matplotlib.patches as mpatches
import pandas as pd
from sqlalchemy import *

# import seaborn as sns

engine = create_engine('sqlite:///data/ms_data.sqlite')
conn = engine.connect()

data = pd.read_sql_query('''SELECT proteins.accession, proteins.abundance, result.sample, proteins.description
FROM proteins
inner join result on result.id = proteins.result_id
inner join analysis on analysis.id = result.analysis_id
where date = '2021-02-08' AND
(description LIKE '%rdhA%'
   OR description LIKE '%rdhB%'
   OR description LIKE '%OmeA%'
   OR description LIKE '%OmeB%'
   OR description LIKE '%hupL%'
   OR description LIKE '%hupS%'
   OR description LIKE '%hupX%')
;''', conn)

conn.close()

temp = data['description'].str.split(' ', expand=True)
data['colour'] = [
    "#FA1912" if ele == 'rdhA'
    else "#FBCA0A" if ele == 'hupX'
    else "#07B0EF" if ele == 'hupS'
    else "#1A7FC4" if ele == "hupL"
    else "#08AF57" if ele == 'omeA'
    else "g" if ele == 'omeB'
    else "#F57AB1" if ele == 'rdhB'
    else " "
    for ele in temp[0]]


# create plot figure and axis to add on the bar charts
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot()
# iterate through the unique values of 'sample'
offset = 0
for g in data['sample'].unique():
    temp = data.loc[data['sample'] == g]
    # add the rows selected as a sub bar chart to the axis
    ax.bar(temp.index + offset, temp['abundance'], log=true, color=temp['colour'], label=temp['accession'])
    # add a text to print the fraction name of the fraction above the sub chart
    ax.text((((temp.tail(1).index + temp.head(1).index) // 2)[0]) - 2 + offset, temp['abundance'].max() * 1.2,
            temp['sample'].unique()[0])
    # increment offset by one so there is a space free between the groups
    offset += 1

# iterate through the how dataset
offset = 0
for i in range(len(data)):
    # if we enter a new fraction group we need to increase the offset by one
    if i > 0:
        if data['sample'][i - 1] != data['sample'][i]:
            offset += 1
    # print the 'accession' below the x axis
    plt.text(i + offset, 3900, data['accession'][i], ha='center', va='center', rotation=90)

# create a dataframe to store all unique protein groups with short descriptor (e.g. 'hupX')
# with the corresponding color
legend = pd.DataFrame()
legend['des'] = data['description'].str.split(' ', expand=True)[0].unique()
legend['color'] = [
    "#FA1912" if ele == 'rdhA'
    else "#FBCA0A" if ele == 'hupX'
    else "#07B0EF" if ele == 'hupS'
    else "#1A7FC4" if ele == "hupL"
    else "#08AF57" if ele == 'omeA'
    else "g" if ele == 'omeB'
    else "#F57AB1" if ele == 'rdhB'
    else " "
    for ele in legend['des']]
print(legend)
# create a empty patch list (search for 'Proxy artists' for more information on creating legend
# https://matplotlib.org/stable/tutorials/intermediate/legend_guide.html#sphx-glr-tutorials-intermediate-legend-guide-py
patches = []
# iterate over the rows in the above created legend df
for i, row in legend.iterrows():
    # append a new patch with the color and the descriptor of the row element
    patches.append(mpatches.Patch(color=row['color'], label=row['des']))

# create a legend based on the patch list
plt.legend(handles=patches, bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0.)

# add some space below the plot and to the right
plt.subplots_adjust(bottom=0.2, right=0.9)
# name axis
ax.set_ylabel('intensity')
# name plot
plt.title('set title here')
# show the plot
plt.show()
