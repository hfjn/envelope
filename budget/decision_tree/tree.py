import csv
import pprint
from itertools import groupby
from pathlib import Path
from typing import List, Any, Dict

test_file = Path("/Users/hfjn/code/budget/data/data_banknote_authentication.txt")


def gini_index(groups: Dict[int, List[Any]], classes):
    number_of_samples += len(group) for _, group in groups.items()

    proportions = {
        idx: _calculate_proportions(group) for idx, group in groups.items()
    }

    gini =
    return proportions


def _calculate_proportions(group):
    print(group)
    return {
        label: (len(list(label_group)) / len(group))
        for label, label_group in groupby(group, key=lambda r: r[4])
    }


def _create_split(rows: List[List[Any]], *, number_of_groups: int = 2):
    groups = {group: [] for group in range(number_of_groups)}
    for idx, row in enumerate(rows):
        groups[idx % number_of_groups].append(row)
    return groups


if __name__ == "__main__":
    with test_file.open() as file:
        csv_reader = csv.reader(file)
        rows = [row for row in csv_reader]

    groups = _create_split(rows)

    pprint.pprint(gini_index(groups, None))
