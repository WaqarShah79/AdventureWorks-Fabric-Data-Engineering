# Read sales order data from the Fabric Lakehouse
df = spark.read.table("SalesOrders")
display(df.limit(10))
df.write.format("delta").mode("overwrite").saveAsTable("Bronze_SalesOrders")
spark.read.table("Bronze_SalesOrders").count()

df = spark.read.table("Bronze_SalesOrders")

print("Total rows:", df.count())
print("Distinct sales orders:", df.select("SalesOrderID").distinct().count())
# Clean Bronze data by filtering out records with missing key fields
from pyspark.sql.functions import col

silver_df = (
    spark.read.table("Bronze_SalesOrders")
    .filter(
        col("SalesOrderID").isNotNull() &
        col("OrderDate").isNotNull() &
        col("CustomerID").isNotNull()
    )
)

silver_df.write.format("delta").mode("overwrite").saveAsTable("Silver_SalesOrders")

print("Silver rows:", spark.read.table("Silver_SalesOrders").count())
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

gold_df.write.format("delta").mode("overwrite").saveAsTable("Gold_SalesByTerritory")

display(gold_df)
gold_df = spark.read.table("Gold_SalesByTerritory")

print("Total orders in Gold:", gold_df.agg({"OrderCount": "sum"}).collect()[0][0])
print("Number of territories:", gold_df.count())
