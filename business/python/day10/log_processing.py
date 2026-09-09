from collections import defaultdict


def parse_log(log):
    log_lines = log.split(",")
    return {
        "timestamp": log_lines[0],
        "level": log_lines[1],
        "user": log_lines[2].split("=")[1],
        "action": log_lines[3].split("=")[1]
    }


def parse_logs(logs):
    parsed_logs = []
    for log in logs:
        try:
            parsed_log = parse_log(log)
            if not parsed_log["user"]:
                continue
            parsed_logs.append(parsed_log)
        except (IndexError, ValueError):
            continue
    return parsed_logs


def count_user_logins(logs):
    # 统计每个用户的登录次数。
    parsed_logs = parse_logs(logs)
    user_count = defaultdict(int)
    for log in parsed_logs:
        if log["action"] == "login":
            user_count[log["user"]] += 1

    return dict(user_count)


def count_actions(logs):
    parsed_logs = parse_logs(logs)
    actions_count = defaultdict(int)
    for log in parsed_logs:
        actions_count[log["action"]] += 1

    return dict(actions_count)


def user_action_counts(logs):
    parsed_logs = parse_logs(logs)
    user_diff_action_counts = defaultdict(dict)
    for log in parsed_logs:
        user_diff_action_counts[log["user"]][log["action"]] = user_diff_action_counts[log["user"]].get(log["action"],
                                                                                                       0) + 1

    return dict(user_diff_action_counts)


def simple_user_action_counts(logs):
    parsed_logs = parse_logs(logs)
    user_diff_action_counts = defaultdict(lambda: defaultdict(int))
    for log in parsed_logs:
        user_diff_action_counts[log["user"]][log["action"]] += 1

    return dict(user_diff_action_counts)


def main():
    logs = [
        "2026-09-09 10:01:23,INFO,user=Alice,action=login",
        "2026-09-09 10:02:15,ERROR,user=Bob,action=payment",
        "2026-09-09 10:03:10,INFO,user=Alice,action=logout",
        "2026-09-09 10:04:05,INFO,user=Charlie,action=login",
    ]
    for log in logs:
        parsed_log = parse_log(log)
        print(parsed_log)
    print("-------------------------------------")

    logs = [
        "2026-09-09 10:01:23,INFO,user=Alice,action=login",
        "2026-09-09 10:02:15,ERROR,user=Bob,action=payment",
        "invalid log",
        "2026-09-09 10:03:10,INFO,user=Alice,action=logout",
        "2026-09-09 10:04:05,INFO,user=,action=login",
    ]

    parsed_logs = parse_logs(logs)
    print(parsed_logs)
    print("-------------------------------------")

    logs = [
        "2026-09-09 10:01:23,INFO,user=Alice,action=login",
        "2026-09-09 10:02:15,ERROR,user=Bob,action=payment",
        "2026-09-09 10:03:10,INFO,user=Alice,action=logout",
        "2026-09-09 10:04:05,INFO,user=Charlie,action=login",
        "2026-09-09 10:05:20,INFO,user=Alice,action=login",
    ]
    user_count = count_user_logins(logs)
    print(user_count)
    print("-------------------------------------")

    logs = [
        "2026-09-09 10:01:23,INFO,user=Alice,action=login",
        "2026-09-09 10:02:15,ERROR,user=Bob,action=payment",
        "2026-09-09 10:03:10,INFO,user=Alice,action=logout",
        "2026-09-09 10:04:05,INFO,user=Charlie,action=login",
        "2026-09-09 10:05:20,INFO,user=Alice,action=login",
    ]
    actions_count = count_actions(logs)
    print(actions_count)
    print("-------------------------------------")

    logs = [
        "2026-09-09 10:01:23,INFO,user=Alice,action=login",
        "2026-09-09 10:02:15,ERROR,user=Bob,action=payment",
        "2026-09-09 10:03:10,INFO,user=Alice,action=logout",
        "2026-09-09 10:04:05,INFO,user=Charlie,action=login",
        "2026-09-09 10:05:20,INFO,user=Alice,action=login",
        "2026-09-09 10:06:20,INFO,user=Bob,action=login",
    ]
    user_diff_action_counts = user_action_counts(logs)
    print(user_diff_action_counts)
    print("-------------------------------------")
    user_diff_action_counts = simple_user_action_counts(logs)
    print(user_diff_action_counts)


if __name__ == "__main__":
    main()
