import csv
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


# write result to file
def save_result(stats, filepath):
    """
    save result to csv file
    :param stats: statistics result
    :param filepath: file path
    :return: None
    """
    country_count, average_age, median_age, youngest_user = stats
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    for country, count in country_count.items():
        rows.append({"metric": f"country_{country}", "value": count})
    rows += [
        {"metric": "average_age", "value": average_age},
        {"metric": "median_age", "value": median_age},
        {
            "metric": "youngest_user",
            "value": youngest_user.name if youngest_user else None,
        },
    ]

    with open(filepath, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["metric", "value"])
        writer.writeheader()
        writer.writerows(rows)

    logger.info(f"Analysis results saved to {filepath}")
