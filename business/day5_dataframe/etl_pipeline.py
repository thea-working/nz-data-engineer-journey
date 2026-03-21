import logging
from pathlib import Path

import pandas as pd

from infrastructure.logging_config import setup_logging


def load_data(path: Path) -> pd.DataFrame:
    """
    Loads data from csv file
    :param path: Path to csv file
    :return: loaded dataset
    """
    if not path.exists():
        raise FileNotFoundError(f"File not found at {path}")
    return pd.read_csv(path)


def merge_data(df_orders: pd.DataFrame, df_users: pd.DataFrame) -> pd.DataFrame:
    """
    Merges orders and users datasets
    Left join ensures that all orders are preserved even if
    a matching user record does not exist.
    :param df_orders: pd.Dataframe
           orders dataset
    :param df_users: pd.Dataframe
           users dataset
    :return: pd.Dataframe
            merged dataset
    """
    return pd.merge(df_orders, df_users, on="user_id", how="left")


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove records where the user's country is missing.
    These rows likely represent orders with unknown users
    after the left join.

    :param df: original dataframe
    :return: cleaned dataframe
    """
    before = len(df)

    cleaned = df.dropna(subset=["country"])

    after = len(cleaned)

    logging.getLogger(__name__).info(
        "Removed %d rows with missing country", before - after
    )

    return cleaned


def analyze_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate total sales by country.
    :param df: Cleaned dataset.
    :return: DataFrame with columns:
             country
             total_sales
    """
    result = df.groupby("country").agg(total_sales=("amount", "sum")).reset_index()
    return result.sort_values(by="total_sales", ascending=False)


def write_data(df: pd.DataFrame, path: Path) -> None:
    """
    Writes data to parquet file
    :param df: pd.DataFrame
               analyzed dataset
    :param path: output directory
    :return: None
    """
    df.to_parquet(path, partition_cols=["country"], index=False)
    logging.getLogger(__name__).info(
        "Data written to Parquet with partition on 'country'"
    )


def main():
    base_dir = Path(__file__).resolve().parent.parent
    # initial logging
    setup_logging(log_file=str(base_dir / "app.log"), log_level="INFO")
    logger = logging.getLogger(__name__)
    try:
        logger.info("Data pipeline started")
        # extract
        users_file = base_dir / "data/users_original.csv"
        users = load_data(users_file)
        logger.info("Users dataset loaded: %d rows:", len(users))
        orders_file = base_dir / "data/orders_original.csv"
        orders = load_data(orders_file)
        logger.info("Orders dataset loaded: %d rows:", len(orders))

        # transform
        orders_with_users = merge_data(orders, users)
        logger.info("Merged dataset created: %d rows:", len(orders_with_users))
        cleaned = clean_data(orders_with_users)
        logger.info("Cleaned dataset created: %d rows:", len(cleaned))

        # aggregate
        analyzed = analyze_data(cleaned)
        logger.info("Aggregated dataset created: %d rows:", len(analyzed))

        # output
        write_data(analyzed, base_dir / "data/sales_by_country")

        logger.info("Data pipeline finished successfully")

    except Exception as e:
        logger.exception(f"Data pipeline failed: {e}")


if __name__ == "__main__":
    main()
