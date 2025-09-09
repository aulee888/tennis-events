import random as rd
from collections import defaultdict


def pick_players(players, attendance, num_players):
    """
    players: list of players [player1, player2, ...]
    attendance: dict mapping {player_id: attendance_count}
    num_players: number of pairs to select

    returns: list of selected players
    """

    # Ensures everyone exists in attendance dict
    for p in players:
        attendance.setdefault(p, 0)

    # Group players by their attendance counts
    counts = defaultdict(list)
    for p in players:
        attendance_count = attendance[p]
        counts[attendance_count].append(p)

    sorted_counts = sorted(counts.items(), key=lambda x: x[0])

    selected = []
    slots_remaining = num_players

    for attendance_count, group in sorted_counts:
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
    for p in selected:
        attendance[p] += 1

    return selected
