import csv
import logging
from pathlib import Path

# load users information from csv file

logger = logging.getLogger(__name__)


def load_users_from_csv(filepath):
    """
    Load CSV file and return list of users
    :param filepath: csv file path
    :return: users list
    """
    filepath = Path(filepath)
    if not filepath.exists():
        logger.error(f"Input file not found: {filepath}")
        return []

    users = []
    with open(filepath, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # just load data from csv file and doesn't change raw data
            user = {
                "id": row["id"],
                "name": row["name"],
                "age": row["age"],
                "country": row["country"],
            }
            # remove this when user data is massive
            # logger.info(f'load users from csv, current user: {user}')
            users.append(user)
    logger.info(f"Total loaded: {len(users)}")
    return users
