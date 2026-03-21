from collections import Counter

from domains.user_profile.src import User
from domains.user_profile.src.analyzer import analyze_users_optimized


def test_analyze_users():
    users = [
        User(1, "Alice", 30, "US"),
        User(2, "Bob", 40, "US"),
        User(3, "Charlie", 25, "UK"),
    ]
    country_count, average_age, median_age, youngest = analyze_users_optimized(users)
    assert country_count == {"US": 2, "UK": 1}
    assert average_age == 31.67
    assert median_age == 30
    assert youngest.name == "Charlie"
