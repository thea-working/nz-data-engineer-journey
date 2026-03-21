import pandas as pd

from business.day8_log_processors.user_log_processor import UserLogProcessor


def test_compute_user_country():
    data = {
        "user_id": [1, 1, 2, 2, 2],
        "country": ["US", "US", "UK", "UK", "UK"],
        "event": ["login", "view", "login", "view", "purchase"],
    }

    df = pd.DataFrame(data)
    processor = UserLogProcessor(None, None)
    processor.df = df
    processor.compute_country_activity()

    result = processor.country_activity

    assert len(result) == 2
    assert result.loc[result["country"] == "US", "event_count"].values[0] == 2
    assert result.loc[result["country"] == "UK", "event_count"].values[0] == 3
