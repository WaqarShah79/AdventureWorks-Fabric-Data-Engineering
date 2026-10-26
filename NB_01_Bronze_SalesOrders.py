from pyspark.sql.functions import col
from pyspark.sql.functions import sum, count
# Read sales order data from the Fabric Lakehouse
df = spark.read.table("SalesOrders")
display(df.limit(10))

# Save the raw data to the Bronze layer
df.write.format("delta").mode("overwrite").saveAsTable("Bronze_SalesOrders")

# Validate the Bronze layer
bronze_df = spark.read.table("Bronze_SalesOrders")
print("Total rows:", bronze_df.count())
print("Distinct sales orders:", bronze_df.select("SalesOrderID").distinct().count())
# Clean Bronze data by filtering out records with missing key fields
silver_df = (
    bronze_df
    .filter(
        col("SalesOrderID").isNotNull() &
        col("OrderDate").isNotNull() &
        col("CustomerID").isNotNull()
    )
)

# Save cleaned data to the Silver layer
silver_df.write.format("delta").mode("overwrite").saveAsTable("Silver_SalesOrders")
print("Silver rows:", spark.read.table("Silver_SalesOrders").count())

# Aggregate revenue and order counts by sales territory for the Gold layer
from pyspark.sql.functions import sum, count

silver_df = spark.read.table("Silver_SalesOrders")

gold_df = (
    silver_df
    .groupBy("TerritoryID")
    .agg(
        sum("TotalDue").alias("TotalRevenue"),
        count("SalesOrderID").alias("OrderCount")
    )
    .orderBy("TerritoryID")
)

# Save aggregated results to the Gold layer
gold_df.write.format("delta").mode("overwrite").saveAsTable("Gold_SalesByTerritory")

# Validate the Gold layer
display(gold_df)
gold_df = spark.read.table("Gold_SalesByTerritory")
print("Total orders in Gold:", gold_df.agg({"OrderCount": "sum"}).collect()[0][0])
print("Number of territories:", gold_df.count())
