
from pyspark.sql.functions import *
from schema import sales_event_schema

def build_stream(spark, config):

    kafka_stream = (
        spark.readStream
            .format("kafka")
            .option("kafka.bootstrap.servers", config["kafka"]["bootstrap_servers"])
            .option("subscribe", config["kafka"]["topic"])
            .option("startingOffsets", config["kafka"]["starting_offsets"])
            .load()
    )

    parsed_df = (
        kafka_stream
            .selectExpr("CAST(value AS STRING)")
            .select(from_json(col("value"), sales_event_schema).alias("data"))
            .select("data.*")
    )

    enriched_df = parsed_df.withColumn("revenue", col("quantity") * col("price_per_unit"))

    agg_df = (
        enriched_df
            .withWatermark("timestamp", config["streaming"]["watermark"])
            .groupBy(
                window(col("timestamp"),
                       config["streaming"]["window_duration"],
                       config["streaming"]["window_slide"]),
                col("store_location")
            )
            .agg(
                count("*").alias("total_orders"),
                sum("quantity").alias("total_quantity"),
                sum("revenue").alias("total_revenue")
            )
    )
    return agg_df
