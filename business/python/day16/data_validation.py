from collections import defaultdict


def validate_user(user):
    try:
        age = int(user["age"])
    except (ValueError, TypeError):
        return False
    if "id" in user and user.get("name") and 0 <= age <= 120 and user["email"]:
        return True
    return False


def split_valid_users(users):
    valid_users = []
    invalid_users = []
    for user in users:
        if validate_user(user):
            valid_users.append(user)
        else:
            invalid_users.append(user)
    return valid_users, invalid_users


def clean_and_validate_users(users):
    cleaned_users = []
    for user in users:
        name = user.get("name").strip()
        email = user.get("email").lower().strip()
        status = user.get("status").lower()
        try:
            age = int(user.get("age"))
        except (ValueError, TypeError):
            age = None
        user = user.copy()
        user["name"] = name
        user["email"] = email
        user["status"] = status
        user["age"] = age
        cleaned_users.append(user)

    return split_valid_users(cleaned_users)


def generate_quality_report(users):
    # {
    #     "total": 4,
    #     "valid": 1,
    #     "invalid": 3,
    #     "errors": {
    #         "missing_name": 1,
    #         "invalid_age": 1,
    #         "missing_email": 1
    #     }
    # }

    total = len(users)
    valid_users, invalid_users = split_valid_users(users)
    valid = len(valid_users)
    invalid = len(invalid_users)
    missing_name = 0
    invalid_age = 0
    missing_email = 0

    for invalid_user in invalid_users:
        age = invalid_user.get("age")
        if not invalid_user.get("name"):
            missing_name += 1
        if not invalid_user.get("email"):
            missing_email += 1
        if age is None or age < 0 or age > 120:
            invalid_age += 1

    return {
        "total": total,
        "valid": valid,
        "invalid": invalid,
        "errors": {
            "missing_name": missing_name,
            "invalid_age": invalid_age,
            "missing_email": missing_email
        }
    }


def validate_user_with_errors(user):
    is_valid = True
    invalid_info = []
    if "id" not in user:
        is_valid = False
        invalid_info.append("missing_id")
    if not user.get("name"):
        is_valid = False
        invalid_info.append("missing_name")
    if not user.get("email"):
        is_valid = False
        invalid_info.append("missing_email")
    try:
        age = int(user.get("age"))
    except (ValueError, TypeError):
        age = None
        is_valid = False
        invalid_info.append("invalid_age")
    else:
        if not 0 <= age <= 120:
            is_valid = False
            invalid_info.append("invalid_age")

    return is_valid, invalid_info


def generate_detailed_quality_report(users):
    total = len(users)
    valid = 0
    invalid = 0
    missing_name = 0
    invalid_age = 0
    missing_email = 0

    for user in users:
        is_valid, invalid_info = validate_user_with_errors(user)
        if is_valid:
            valid += 1
        else:
            invalid += 1
            missing_name += invalid_info.count("missing_name")
            invalid_age += invalid_info.count("invalid_age")
            missing_email += invalid_info.count("missing_email")

    return {
        "total": total,
        "valid": valid,
        "invalid": invalid,
        "errors": {
            "missing_name": missing_name,
            "invalid_age": invalid_age,
            "missing_email": missing_email
        }
    }


def main():
    users = [
        {"id": 1, "name": "Alice", "age": 28, "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "age": 35, "email": "bob@example.com"},
        {"id": 3, "name": "", "age": 25, "email": "charlie@example.com"},
        {"id": 4, "name": "David", "age": -5, "email": "david@example.com"},
        {"id": 5, "name": "Eva", "age": 30, "email": ""},
    ]
    for user in users:
        print(validate_user(user))

    print("-------------------------------------------------")

    users = [
        {"id": 1, "name": "Alice", "age": 28, "email": "alice@example.com"},
        {"id": 2, "name": "", "age": 35, "email": "bob@example.com"},
        {"id": 3, "name": "Charlie", "age": 150, "email": "charlie@example.com"},
        {"id": 4, "name": "David", "age": 40, "email": ""},
        {"id": 5, "name": "Eva", "age": 30, "email": "eva@example.com"},
    ]

    valid_users, invalid_users = split_valid_users(users)
    print("valid_users:", valid_users)
    print("invalid_users:", invalid_users)
    print("-------------------------------------------------")

    users = [
        {"id": 1, "name": " Alice ", "age": "28", "email": "ALICE@EXAMPLE.COM", "status": "active"},
        {"id": 2, "name": "Bob", "age": "35", "email": "bob@example.com", "status": "ACTIVE"},
        {"id": 3, "name": "Charlie", "age": "150", "email": "charlie@example.com", "status": "active"},
        {"id": 4, "name": "David", "age": "40", "email": "", "status": "inactive"},
    ]
    valid_users, invalid_users = clean_and_validate_users(users)
    print("valid_users:", valid_users)
    print("invalid_users:", invalid_users)
    print("-------------------------------------------------")

    users = [
        {"id": 1, "name": "Alice", "age": 28, "email": "alice@example.com"},
        {"id": 2, "name": "", "age": 35, "email": "bob@example.com"},
        {"id": 3, "name": "Charlie", "age": 150, "email": "charlie@example.com"},
        {"id": 4, "name": "David", "age": 40, "email": ""},
    ]

    result = generate_quality_report(users)
    print(result)
    print("---------------------------------------------------")

    result = generate_detailed_quality_report(users)
    print(result)


if __name__ == "__main__":
    main()
