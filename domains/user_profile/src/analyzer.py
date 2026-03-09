import logging
from collections import Counter, defaultdict
import statistics
from . import User

logger = logging.getLogger(__name__)
# calculate metrics based on users data
"""
statistics 1) count users by country
           2) calculate average age
           3) find the median age
           4) find the youngest user
"""


# practice python expression, ignore efficiency
# def analyze_users(users):
#     # count users by country
#     country_count = Counter(user['country'] for user in users)
#     # average age
#     average_age = round((sum(user['age'] for user in users) / len(users)), 2)
#     # median age
#     median_age = statistics.median(user['age'] for user in users)
#     # the youngest user
#     youngest_user = min(users, key=lambda user: user['age'])
#     return country_count, average_age, median_age, youngest_user


def analyze_users_optimized(users: list[User]):
    # calculate within one loop when possible for efficiency
    if not users:
        logger.warning("No users to analyze.")
        return {}, 0, 0, None

    country_count = defaultdict(int)
    ages = []
    youngest_user = None
    for user in users:
        country_count[user.country] += 1
        age = user.age
        ages.append(age)
        if youngest_user is None or age < youngest_user.age:
            youngest_user = user

    average_age = round((sum(ages) / len(ages)), 2)
    median_age = statistics.median(ages)

    logger.info(
        f"Analysis result: {len(users)} users | "
        f"Average age: {average_age} | Median age: {median_age} | "
        f"Youngest: {youngest_user}"
    )

    return country_count, average_age, median_age, youngest_user
