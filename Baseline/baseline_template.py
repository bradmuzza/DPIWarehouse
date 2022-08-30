#%%
import pandas as pd 
import numpy as np
from sympy import N 

#%% 
df_4  = pd.read_excel(r'C:\Users\murrab01\Desktop\Strategic Investment Planning Measures_290422.xlsx', sheet_name='Outcome 2')
# %%
df_4['Key Deliverables'] = df_4['Key Deliverables related to this measure'].replace({None:'No Deliverable assigned'})
# df_4 = df_4[df_4['Recommendation'].isin(['Top 3 (for execs)','To be included']) ]
# %%

df_4 = df_4[[
    'Strategic Outcome'
  ,'Strategic Priority '
  ,'Medium Term Outcomes'
  ,'Key Deliverables'
  ,'Measures'
#,'Recommendation'
  ]]

# %%
df_Temp  =  df_4.fillna("blank")
df_Temp.groupby([
   'Strategic Outcome',
  'Strategic Priority ',
  'Medium Term Outcomes',
  'Key Deliverables',
  'Measures'
  #,'Recommendation'
  ]).count().to_excel('temp verision 1.3.xlsx')


# %%
df_4

# %%
# %%
