import heapq
from dataclasses import dataclass


@dataclass(frozen=True)
class CandidateSite:
    cell_id: str
    marginal_gain: float
    covered_trajectories: frozenset[int]


def solve_celf_max_coverage(
    candidate_coverage: dict[str, set[int]],
    trajectory_weights: dict[int, float],
    k_sites: int,
    already_covered: set[int] | None = None,
) -> list[tuple[str, float]]:
    """
    Accelerated Lazy Greedy (CELF) solver for submodular trajectory coverage.
    Guarantees a (1 - 1/e) approximation bound in near-linear time.
    """
    covered: set[int] = set(already_covered) if already_covered else set()
    selected: list[tuple[str, float]] = []

    # Max-heap via negated marginal gain: (-gain, last_updated_step, cell_id)
    heap: list[tuple[float, int, str]] = []
    for cell_id, traj_ids in candidate_coverage.items():
        uncovered = traj_ids - covered
        gain = sum(trajectory_weights[t] for t in uncovered)
        if gain > 0:
            heapq.heappush(heap, (-gain, 0, cell_id))

    step = 0
    while heap and len(selected) < k_sites:
        neg_gain, last_step, cell_id = heapq.heappop(heap)

        if last_step == step:
            selected.append((cell_id, -neg_gain))
            covered.update(candidate_coverage[cell_id])
            step += 1
        else:
            uncovered = candidate_coverage[cell_id] - covered
            updated_gain = sum(trajectory_weights[t] for t in uncovered)
            if updated_gain > 0:
                heapq.heappush(heap, (-updated_gain, step, cell_id))

    return selected
