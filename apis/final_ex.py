import pandas as pd 
import numpy as np

data = pd.read_csv("./data/data4filter.csv")

def do_filtering(data, min_score=1, max_score=10, min_episodes=1, max_episodes=10000, min_year=1970, max_year=2023):
    return data[(data['Score'] >= min_score) & (data['Score'] <= max_score) & (data['Episodes'] >= min_episodes) & (data['Episodes'] <= max_episodes) & (data['Year'] >= min_year) & (data['Year'] <= max_year) & (data['Year'] >= min_year)]

# cb = ContentBasedRecommender()
# example = cb.recommend("Naruto")
df = pd.DataFrame(example, columns=['Id', 'model_score'])

# Merge model scoring and data
res_df = pd.merge(df, data, on="Id")

# Testing
do_filtering(res_df, min_score=7.5)