# ipac-lab

Sandbox **Databricks Asset Bundle** for demos and experiments: cluster tiers, jobs, and a demo DLT pipeline. Keeps lab work separate from `ipac_delta_sync`, `ipac-sdt-calc`, and the Deloitte monolith.

## Layout

```text
ipac-lab/
  databricks.yml              # bundle root, targets (dev / qa)
  config/
    cluster_tiers.json        # j1 / j2 / j3 single-node tiers
    variables.yml             # spark version, node types, spark_conf
  resources/
    jobs/
      hello_experiment.job.yml       # smoke test (j1)
      allocation_benchmark.job.yml   # allocation A/B (tier from var)
    pipelines/
      demo_etl.pipeline.yml          # demo DLT pipeline
  notebooks/
    hello_lab.py
    benchmark_load_allocation_input.py
  src/
    pipelines/demo_etl.py
    util/cluster_tiers.py
```

## Prerequisites

- Databricks CLI v0.2+ with a configured profile (`databricks auth login`)
- Workspace access to deploy jobs/pipelines
- For **allocation benchmark**: monolith `Source/` deployed with `AllocationV2/usp_load_allocation_input/output/` (original + `_updated` modules)

## Quick start

```bash
cd /path/to/ipac-lab

# Validate bundle
databricks bundle validate -t dev

# Deploy everything
databricks bundle deploy -t dev

# Deploy one resource
databricks bundle deploy -t dev --select jobs.hello_experiment
databricks bundle deploy -t dev --select jobs.allocation_benchmark
databricks bundle deploy -t dev --select pipelines.demo_etl

# Run smoke job
databricks bundle run -t dev hello_experiment

# Run demo pipeline once
databricks bundle run -t dev demo_etl
```

Workspace root (dev): user bundle path under your workspace (development mode — no shared `root_path`).

Shared deploy (qa target): `/Workspace/Shared/ipac_lab/qa`

## Cluster tiers

Defined in `config/cluster_tiers.json`:

| Tier | Node | Use |
|------|------|-----|
| **j1** | `Standard_D16s_v3` single-node | Smoke tests (`hello_experiment`) |
| **j2** | `Standard_D32s_v3` single-node | Allocation benchmark (default) |
| **j3** | `Standard_D64s_v3` single-node | Heavy experiments |

Change tier for the benchmark job via target variables in `databricks.yml`:

```yaml
variables:
  cluster_tier: j2
  job_cluster_node_type: Standard_D32s_v3
  spark_master: local[32]   # in job_cluster_spark_conf
```

Or override at deploy:

```bash
databricks bundle deploy -t dev \
  --var cluster_tier=j3 \
  --var job_cluster_node_type=Standard_D64s_v3
```

(Also update `job_cluster_spark_conf.spark.master` to `local[64]` for j3.)

## Jobs

### `ipac_lab_hello_experiment`

- Cluster: **j1** (fixed in job YAML)
- Notebook: `notebooks/hello_lab.py`
- Purpose: verify deploy, cluster, and sync

### `ipac_lab_allocation_benchmark`

- Cluster: tier from `${var.cluster_tier}` (default **j2**)
- Notebook: `notebooks/benchmark_load_allocation_input.py`
- Parameters: set in `allocation_benchmark.job.yml` or override `monolith_source_path`, `volume_path`, `parallel_workers`, `benchmark_number_of_run` in `databricks.yml`

## Demo pipeline

`ipac_lab_demo_etl` — DLT pipeline writing to `${uc_catalog}.${uc_schema}`:

- `lab_demo_bronze` — synthetic rows
- `lab_demo_silver` — filtered bronze

Create the target schema in UC before first run if it does not exist.

## Related projects

| Project | Role |
|---------|------|
| `deloitte/usp_load_allocation_input/` | Python modules (`load_allocation_input_updated`, etc.) — copy into monolith |
| `ipac_delta_sync/` | Production ingestion bundles |
| `ipac-sdt-calc/` | Production calc jobs |

## Customization

Edit `databricks.yml` target variables for catalog, monolith path, volume path, and grant group. Add new jobs under `resources/jobs/` and include them automatically via `resources/jobs/*.yml`.
