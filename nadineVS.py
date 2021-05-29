import matplotlib.pyplot as plt
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

# data.plot('accession', 'abundance', kind='bar', log=true, color=data['colour'])
# plt.show()
print(data['sample'].unique())

for g in data['sample'].unique():
    # output = pd.concat(output, data.loc[data['sample']==g])
    print(data.loc[data['sample'] == g])

"""
dataGrouped = data.groupby('sample')
group1 = dataGrouped.get_group('frac11')
group2 = dataGrouped.get_group('frac12')

plt.bar(group1.index, group1['abundance'], log=true, color=data['colour'])
plt.bar(group2.index + 1, group2['abundance'], log=true, color=data['colour'])

plt.show()
"""
for g in data['sample'].unique():
    temp = data.loc[data['sample'] == g]
    print(temp.tail(1).index + temp.head(1).index)

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot()

for g in data['sample'].unique():
    temp = data.loc[data['sample'] == g]
    ax.bar(temp.index, temp['abundance'], log=true, color=temp['colour'], label=temp['accession'])
    ax.text((((temp.tail(1).index + temp.head(1).index)//2)[0])-2, temp['abundance'].max() *1.2, temp['sample'].unique()[0])

for i in range(len(data)):
    # plt.text(i, data['abundance'][i]/2, data['accession'][i], rotation=90)
    # plt.text(i, data['abundance'][i]/2, data['accession'][i], ha = 'center', va = 'center',  rotation=90)
    plt.text(i, 3000, data['accession'][i], ha='center', va='center', rotation=90)

plt.subplots_adjust( bottom=0.2)

plt.show()
