import argparse
import json
from collections import defaultdict
import random


def assign_shift(target_days: list[int], employees: dict[str, list[int]]) -> tuple[dict[str, int], list[int]]:
    shift_schedule = {k: [] for k in employees.keys()}
    not_assigned_days = []
    for target_day in target_days:
        shift_counts = defaultdict(list)
        for k, v in shift_schedule.items():
            shift_counts[len(v)].append(k)
        min_shift_days = min(shift_counts.keys())
        min_shift_day_employees = shift_counts[min_shift_days]
        random.shuffle(min_shift_day_employees)
        ok_flag = False
        for employee in min_shift_day_employees:
            off_days = employees[employee]
            if target_day not in off_days:
                shift_schedule[employee].append(target_day)
                ok_flag = True
            if ok_flag:
                break
        if not ok_flag:
            print(f"Target_day({target_day}) is off day for all employees.")
            not_assigned_days.append(target_day)

    return shift_schedule, not_assigned_days

def validate(shift_schedule: dict[str, list[int]]):
    shift_counts = defaultdict(list)
    for v in shift_schedule.values():
        shift_counts[len(v)].append(v)
    diff = max(shift_counts) - min(shift_counts)
    assert 0 <= diff <= 1, f"diff: {diff}"

def main(args: argparse.Namespace) -> None:
    employees = json.loads(args.employees)
    shift_schedule, not_assigned_days = assign_shift(args.target_days, employees)
    if len(not_assigned_days):
        print(f"{not_assigned_days} are NOT assigned.")
    else:
        print("All target_days are assigned!")
    print(shift_schedule)

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--target_days", type=int, nargs="+")
    argparser.add_argument("--employees", type=str, help="json file path")
    args = argparser.parse_args()
    main(args)
