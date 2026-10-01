def add_unit_price(orders):
    added_orders = []
    for order in orders:
        # add unit_price
        try:
            unit_price = float(order.get("amount") / order.get("quantity"))
        except (TypeError, ValueError, ZeroDivisionError):
            continue
        order = order.copy()
        order["unit_price"] = unit_price
        added_orders.append(order)

    return added_orders


def add_order_level(orders):
    # add order level based on amount
    added_orders = []
    for order in orders:
        level = None
        try:
            amount = int(order.get("amount"))
        except (TypeError, ValueError):
            continue
        if amount >= 200:
            level = "high"
        elif amount >= 100:
            level = "medium"
        else:
            level = "low"

        order = order.copy()
        order["order_level"] = level
        added_orders.append(order)

    return added_orders


def add_order_metrics(orders):
    priced_orders = add_unit_price(orders)
    added_orders = []
    for order in priced_orders:
        is_valid_sale = (
                order.get("status") == "completed"
                and order.get("amount") > 0
                and order.get("quantity") > 0
        )
        order = order.copy()
        order["is_valid_sale"] = is_valid_sale
        added_orders.append(order)

    return added_orders


def add_discounted_amount(orders, discount_rate):
    added_orders = []
    for order in orders:
        amount = float(order.get("amount"))
        if order.get("status") == "completed":
            discounted_amount = amount * (1 - discount_rate)
        else:
            discounted_amount = 0
        order = order.copy()
        order["discounted_amount"] = discounted_amount
        added_orders.append(order)

    return added_orders


def transform_orders(orders, discount_rate):
    transformed_orders = add_unit_price(orders)
    transformed_orders = add_order_level(transformed_orders)
    transformed_orders = add_order_metrics(transformed_orders)
    added_orders = add_discounted_amount(transformed_orders, discount_rate)
    return added_orders


def main():
    orders = [
        {"order_id": 1, "amount": 120, "quantity": 2},
        {"order_id": 2, "amount": 80, "quantity": 1},
        {"order_id": 3, "amount": 300, "quantity": 5},
        {"order_id": 4, "amount": 50, "quantity": 2},
    ]
    added_orders = add_unit_price(orders)
    print(added_orders)
    print("----------------------------------------------")

    orders = [
        {"order_id": 1, "amount": 120},
        {"order_id": 2, "amount": 80},
        {"order_id": 3, "amount": 300},
        {"order_id": 4, "amount": 50},
    ]

    added_orders = add_order_level(orders)
    print(added_orders)
    print("------------------------------------------------")

    orders = [
        {"order_id": 1, "amount": 120, "quantity": 2, "status": "completed"},
        {"order_id": 2, "amount": 80, "quantity": 1, "status": "cancelled"},
        {"order_id": 3, "amount": 300, "quantity": 5, "status": "completed"},
        {"order_id": 4, "amount": 50, "quantity": 2, "status": "completed"},
    ]
    added_orders = add_order_metrics(orders)
    print(added_orders)
    print("-----------------------------------------------")

    orders = [
        {"order_id": 1, "amount": 120, "quantity": 2, "status": "completed"},
        {"order_id": 2, "amount": 80, "quantity": 1, "status": "cancelled"},
        {"order_id": 3, "amount": 300, "quantity": 5, "status": "completed"},
        {"order_id": 4, "amount": 50, "quantity": 2, "status": "completed"},
    ]

    added_orders = add_discounted_amount(orders, 0.1)
    print(added_orders)
    print("-----------------------------------------------")

    orders = [
        {"order_id": 1, "amount": 120, "quantity": 2, "status": "completed"},
        {"order_id": 2, "amount": 80, "quantity": 1, "status": "cancelled"},
        {"order_id": 3, "amount": 300, "quantity": 5, "status": "completed"},
        {"order_id": 4, "amount": 50, "quantity": 2, "status": "completed"},
    ]
    added_orders = transform_orders(orders, 0.1)
    print(added_orders)


if __name__ == '__main__':
    main()
