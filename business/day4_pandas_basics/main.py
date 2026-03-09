from pathlib import Path
import pandas as pd


def load_orders(input_file: Path) -> pd.DataFrame:
    return pd.read_csv(input_file)


def filter_orders(df: pd.DataFrame) -> pd.DataFrame:
    return df[df.amount > 150]


def aggregate_by_count(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby('country')['amount']
        .sum()
        .reset_index()
    )


def main():
    base_dir = Path(__file__).resolve().parent.parent
    order_file = base_dir / 'data/orders.csv'
    orders = load_orders(order_file)
    print(f'orders info:\n{orders}')
    filtered = filter_orders(orders)
    result = aggregate_by_count(filtered)
    print(f'aggregate by country:\n{result}')
    users_file = base_dir / 'data/users.csv'
    users = load_orders(users_file)
    print(f'users info:\n{users}')
    order_user_df = orders.merge(users, on='user_id')
    print(f'order_user_df info:\n{order_user_df}')


if __name__ == '__main__':
    main()
