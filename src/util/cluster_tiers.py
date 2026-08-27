"""Load cluster tier definitions from config/cluster_tiers.json."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_CONFIG_PATH = Path(__file__).resolve().parents[2] / "config" / "cluster_tiers.json"


def load_cluster_tiers() -> dict[str, Any]:
    with _CONFIG_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


def get_job_tier(tier_key: str) -> dict[str, Any]:
    tiers = load_cluster_tiers()["tiers"]
    if tier_key not in tiers:
        raise KeyError(f"Unknown tier {tier_key!r}; expected one of {list(tiers)}")
    return tiers[tier_key]


def single_node_spark_conf(tier_key: str) -> dict[str, str]:
    tier = get_job_tier(tier_key)
    cores = int(tier["local_cores"])
    return {
        "spark.databricks.cluster.profile": "singleNode",
        "spark.master": f"local[{cores}]",
    }
