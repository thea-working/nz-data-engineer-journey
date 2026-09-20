from collections import defaultdict
from datetime import datetime, timedelta


def parse_timestamps(timestamps):
    return [datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S") for timestamp in timestamps]


def calculate_session_duration(events):
    # 计算每个用户的 session duration 使用 logout - login
    # 返回新的 list duration 用分钟表示
    result = []
    for event in events:
        session_duration = datetime.strptime(event["logout"], "%Y-%m-%d %H:%M:%S") - datetime.strptime(event["login"],
                                                                                                       "%Y-%m-%d %H:%M:%S")
        result.append({
            "user": event["user"],
            "duration": session_duration.total_seconds() / 60
        })
    return result


def count_orders_by_date(orders):
    # 从 timestamp 中提取日期
    # 按日期统计订单数量 返回一个 dict
    result = defaultdict(int)
    for order in orders:
        dt = datetime.strptime(order["timestamp"], "%Y-%m-%d %H:%M:%S")
        order_date = dt.date().strftime("%Y-%m-%d")
        result[order_date] += 1
    return dict(result)


def get_recent_events(events, current_time):
    recent_events = []
    start_time = current_time - timedelta(hours=24)
    for event in events:
        event_time = datetime.strptime(event["timestamp"], "%Y-%m-%d %H:%M:%S")
        if start_time <= event_time <= current_time:
            recent_events.append(event)
    return recent_events


def get_recent_event_counts(events, current_time):
    # 只处理过去 24 小时内的 events
    # 按 action 统计数量 返回 dict
    # timestamp 需要先转换成 datetime
    # 可以复用你刚才写的 get_recent_events()
    recent_events = get_recent_events(events, current_time)
    recent_event_counts = defaultdict(int)
    for event in recent_events:
        action = event["action"]
        recent_event_counts[action] += 1
    return dict(recent_event_counts)


def main():
    timestamps = [
        "2026-09-19 10:30:00",
        "2026-09-19 11:45:30",
        "2026-09-20 09:15:00",
    ]
    result = parse_timestamps(timestamps)
    print(result)
    print("--------------------------------------")

    events = [
        {
            "user": "Alice",
            "login": "2026-09-19 10:00:00",
            "logout": "2026-09-19 10:45:00"
        },
        {
            "user": "Bob",
            "login": "2026-09-19 11:00:00",
            "logout": "2026-09-19 12:30:00"
        },
        {
            "user": "Charlie",
            "login": "2026-09-19 14:00:00",
            "logout": "2026-09-19 14:20:00"
        }
    ]
    result = calculate_session_duration(events)
    print(result)
    print("--------------------------------------")

    orders = [
        {"order_id": "A001", "timestamp": "2026-09-19 10:30:00", "amount": 100},
        {"order_id": "A002", "timestamp": "2026-09-19 11:20:00", "amount": 200},
        {"order_id": "A003", "timestamp": "2026-09-20 09:15:00", "amount": 150},
        {"order_id": "A004", "timestamp": "2026-09-20 14:30:00", "amount": 300},
        {"order_id": "A005", "timestamp": "2026-09-20 16:45:00", "amount": 50},
    ]
    result = count_orders_by_date(orders)
    print(result)
    print("-------------------------------------")

    events = [
        {"user": "Alice", "timestamp": "2026-09-19 10:00:00"},
        {"user": "Bob", "timestamp": "2026-09-18 18:00:00"},
        {"user": "Charlie", "timestamp": "2026-09-19 08:30:00"},
        {"user": "David", "timestamp": "2026-09-17 12:00:00"},
    ]

    current_time = datetime(2026, 9, 19, 12, 0, 0)
    result = get_recent_events(events, current_time)
    print(result)
    print("-------------------------------------")

    events = [
        {"user": "Alice", "timestamp": "2026-09-19 10:00:00", "action": "login"},
        {"user": "Bob", "timestamp": "2026-09-18 18:00:00", "action": "login"},
        {"user": "Alice", "timestamp": "2026-09-19 10:30:00", "action": "purchase"},
        {"user": "Charlie", "timestamp": "2026-09-19 08:30:00", "action": "login"},
        {"user": "David", "timestamp": "2026-09-17 12:00:00", "action": "login"},
        {"user": "Bob", "timestamp": "2026-09-19 11:00:00", "action": "purchase"},
    ]
    current_time = datetime(2026, 9, 19, 12, 0, 0)
    result = get_recent_event_counts(events, current_time)
    print(result)


if __name__ == "__main__":
    main()
