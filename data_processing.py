import pandas as pd

df = pd.read_csv("dataset/vgchartz-2024.csv")


# removing unwanted columns
df.drop(['img', 'last_update'], axis=1, inplace=True)


# Count missing values in each column



# Fill with mean or median (numeric columns)
df["critic_score"].fillna(df["critic_score"].mean(), inplace=True)


# total_sales =	na_sales +	jp_sales + pal_sales +	other_sales
# so total_sales null columns filling with sum before that filling other columns with this relation

sales_cols = ["na_sales", "jp_sales", "pal_sales", "other_sales"]
df[sales_cols] = df[sales_cols].fillna(0)

# Fill missing total_sales using sum of 4 columns
df["total_sales"] = df.apply(
    lambda row: row["total_sales"]
    if pd.notnull(row["total_sales"])
    else row[sales_cols].sum(),
    axis=1
)

# For each row, if exactly one sales col was missing (originally),
#     infer it as total_sales - sum(other_3)
for col in sales_cols:
    mask = (df[col] == 0) & (df[sales_cols].sum(axis=1) != df["total_sales"])
    df.loc[mask, col] = df["total_sales"] - (df[sales_cols].sum(axis=1) - df[col])

# Remove rows where everything is 0 (no sales data)
df = df[~((df[sales_cols + ["total_sales"]].sum(axis=1)) == 0)]


df.dropna(inplace=True)
print(df.isnull().sum())


#checking for duplicates

# Check duplicates
print("--- duplicates ----", df.duplicated().sum())

if df.duplicated().sum()>0:
    # Remove duplicates
    df.drop_duplicates(inplace=True)

#Formatting and Standardization

#Ensures data consistency — same format, type, and units.

# Convert data types
df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
float_cols = ["critic_score",	"total_sales",	"na_sales",	"jp_sales",	"pal_sales", "other_sales"]


df[float_cols] = df[float_cols].astype(float)


str_cols = ["title","console","genre","publisher","developer"]

df[str_cols] = df[str_cols].apply(lambda x: x.str.strip())
df["console"] = df["console"].str.upper()

df.to_csv('cleaned_data.csv', index=False)

