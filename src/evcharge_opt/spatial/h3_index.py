import h3
import numpy as np
from numpy.typing import NDArray


def coords_to_h3(
    lats: NDArray[np.float64],
    lons: NDArray[np.float64],
    resolution: int = 7,
) -> list[str]:
    """Vectorized-style conversion of lat/lon arrays into H3 cell index strings."""
    return [h3.latlng_to_cell(float(lat), float(lon), resolution) for lat, lon in zip(lats, lons)]


def get_coverage_disk(cell_id: str, k_rings: int = 1) -> set[str]:
    """Return all H3 cells within k grid steps (detour tolerance) of a candidate cell."""
    return set(h3.grid_disk(cell_id, k_rings))
