import pandas as pd

from business.day8_log_processors.user_log_processor import UserLogProcessor


def test_log_clean_data():
    data = {"user_id": [1, 1, 2, 2, 2], "country": ["US", "US", "UK", None, "UK"]}
    df = pd.DataFrame(data)
    processor = UserLogProcessor(None, None)
    processor.df = df

    processor.clean_data()

    cleaned_log = processor.df

    assert len(cleaned_log) == 4
    assert cleaned_log["country"].isnull().sum() == 0
