import pandas as pd
import numpy as np
from missingpy import MissForest

# import controls and drop subject 1 and subject 24 because of many missing data
df_con = pd.read_excel("ClinicalDemogData_COFL.xlsx",sheet_name=0,skiprows=[1,24],usecols=[x for x in range (2,29)],dtype=str)
# import fallers
df_fall = pd.read_excel("ClinicalDemogData_COFL.xlsx",sheet_name=1,usecols=[x for x in range (2,29)],dtype=str)

# replace n/a with numpy nan with regex
df_con = df_con.replace(r'^n', np.NaN, regex=True)
df_fall = df_fall.replace(r'^n',np.NaN,regex=True)

# concat two dataframes of controls and fallers and make values numeric
df = pd.concat([df_con,df_fall],ignore_index=True,names=list(df_con.columns))
for i in range(27):
    df.iloc[i] = pd.to_numeric(df.iloc[i],errors='coerce')

# initiate Missforest class to impute missing data
imputer = MissForest(random_state=1)
X_clean = imputer.fit_transform(df.values)
df_clean = pd.DataFrame(X_clean.reshape(74,27),columns=list(df.columns))

# export imputed dataframe to new excel
df_clean.to_excel("Imputed Data.xlsx")