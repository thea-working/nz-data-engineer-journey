

import pandas as pd

data = {
    'order_id': [1, 2, 3, 4],
    'user_id': [101, 102, 101, 103],
    'amount': [100, 200, 150, 300],
    'country': ['NZ', 'AU', 'NZ', None]
}

df = pd.DataFrame(data)
print(df)
print(f'df.columns = {df.columns}')
print(f'df.dtypes = {df.dtypes}')
print(f'df.shape = {df.shape}')
print('*' * 60)
print(type(df['amount']))
print(type(df))
print('*' * 60)

# filter
filtered = df[df['amount'] > 150]
print(filtered)
print('*' * 60)
result = filtered.groupby('country')['amount'].sum().reset_index()
print(result)
print(df[df['amount'] > 100])
print(df[(df['amount'] > 100) & (df['country'] == 'NZ')])
print('*' * 60)

# select columns
print(df[['order_id', 'amount']])
print('*' * 60)

# group+agg
df1 = df.groupby('country').agg({
    'amount': 'sum',
    'order_id': 'count'
})
print(df1)

# sort
print(df.sort_values(by='amount', ascending=False))
print('*' * 60)

# df['amount_usd'] = df['amount'] * 0.5
print(df)

# df['country'] = df['country'].fillna('Unknown')
# print(df)
filtered = df.dropna(subset=['country'])
filtered['tax'] = filtered['amount'] * 0.1
print(filtered)
sorted_df = filtered.sort_values(by='amount', ascending=False)
print(sorted_df)
print('*' * 60)

order_df = pd.DataFrame({
    "country": ["NZ", "NZ", "AU", "AU"],
    "amount": [100, 200, 150, 300],
    "orders": [1, 2, 1, 3]
})
print(order_df)
country_agg = (
    order_df
    .groupby('country')
    .agg(
        total_amount=('amount', 'sum'),
        avg_amount=('amount', 'mean'),
        order_count=('orders', 'count')
    ).reset_index()
)
print(country_agg)
