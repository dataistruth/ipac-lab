# Databricks notebook source
# MAGIC %md
# MAGIC # ipac-lab — Demo DLT pipeline
# MAGIC
# MAGIC Static bronze/silver tables for pipeline experiments. No external data required.
# MAGIC
# MAGIC Defined in `resources/pipelines/demo_etl.pipeline.yml`.

# COMMAND ----------

import dlt
from pyspark.sql.functions import col, current_timestamp, lit

environment = spark.conf.get("environment", "lab")
uc_catalog = spark.conf.get("uc_catalog", "QA7")
uc_schema = spark.conf.get("uc_schema", "ipac_lab")


@dlt.table(
    name="lab_demo_bronze",
    comment="ipac-lab demo bronze — synthetic rows",
)
def lab_demo_bronze():
    return (
        spark.range(10)
        .select(
            col("id"),
            lit("bronze").alias("layer"),
            lit(environment).alias("environment"),
            current_timestamp().alias("_ingested_at"),
        )
    )


@dlt.table(
    name="lab_demo_silver",
    comment="ipac-lab demo silver — filtered bronze",
)
def lab_demo_silver():
    return spark.read.table("lab_demo_bronze").filter(col("id") >= 0)
