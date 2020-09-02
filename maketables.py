"""
Prospector Portal Dev
16 July 2020
From JSON list to Relational Table
"""

import pandas as pd
import os
import json

# filename variables
authors="authors.json"
authors_education="authors_education.json"
companies="companies.json"
job_history="authors_job_history.json"


# general function to read in + transform JSON list into both csv and excel sheets
def jsonListtoCSV(file,prefix):
    df = pd.read_json (file)
    print (df)
    df.to_csv(prefix+'.csv')
    df.to_excel(prefix+'.xlsx')

jsonListtoCSV(authors,'authors')
jsonListtoCSV(authors_education,"authors_education_background")
jsonListtoCSV(companies,"authors_company_history")
jsonListtoCSV(job_history,"authors_job_history")
