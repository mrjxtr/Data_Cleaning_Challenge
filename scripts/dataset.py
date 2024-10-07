import os
import pandas as pd

# Loading data
script_dir = os.path.dirname(__file__)
data_path = os.path.join(script_dir, "../data/raw/data_cleaning_challenge.csv")

# Reading data into a DataFrame
df = pd.read_csv(data_path)

# Creating a copy of the DataFrame and drop unnecessary columns
df_cleaning = df.copy().drop(columns=["Unnamed: 9", "Unnamed: 10"])

# Adding column headers to the DataFrame
column_headers = [
    "Row Type",
    "Iter Number",
    "Power1",
    "Speed1",
    "Speed2",
    "Electricity",
    "Effort",
    "Weight",
    "Torque",
]
df_cleaning.columns = column_headers

# Removing rows with missing 'Row Type' and filter out header rows
df_cleaning = df_cleaning.dropna(subset=["Row Type"]).query("`Row Type` != 'Row Type'")

# Creating a list to store table numbers
table_nums = []
counter = 0

# Assigning table numbers based on 'first name' occurrences
for i in df_cleaning["Row Type"]:
    if "first name" in i:
        counter += 1
    table_nums.append(counter)

# Adding table numbers as a new column
df_cleaning["table_num"] = table_nums

# Creating a DataFrame for names
names_df = (
    df_cleaning[df_cleaning["Row Type"].str.contains("first name")]
    .drop(columns=df_cleaning.columns[3:-1])
    .rename(
        columns={
            "Row Type": "First Name",
            "Iter Number": "Last Name",
            "Power1": "Date",
        }
    )
)

# Cleaning up names data
names_df["First Name"] = names_df["First Name"].str[12:]
names_df["Last Name"] = names_df["Last Name"].str[11:]
names_df["Date"] = names_df["Date"].str[6:]

# Creating a DataFrame for values
values_df = df_cleaning[~df_cleaning["Row Type"].str.contains("first name")]

# Merge names and values DataFrames
merged_df = pd.merge(left=names_df, right=values_df, how="inner", on="table_num").drop(
    columns=["table_num"]
)

# Exporting the merged DataFrame to a CSV file
export_path = os.path.abspath(
    os.path.abspath(
        os.path.join(
            script_dir, "../data/processed/data_cleaning_challenge_cleaned.csv"
        )
    )
)
merged_df.to_csv(export_path, index=False)
print(f"Data exported successfully to {export_path[:15]}...{export_path[-35:]}")
