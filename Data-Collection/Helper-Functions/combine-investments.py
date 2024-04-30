import pandas as pd
import os

def combine_investments(dir_path, output_file):
   
    combined_df = pd.DataFrame()

    for file_name in os.listdir(dir_path):
        if file_name.endswith('.csv'): 
            file_path = os.path.join(dir_path, file_name)
            source = file_name.split('.')[0]  

            df = pd.read_csv(file_path)

            #
            df['Source'] = source

            combined_df = pd.concat([combined_df, df], ignore_index=True)

    result_df = combined_df.groupby('Name').agg(
        Total_investment=pd.NamedAgg(column='Amount', aggfunc='sum'),
        UCRP_Amount=pd.NamedAgg(column='Amount', aggfunc=lambda x: sum(x[combined_df['Source'].str.startswith('UCRP')])),
        GEP_Amount=pd.NamedAgg(column='Amount', aggfunc=lambda x: sum(x[combined_df['Source'].str.startswith('GEP')])),
    ).reset_index()

    
    result_df.to_csv(output_file, index=False)

dir_path = 'Data-Collection/Helper-Functions/individual-fund-outputs'
output_file = 'Data-Collection/Helper-Functions/combined-output/combined_investments.csv'
combine_investments(dir_path, output_file)
