# %%

import pandas as pd
import dateparser

def infer_and_convert_data_types(df):
    for col in df.columns:
        # Attempt to convert to numeric first
        df_converted = pd.to_numeric(df[col], errors='coerce')
        if not df_converted.isna().all():  # If at least one value is numeric
            df[col] = df_converted
            continue

        # Attempt to convert to datetime
        df_date_converted = pd.to_datetime(df[col], errors='coerce')
        # consider this col as date if at least one value is date
        if not df_date_converted.isna().all():
            df[col] = df[col].apply(lambda x: dateparser.parse(str(x)))
            # df[col] = df[col].apply(lambda x: x.isoformat() if pd.notnull(x) else 'NaT')
            
            continue
        
         # Check if the column should be boolean
        unique_values = set(df[col].dropna().unique())
        if unique_values.issubset({True, False, 1, 0, 'True', 'False', 'true', 'false'}):
            df[col] = df[col].apply(lambda x: True if str(x).lower() in ['true', '1'] else False)
            continue

        # Check if the column should be categorical
        if len(df[col].unique()) / len(df[col]) < 0.5:  # Example threshold for categorization
            df[col] = pd.Categorical(df[col])
            continue
        
        # If no conversion was possible, consider the column as string
        # Keep only alphanumeric characters, spaces, commas, and periods
        df[col] = df[col].str.replace(r'[^a-zA-Z0-9.,\s]', '', regex=True)
        
        # Remove any extra spaces
        df[col] = df[col].str.replace(r'\s+', ' ', regex=True).str.strip()
        
    print('>>>>> df')
    print(df)
    return df

# # Test the function with your DataFrame
# df = pd.read_csv('sample_data.csv')
# # print("Data types before inference:")
# # print(df.dtypes)

# df = infer_and_convert_data_types(df)

# print("\nData types after inference:")
# print(df.dtypes)

# # %%
