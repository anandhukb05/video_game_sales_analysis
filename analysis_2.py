


"""


Analyze correlation between critic_score and total_sales.



Which publishers/developers consistently make highly rated games?
Is there a strong relationship between critic score and sales?


Are Rockstar Games titles rated higher on average than Activision’s?

"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('cleaned_data.csv')

sns.scatterplot(data=df, x="critic_score", y="total_sales", hue="genre")
plt.legend(title="Genre", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
# plt.show()


publisher_counts = df['publisher'].value_counts()
developer_counts = df['developer'].value_counts()

# Keep only publishers/developers with at least 5 games (you can adjust)
top_publishers = df.groupby('publisher').filter(lambda x: len(x) >= 5)
top_developers = df.groupby('developer').filter(lambda x: len(x) >= 5)
publisher_avg = top_publishers.groupby('publisher')['critic_score'].mean().sort_values(ascending=False)
developer_avg = top_developers.groupby('developer')['critic_score'].mean().sort_values(ascending=False)


plt.figure(figsize=(10,6))
sns.barplot(x=publisher_avg.head(10).values, y=publisher_avg.head(10).index, palette="crest")
plt.title("Top 10 Publishers by Average Critic Score")
plt.xlabel("Average Critic Score")
plt.ylabel("Publisher")
plt.show()