# statistics based on users information
from collections import Counter


# # users info
# users = [
#     {'id': 1, 'name': 'Alice', 'age': 25, 'country': 'NZ'},
#     {'id': 2, 'name': 'Bob', 'age': 17, 'country': 'AU'},
#     {'id': 3, 'name': 'Charlie', 'age': 30, 'country': 'NZ'},
#     {'id': 4, 'name': 'David', 'age': 22, 'country': 'US'},
#     {'id': 5, 'name': 'Eva', 'age': 19, 'country': 'UK'},
# ]
# #
# # #just to practice python expression, ignore data amount and efficiency
# # #print all usernames
# # print('all usernames are: ', ' '.join(user['name'] for user in users))
# #
# # #adults age > 20
# # adults = [u for u in users if u['age'] > 20]
# # print(f'adults: {adults}')
# #
# # #nz users
# # nz_users = sum(1 for user in users if user['country'] == 'NZ')
# # print(f'nz_users: {nz_users} in total')
# #
# # #find the oldest user
# # max_age_user = max(users, key=lambda u: u['age'])
# # print(f'max_age_user: {max_age_user}')
#
# # Simulate SQL: SELECT country, COUNT(*) FROM users GROUP BY country
# country_count = {}  # {'country':'NZ','count':2}
# adult_count = 0
# for user in users:
#     # country count
#     country = user['country']
#     country_count[country] = country_count.get(country, 0) + 1
#
#     # adult count
#     if user['age'] >= 18:
#         adult_count += 1
# minor_count = len(users) - adult_count
#
# print('country_count:', country_count)
# print('adult count:', adult_count)
# print('minor count:', minor_count)
#
# # improvement
# from collections import Counter
#
# country_counts = Counter(user['country'] for user in users)
# print('country_counts:', country_counts)
# print(country_counts.most_common(1))
#
#
# def age_bucket(age):
#     if age < 18:
#         return "Under 18"
#     elif 18 <= age <= 25:
#         return "18-25"
#     elif 26 <= age <= 35:
#         return "26-35"
#     else:
#         return "36+"
#
#
# age_distribution = Counter(age_bucket(user['age']) for user in users)
# print("Age distribution:", age_distribution)

def load_users():
    users = [
        {'id': 1, 'name': 'Alice', 'age': 25, 'country': 'NZ'},
        {'id': 2, 'name': 'Bob', 'age': 17, 'country': 'AU'},
        {'id': 3, 'name': 'Charlie', 'age': 30, 'country': 'NZ'},
        {'id': 4, 'name': 'David', 'age': 22, 'country': 'US'},
        {'id': 5, 'name': 'Eva', 'age': 19, 'country': 'UK'},
    ]
    return users


def filter_adults(users):
    adults = [user for user in users if user['age'] >= 18]
    return adults


def count_by_country(users):
    country_count = Counter(user['country'] for user in users)
    return country_count


def find_oldest_user(users):
    if not users:
        return None
    oldest_user = max(users, key=lambda user: user['age'])
    return oldest_user


def main():
    users = load_users()
    adults = filter_adults(users)
    country_count = count_by_country(users)
    oldest_user = find_oldest_user(users)
    print('Adults: ', adults)
    print('Country statistics', country_count)
    print('Oldest user: ', oldest_user)


if __name__ == "__main__":
    main()

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
