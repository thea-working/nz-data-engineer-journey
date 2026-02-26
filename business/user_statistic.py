# statistics based on users information

# users info
users = [
    {'id': 1, 'name': 'Alice', 'age': 25, 'country': 'NZ'},
    {'id': 2, 'name': 'Bob', 'age': 17, 'country': 'AU'},
    {'id': 3, 'name': 'Charlie', 'age': 30, 'country': 'NZ'},
    {'id': 4, 'name': 'David', 'age': 22, 'country': 'US'},
    {'id': 5, 'name': 'Eva', 'age': 19, 'country': 'UK'},
]

#just to practice python expression, ignore data amount and efficiency
#print all usernames
print('all usernames are: ', ' '.join(user['name'] for user in users))

#adults age > 20
adults = [u for u in users if u['age'] > 20]
print(f'adults: {adults}')

#nz users
nz_users = sum(1 for user in users if user['country'] == 'NZ')
print(f'nz_users: {nz_users} in total')

#find the oldest user
max_age_user = max(users, key=lambda u: u['age'])
print(f'max_age_user: {max_age_user}')


# #considering efficiency, deal with all statistic within one iterate
# adults = []
# nz_user = 0
# max_age = 0
# max_age_user = None
# print('all usernames are:')
# for user in users:
#     # print all usernames
#     print(f'{user["name"]} ', end=' ')
#     # filter users age>20
#     if user['age'] > 20:
#         adults.append(user)
#     # find the oldest user
#     if max_age_user is None or user['age'] > max_age_user['age']:
#         max_age_user = user
#     if user['country'] == 'NZ':
#         nz_user += 1
#
# print()
# print(f'adults: {adults}')
# print(f'nz_user: {nz_user} in total')
# print(f'oldest user: {max_age_user}')
