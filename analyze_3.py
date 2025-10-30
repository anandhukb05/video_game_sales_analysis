"""
Study sales over time — which years saw the most blockbuster releases?


Track sales across years.


Region wise slaes analysis by year.


"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('cleaned_data.csv')


# Ensure correct column name
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
df['year'] = df['release_date'].dt.year

df['total_sales'] = pd.to_numeric(df['total_sales'], errors='coerce')


sales_per_year = df.groupby('year')['total_sales'].sum().reset_index()
sales_per_year = sales_per_year.sort_values('year')
print(sales_per_year.head())


plt.figure(figsize=(12, 6))
plt.plot(sales_per_year['year'], sales_per_year['total_sales'], marker='o')
plt.title('Total Game Sales by Year')
plt.xlabel('Year')
plt.ylabel('Total Global Sales (in millions)')
plt.grid(True)
# plt.show()



df['year'] = df['release_date'].dt.year

# Find the top-selling game per year
top_games = (
    df.loc[df.groupby('year')['total_sales'].idxmax(), ['year', 'title', 'total_sales']]
    .sort_values('year')
)

# --- Plot ---
plt.figure(figsize=(14, 7))
bars = plt.bar(top_games['year'].astype(int), top_games['total_sales'], color='skyblue')

plt.title('Top-Selling Game by Year', fontsize=16)
plt.xlabel('Year')
plt.ylabel('Total Global Sales (Millions)')
plt.grid(axis='y', linestyle='--', alpha=0.6)

# Add game names as labels above bars
for bar, name, sales in zip(bars, top_games['title'], top_games['total_sales']):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.5,
        f"{name[:20]}...",  # truncate long names
        ha='center',
        va='bottom',
        rotation=90,
        fontsize=8
    )

plt.tight_layout()
# plt.show()

df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
df['year'] = df['release_date'].dt.year

# Drop rows without year
df = df.dropna(subset=['year'])

# Convert all sales columns to numeric
for col in ['na_sales', 'jp_sales', 'pal_sales', 'other_sales']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Group by year and sum each region's sales
yearly_sales = (
    df.groupby('year')[['na_sales', 'jp_sales', 'pal_sales', 'other_sales']]
    .sum()
    .reset_index()
    .sort_values('year')
)

plt.figure(figsize=(12, 6))

plt.plot(yearly_sales['year'], yearly_sales['na_sales'], marker='o', label='North America')
plt.plot(yearly_sales['year'], yearly_sales['pal_sales'], marker='o', label='Europe (PAL)')
plt.plot(yearly_sales['year'], yearly_sales['jp_sales'], marker='o', label='Japan')
plt.plot(yearly_sales['year'], yearly_sales['other_sales'], marker='o', label='Other Regions')

plt.title('Year-wise Game Sales by Region')
plt.xlabel('Year')
plt.ylabel('Sales (in Millions)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
