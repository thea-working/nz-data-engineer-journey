# users information clean transform statistic
import csv
import os
from collections import Counter, defaultdict
import statistics
import logging

logger = logging.getLogger(__name__)


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("app.log", encoding="utf-8")
        ]
    )


def load_users_from_csv(filepath):
    """
    read csv file and return list of users
    :param filepath: csv file path
    :return: users list
    """
    users = []
    with open(filepath, newline="", encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # just load data from csv file and doesn't change raw data
            user = {
                'id': row['id'],
                'name': row['name'],
                'age': row['age'],
                'country': row['country'],
            }
            logger.info(f'load users from csv, current user: {user}')
            users.append(user)
    return users


"""
data clean rules: 1) age 不是数字 → 丢弃
                  2) age < 0 或 > 120 → 丢弃
                  3) name 为空 → 丢弃
                  4) country 为空 → 填充 "Unknown"
"""


def clean_users(users):
    cleaned_users = []
    for user in users:
        try:
            user_id = int(user['id'])
            age = int(user['age'])
        except ValueError:
            logger.warning(f'invalid user info: {user}')
            continue
        name = user['name'].strip()
        country = user['country'].strip()

        if not name:
            logger.warning(f'invalid username: {user_id}, name: {name}, age: {age}, country: {country}')
            continue
        if age < 0 or age > 120:
            logger.warning(f'invalid user age: {user_id}, name: {name}, age: {age}, country: {country}')
            continue
        if not country:
            country = 'Unknown'
        logger.info(f'clean user: {user_id}, name: {name}, age: {age}, country: {country}')
        cleaned_users.append({
            'id': user_id,
            'name': name,
            'age': age,
            'country': country,
        })
    return cleaned_users


"""
statistics 1) count users by country
           2) calculate average age
           3) find the median age
           4) find the youngest user
"""


def analyze_users(users):
    # count users by country
    country_count = Counter(user['country'] for user in users)
    # average age
    average_age = round((sum(user['age'] for user in users) / len(users)), 2)
    # median age
    median_age = statistics.median(user['age'] for user in users)
    # the youngest user
    youngest_user = min(users, key=lambda user: user['age'])
    return country_count, average_age, median_age, youngest_user


def analyze_users_optimized(users):
    # calculate within one loop when possible for efficiency
    country_count = defaultdict(int)
    sum_age = 0
    ages = []
    youngest_user = None
    for user in users:
        country_count[user['country']] += 1
        age = user['age']
        sum_age += age
        ages.append(age)
        if youngest_user is None or age < youngest_user['age']:
            youngest_user = user
    average_age = round((sum_age / len(users)), 2)
    median_age = statistics.median(ages)
    logger.info(
        f'analyze_users_optimized, country_count: {list(country_count.items())}, average_age: {average_age}, median_age: {median_age} , youngest_user: {youngest_user}')
    return country_count, average_age, median_age, youngest_user


def save_result(stats, filepath):
    """
    save result to csv file
    :param stats: statistics result
    :param filepath: file path
    :return: None
    """
    country_count, average_age, median_age, youngest_user = stats
    stat_data = {
        'country_count': list(country_count.items()),
        'average_age': average_age,
        'median_age': median_age,
        'youngest_user': youngest_user,
    }
    rows = [{'metric': k, 'value': v} for k, v in stat_data.items()]
    with open(filepath, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['metric', 'value'])
        writer.writeheader()
        writer.writerows(rows)


def run_pipeline(file_path, save_file_path):
    logger.info('loading users from csv file')
    users = load_users_from_csv(file_path)
    logger.info('loading users finished, start to clean users')
    cleaned_user = clean_users(users)
    logger.info('clean users finished, start to analyze')
    stats = analyze_users_optimized(cleaned_user)
    logger.info('analyze finished, start to save result to csv file')
    save_result(stats, save_file_path)
    logger.info('save result to csv file finished')


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, 'data', 'users.csv')
    # users = load_users_from_csv(file_path)
    # print('users load from csv are: ', users)
    # print('-------------------------------')
    # cleaned_user = clean_users(users)
    # print('after clean users are: ', cleaned_user)
    # country_count, average_age, median_age, youngest_user = analyze_users(cleaned_user)
    # print('users count by country:')
    # for country, count in country_count.items():
    #     print(f'{country}: {count}')
    # print(f'average age is: {average_age}')
    # print(f'median age is: {median_age}')
    # print(f'youngest user is: {youngest_user}')
    # print('*' * 30)
    # country_count_optimized, average_age_optimized, median_age_optimized, youngest_user_optimized = analyze_users_optimized(
    #     cleaned_user)
    # print('users count by country:')
    # for country, count in country_count_optimized.items():
    #     print(f'{country}: {count}')
    # print(f'average age is: {average_age_optimized}')
    # print(f'median age is: {median_age_optimized}')
    # print(f'youngest user is: {youngest_user_optimized}')

    save_file_path = os.path.join(base_dir, 'data', 'user_statistics.csv')
    # stats = analyze_users_optimized(cleaned_user)
    # save_result(stats, save_file_path)

    setup_logging()
    run_pipeline(file_path, save_file_path)


if __name__ == '__main__':
    main()
