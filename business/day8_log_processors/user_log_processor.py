import json
import logging

import pandas as pd

logger = logging.getLogger(__name__)


class UserLogProcessor:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        self.df = None
        self.df_activity = None
        self.country_activity = None
        self.user_country_activity = None

    def load_data(self):
        """
        Load user log data from json file
        :return: pd.DataFrame
                 user log dataset
        """
        with open(self.input_path, "r") as f:
            data = json.load(f)

        self.df = pd.DataFrame(data)
        logger.info("Loaded user log %d rows", len(self.df))

    def clean_data(self):
        """
        Remove records where the user's country is missing.
        :return: cleaned dataframe
        """
        if self.df is None:
            raise ValueError("Dataframe not loaded")

        before = len(self.df)
        self.df = self.df.dropna(subset=["country"])
        after = len(self.df)
        logger.info(
            f"Original log {before} rows , "
            f"after cleaning {after} rows, "
            f"delete {before - after} rows with missing country"
        )

    def compute_user_activity(self):
        """
        Aggregate user activity by event
        :return: df_activity pd.DataFrame with columns
                 user_id
                 event_count
        """
        result = (
            self.df.groupby("user_id").agg(event_count=("event", "count")).reset_index()
        )
        self.df_activity = result
        logger.info("Aggregated user activity created: %d rows", len(self.df_activity))

    def compute_country_activity(self):
        """
        Aggregate user activity by country
        :return: country_activity pd.DataFrame with columns
                 country
                 event_count
        """
        result = (
            self.df.groupby("country").agg(event_count=("event", "count")).reset_index()
        )
        self.country_activity = result
        logger.info(
            "Aggregated country activity created: %d rows", len(self.country_activity)
        )

    def compute_user_country_activity(self):
        """
        Aggregate user activity by user_id, country
        :return: user_country_activity pd.DataFrame with columns
                 user_id
                 country
                 event_count
        """
        result = (
            self.df.groupby(["user_id", "country"])
            .agg(event_count=("event", "count"))
            .reset_index()
        )
        self.user_country_activity = result
        logger.info(
            "Aggregated user country activity created: %d rows",
            len(self.user_country_activity),
        )

    def save_result(self):
        """
        Save result into csv file
        :return: None
        """
        self.output_path.mkdir(parents=True, exist_ok=True)

        outputs = {
            "user_activity.csv": self.df_activity,
            "country_activity.csv": self.country_activity,
            "user_country_activity.csv": self.user_country_activity,
        }

        for filename, df in outputs.items():
            path = self.output_path / filename
            df.to_csv(path, index=False)

            logger.info("Saved %s (%d rows)", path, len(df))

    def run(self):
        # extract
        self.load_data()

        # transform
        self.clean_data()

        # aggregate
        self.compute_user_activity()
        self.compute_country_activity()
        self.compute_user_country_activity()

        # output
        self.save_result()
