
from pyspark.sql.types import *

sales_event_schema = StructType([
    StructField("transaction_id", StringType(), False),
    StructField("timestamp", TimestampType(), False),
    StructField("product_id", StringType(), False),
    StructField("product_name", StringType(), False),
    StructField("quantity", IntegerType(), False),
    StructField("price_per_unit", DoubleType(), False),
    StructField("store_location", StringType(), False),
    StructField("payment_mode", StringType(), True)
])
