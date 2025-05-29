import pandas as pd
import os

def extract_usernames():
    category_dir = 'category'
    for file in os.listdir(category_dir):
        if file.endswith('.csv'):
            # Read the CSV file
            df = pd.read_csv(os.path.join(category_dir, file))
            # Create new file with only usernames
            usernames_df = df[['username']]
            new_filename = f'usernames_{file}'
            usernames_df.to_csv(os.path.join(category_dir, new_filename), index=False)
            print(f"Processed {file} -> {new_filename}")

if __name__ == "__main__":
    extract_usernames() 