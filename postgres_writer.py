
import time
from pyspark.sql import DataFrame

def write_to_postgres(df: DataFrame, epoch_id: int, config):
    retries = 0
    max_retries = config["postgres"]["max_retries"]
    backoff = config["postgres"]["retry_backoff_sec"]

    while retries <= max_retries:
        try:
            (
                df.write
                  .format("jdbc")
                  .option("url", config["postgres"]["url"])
                  .option("dbtable", config["postgres"]["table"])
                  .option("user", config["postgres"]["user"])
                  .option("password", config["postgres"]["password"])
                  .option("driver", config["postgres"]["driver"])
                  .mode("append")
                  .save()
            )
            print(f"✅ Successfully wrote batch {epoch_id} to PostgreSQL.")
            break

        except Exception as e:
            print(f"❌ Failed writing batch {epoch_id}. Attempt {retries+1}/{max_retries}. Error: {str(e)}")
            retries += 1
            time.sleep(backoff)
            if retries > max_retries:
                raise e
