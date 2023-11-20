import pandas as pd

keysPath = "./dataset/labels/keys.csv"
df = pd.read_csv(keysPath, index_col=None)
df['combined'] = df['Throttle Value'].astype(str) + '_' + df['Steering Value'].astype(str)

def sample_rows(group, n):
    if len(group) < n:
        return group.sample(n=n, replace=True)
    else:
        return group.sample(n=n)

df = df.groupby(['combined'], group_keys=False).apply(lambda x: sample_rows(x, int(100000/9)+1))
df = df.sample(frac=1)
df = df.reset_index(drop=True)

df_1 = df.groupby('combined', group_keys=False).apply(lambda x: x.sample(n=int(10000/9)+1))
remaining = df.drop(df_1.index)
df_1 = df_1.sample(frac=1)

df_2 = df.groupby('combined', group_keys=False).apply(lambda x: x.sample(n=int(20000/9)+1))
remaining = df.drop(df_2.index)
df_2 = df_2.sample(frac=1)

df_3 = df.groupby('combined', group_keys=False).apply(lambda x: x.sample(n=int(30000/9)+1))
remaining = df.drop(df_3.index)
df_3 = df_3.sample(frac=1)

df_4 = df.groupby('combined', group_keys=False).apply(lambda x: x.sample(n=int(40000/9)+1))
df_4 = df_4.sample(frac=1)

df_1 = df_1.drop('combined', axis=1)
df_2 = df_2.drop('combined', axis=1)
df_3 = df_3.drop('combined', axis=1)
df_4 = df_4.drop('combined', axis=1)

df_1.to_csv('./dataset/labels/keys_1.csv', index=False)
df_2.to_csv('./dataset/labels/keys_2.csv', index=False)
df_3.to_csv('./dataset/labels/keys_3.csv', index=False)
df_4.to_csv('./dataset/labels/keys_4.csv', index=False)

print("Bifurcation Done")



# TESTING

# df = df_1

# unique_values_count = df['combined'].value_counts()
# print(unique_values_count)
# print()
# print(df.head(10))
# print()
# print(df.shape)
# print()

# specified_value_col2 = '0.0_0.0'
# filtered_df = df[df['combined'] == specified_value_col2]
# unique_values_count = filtered_df['filename'].value_counts()
# print(f"Unique values and their counts in 'filename' where 'combined' is equal to {specified_value_col2}:\n{unique_values_count}")

# specified_value_col2 = '0.0_1.0'
# filtered_df = df[df['combined'] == specified_value_col2]
# unique_values_count = filtered_df['filename'].value_counts()
# print(f"Unique values and their counts in 'filename' where 'combined' is equal to {specified_value_col2}:\n{unique_values_count}")