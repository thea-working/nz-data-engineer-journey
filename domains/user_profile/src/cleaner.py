import logging
from . import User

logger = logging.getLogger(__name__)


# clean users data according to rules

def clean_users(users: list[dict[str, str]]) -> list[User]:
    """
    data clean rules: 1) age 不是数字 → 丢弃
                      2) age < 0 或 > 120 → 丢弃
                      3) name 为空 → 丢弃
                      4) country 为空 → 填充 "Unknown"
    """
    cleaned_users = []
    for user in users:
        try:
            user_id = int(user['id'].strip())
            age = int(user['age'].strip())
            name = user['name'].strip()
            country = user['country'].strip()

            if not name:
                logger.warning(
                    f'skipping user with invalid name : id: {user_id}, name: {name}, age: {age}, country: {country}')
                continue
            if age < 0 or age > 120:
                logger.warning(
                    f'skipping user with invalid age : id: {user_id}, name: {name}, age: {age}, country: {country}')
                continue
            if not country:
                country = 'Unknown'

            # logger.info(f'clean user: id: {user_id}, name: {name}, age: {age}, country: {country}')
            cleaned_users.append(User(id=user_id, name=name, age=age, country=country))

        except Exception as e:
            logger.warning(f"Skipping invalid row: {user} | Error: {e}")
            continue

    logger.info(f"Total cleaned: {len(cleaned_users)}")
    return cleaned_users
