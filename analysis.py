import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
"""


Find top-selling games globally and regionally.


Compare sales performance between regions.(bar chart)

Identify which console/platform contributes most to total sales.


Check which publishers or developers dominate global sales.


Analyze genre popularity (e.g., Action vs. Shooter vs. Adventure).


Which console has the highest total sales?


Which genre performs best globally?


How do Japanese sales compare to North American sales for top games?


"""

df = pd.read_csv('cleaned_data.csv')




#Find top-selling games globally and regionally.
print(df.loc[df['total_sales'].idxmax(), 'title'])
print(df.loc[df['na_sales'].idxmax(), 'title'])
print(df.loc[df['jp_sales'].idxmax(), 'title'])
print(df.loc[df['pal_sales'].idxmax(), 'title'])

#Compare sales performance between regions.
region_sales = {
    'North America': df['na_sales'].sum(),
    'Japan': df['jp_sales'].sum(),
    'Europe & Africa (PAL)': df['pal_sales'].sum(),
    'Other': df['other_sales'].sum()
}

# Step 2: Convert to DataFrame
# region_df = pd.DataFrame(list(region_sales.items()), columns=['Region', 'Total_Sales'])
# region_df = region_df.sort_values('Total_Sales', ascending=False)

# # Step 3: Plot with Seaborn
# plt.figure(figsize=(8, 5))
# sns.barplot(data=region_df, x='Region', y='Total_Sales', palette='viridis')

# # Step 4: Label the chart
# plt.title('Global Game Sales by Region', fontsize=14, fontweight='bold')
# plt.xlabel('Region', fontsize=12)
# plt.ylabel('Total Sales (millions)', fontsize=12)

# # Show values on bars
# for i, v in enumerate(region_df['Total_Sales']):
#     plt.text(i, v + 5, f"{v:.1f}", ha='center', fontweight='bold')

# plt.tight_layout()
# plt.show()



# Identify which console/platform contributes most to total sales.

print(df.loc[df['total_sales'].idxmax(), 'console'])

# Check which publishers or developers dominate global sales.
print(df.loc[df['total_sales'].idxmax(), 'publisher'])
print(df.loc[df['total_sales'].idxmax(), 'developer'])

genre_sales = df.groupby("genre")["total_sales"].sum().sort_values(ascending=False)

# Plot
# plt.figure(figsize=(10,5))
# sns.barplot(x=genre_sales.index, y=genre_sales.values, palette="viridis")
# plt.title("Genre Popularity by Total Global Sales (in millions)")
# plt.xlabel("Genre")
# plt.ylabel("Total Sales (Millions)")
# plt.xticks(rotation=45)
# plt.show()

#How do Japanese sales compare to North American sales for top games?
top_games = df.nlargest(10, 'total_sales')[['title', 'na_sales', 'jp_sales']]
print("====", top_games)
plt.figure(figsize=(12,6))
sns.barplot(data=top_games.melt(id_vars='title', 
                                value_vars=['na_sales', 'jp_sales'],
                                var_name='Region', 
                                value_name='Sales'),
            x='title', y='Sales', hue='Region', palette='Set2')

plt.title("Japanese vs North American Sales for Top 10 Games")
plt.xlabel("Game Title")
plt.ylabel("Sales (in millions)")
plt.xticks(rotation=45, ha='right')
plt.legend(title="Region")
plt.tight_layout()
#  plt.show()