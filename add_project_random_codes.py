'''
Goal: Add random codes to the project 

'''

import pandas as pd 
import sys

df = pd.read_csv('./docs/data/Projects.tsv',sep='\t')

# Ensure no duplicate rows exists
df = df.drop_duplicates()

# Assign Code based on position starting from B2000, fitting within 5 characters (B2 + 3 digits)
# This allows for up to 1000 unique codes: B2000 to B2999
df['Assigned_Code'] = 'B2' + df.index.astype(str).str.zfill(3)


# Strip out markdown characters from the Project Description. 
df['Project description'] = df['Project description'].fillna('').str.replace(r'[_*`#]', '', regex=True)

# Double check no duplicate project descriptions exist
df['Project description'] = df['Project description'].astype(str)
if df['Project description'].duplicated().any():
    raise ValueError("Duplicate project descriptions found after cleaning.")
    sys.exit(1)
    

# Save the updated dataframe back to the file
df.to_csv('./docs/data/Projects.tsv', sep='\t', index=False)

# Rachel Parkinson

