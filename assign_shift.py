from collections import defaultdict
import random
from loguru import logger

def assign_shift(target_days: list[int], employees: dict[str, list[int]]) -> dict[str, int]:
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
            logger.warning(f"target_day: {target_day} is off day for all employees.")
            not_assigned_days.append(target_day)

    return shift_schedule, not_assigned_days

def validate(shift_schedule):
    shift_counts = defaultdict(list)
    for v in shift_schedule.values():
        shift_counts[len(v)].append(v)
    diff = max(shift_counts) - min(shift_counts)
    assert 0 <= diff <= 1, f"diff: {diff}"

def main():
    target_days = [2, 3, 9, 10, 16, 17, 20, 23, 24, 30, 31]
    employees = {"A": [2, 3], "B": [4], "C": []}
    shift_schedule, not_assigned_days = assign_shift(target_days, employees)
    if len(not_assigned_days):
        logger.warning(f"NOT all target_days are assigned.({not_assigned_days})")
    else:
        logger.info("All target_days are assigned!")
    logger.info(shift_schedule)

if __name__ == "__main__":
    main()
