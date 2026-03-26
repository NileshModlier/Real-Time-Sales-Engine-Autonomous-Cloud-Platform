
from pyspark.sql import SparkSession
from utils import load_config
from streaming_job import build_stream
from postgres_writer import write_to_postgres

def start_stream():
    config = load_config()

    spark = (
        SparkSession.builder
            .appName(config["spark"]["app_name"])
            .master(config["spark"]["master"])
            .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    agg_df = build_stream(spark, config)

    query = (
        agg_df.writeStream
            .foreachBatch(lambda df, eid: write_to_postgres(df, eid, config))
            .outputMode("update")
            .trigger(processingTime=config["streaming"]["trigger_interval"])
            .option("checkpointLocation", config["spark"]["checkpoint_location"])
            .start()
    )

    query.awaitTermination()

if __name__ == "__main__":
    start_stream()
