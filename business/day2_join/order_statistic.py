# order statistic

# order info
orders = [
    {"order_id": 1, "user_id": 1, "amount": 120},
    {"order_id": 2, "user_id": 2, "amount": 80},
    {"order_id": 3, "user_id": 1, "amount": 200},
    {"order_id": 4, "user_id": 3, "amount": 150},
]

users = [
    {"id": 1, "name": "Alice", "age": 25, "country": "NZ"},
    {"id": 2, "name": "Bob", "age": 17, "country": "AU"},
    {"id": 3, "name": "Charlie", "age": 30, "country": "NZ"},
    {"id": 4, "name": "David", "age": 22, "country": "US"},
    {"id": 5, "name": "Eva", "age": 19, "country": "UK"},
]


def analyse_orders(orders):
    """
    calculate the total sales , spending per user and find user who spent most
    :param orders: order information, including order_id, user_id, amount
    :return: total_sales, user_total_spending, top_user, top_amount
    """
    total_sales = 0
    user_total_spending = {}  # {1: 320}
    top_user = None
    top_amount = 0

    for order in orders:
        order_amount = order["amount"]
        user_id = order["user_id"]

        # total sales
        total_sales += order_amount
        # total spending for per user
        user_total_spending[user_id] = (
            user_total_spending.get(user_id, 0) + order_amount
        )
        # user who spent the most
        if user_total_spending[user_id] > top_amount:
            top_amount = user_total_spending[user_id]
            top_user = user_id

    return total_sales, user_total_spending, top_user, top_amount


def main():
    total_sales, user_total_spending, top_user, top_amount = analyse_orders(orders)

    print("the total sales for all users is: ", total_sales)
    print("the total spending for per user is: ", user_total_spending)
    print(f"the user_id of user who spent most is: {top_user}, spent {top_amount}")

    # extend user_total_spending join users , print username and their spending eg: Alice spent 320
    # build lookup table
    user_index = {user["id"]: user["name"] for user in users}  # 1: 'Alice'

    # find spending through user_id
    for user_id, amount in user_total_spending.items():
        name = user_index.get(user_id)

        if name is None:
            print(f"Unknown user: {user_id}, spent {amount}")
        else:
            print(f"{name} spent {amount}")


if __name__ == "__main__":
    main()
