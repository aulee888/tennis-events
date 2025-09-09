import random as rd
from collections import defaultdict


def pick_pairs(pairs, attendance, num_pairs):
    """
    pairs: list of tuples [(player1, player2), ...]
    attendance: dict mapping {player_id: attendance_count}
    num_pairs: number of pairs to select

    returns: list of selected pairs
    """

    # Ensures everyone exists in attendance dict
    for p1, p2 in pairs:
        attendance.setdefault(p1, 0)
        attendance.setdefault(p2, 0)

    # Group pairs by "fairness score"
    # Use the min of the two players' attendance
    counts = defaultdict(list)
    for pair in pairs:
        p1, p2 = pair
        score = min(attendance[p1], attendance[p2])
        counts[score].append(pair)

    sorted_counts = sorted(counts.items(), key=lambda x: x[0])

    selected = []
    slots_remaining = num_pairs

    for score, group in sorted_counts:
        if slots_remaining <= 0:
            break
        rd.shuffle(group)
        if len(group) <= slots_remaining:
            selected.extend(group)
            slots_remaining -= len(group)
        else:
            selected.extend(rd.sample(group, slots_remaining))
            slots_remaining = 0

    # Update attendance for selected individuals
    for p1, p2 in selected:
        attendance[p1] += 1
        attendance[p2] += 1

    return selected
