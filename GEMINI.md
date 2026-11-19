# Project Context: National EV Corridor Optimizer

## Project Overview & Goal
This repository (`evcharge_opt`) is an open-data geospatial pipeline and optimization engine for EV fast-charger placement across the United States. It ingests public EVSE inventories (NREL AFDC), road networks (OSM), and demand proxies (AAA roadside assistance, EPRI eRoadMap, corridor flow) to output cloud-native geospatial assets (GeoParquet & PMTiles) for public, client-side state and cross-border evaluation.

## Architectural Decisions & Constraints
- **Avoid Fragile C++ Spatial Wrappers:** Do NOT use `GeoPandas`, `Shapely` heavy overlays, or `cuSpatial` in production pipelines. They cause memory bloat and C++ segfaults at national scale.
- **Compute & Vector Engine:** Standardize on **DuckDB (Spatial + H3)**, **Polars**, and vectorized **NumPy/SciPy** routines. Code must run natively on Apple Silicon (M5 Max / 64GB UMA) and portable Linux containers without NVIDIA CUDA dependencies.
- **Spatial Discretization:** Pre-compute **H3 cell IDs** (`h3-py`, Res 7–8) during ingestion. Convert geometric proximity and detour radii into integer H3 `grid_disk` (k-ring) set operations.
- **Cross-Border Continuity:** Partition output Parquet files by `state=XX/dt=YYYY-MM-DD/`, but apply a 25 km spatial buffer across state borders during corridor calculation so interstate routes optimize seamlessly.
- **Optimization Engines:** Implement **CELF Lazy-Greedy** submodular maximization for rapid national/regional runs, retaining **PuLP** (MILP) as a benchmark validator for constrained single-state subsets.
- **Coursework Isolation:** Leave academic notebooks inside `UIUC_GGIS/` untouched. All production code belongs in modular, strictly typed Python packages under `src/evcharge_opt/`.

## Monthly Batch & Cloud-Native Publishing
- **Ingestion:** Monthly scheduled run pulling NREL AFDC EVSE JSON/CSV and Geofabrik state `.osm.pbf` extracts (`pyrosm` / `osmium`).
- **Artifacts:** Export partitioned **GeoParquet** (analytical layer) and **PMTiles** (vector map tiles) for zero-egress hosting on Cloudflare R2 / Source Cooperative and browser-based querying via DuckDB-WASM.
- **Workflow:** Manage dependencies via `Poetry` (`poetry run ...`). Maintain clean commit history and document benchmarks, memory footprints, and cost savings in `README.md`.
