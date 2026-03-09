import pytest
from domains.user_profile.src.cleaner import clean_users


def test_clean_users():
    # (users: list[dict[str, str]]) -> list[User]:

    users = [
        {'id': '1', 'name': 'Alice', 'age': '30', 'country': 'US'},
        {'id': '2', 'name': '', 'age': '25', 'country': 'UK'},  # name 空 → 丢弃
        {'id': '3', 'name': 'Bob', 'age': '-5', 'country': 'UK'},  # age <0 → 丢弃
        {'id': '4', 'name': 'Charlie', 'age': '40', 'country': ''},  # country 空 → Unknown
    ]

    cleaned_users = clean_users(users)
    assert len(cleaned_users) == 2
    assert cleaned_users[1].country == 'Unknown'
    assert all(0 <= user.age <= 120 for user in cleaned_users)
    assert all(user.name for user in cleaned_users)
