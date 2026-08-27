# Databricks notebook source
# MAGIC %md
# MAGIC # ipac-lab — Hello experiment
# MAGIC
# MAGIC Smoke test for bundle deploy, job cluster **j1**, and notebook sync.
# MAGIC
# MAGIC Run via job `ipac_lab_hello_experiment` or interactively after `databricks bundle sync`.

# COMMAND ----------

dbutils.widgets.text("uc_catalog", "QA7", "UC catalog")
dbutils.widgets.text("uc_schema", "ipac_lab", "UC schema")
dbutils.widgets.text("cluster_tier", "j1", "Cluster tier label")

uc_catalog = dbutils.widgets.get("uc_catalog").strip()
uc_schema = dbutils.widgets.get("uc_schema").strip()
cluster_tier = dbutils.widgets.get("cluster_tier").strip()

# COMMAND ----------

import json
import os
from datetime import datetime

spark_version = spark.version
node_type = spark.conf.get("spark.databricks.cluster.nodeType", "unknown")

summary = {
    "bundle": "ipac-lab",
    "notebook": "hello_lab",
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "spark_version": spark_version,
    "node_type": node_type,
    "uc_catalog": uc_catalog,
    "uc_schema": uc_schema,
    "cluster_tier": cluster_tier,
    "workspace_file_path": os.environ.get("DB_WORKSPACE_FILE_PATH", ""),
}

print(json.dumps(summary, indent=2))

# COMMAND ----------

rows = spark.range(3).selectExpr("id", "concat('ipac-lab-', cast(id as string)) as label")
display(rows)

print("ipac-lab hello experiment OK")
