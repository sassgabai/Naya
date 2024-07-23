from pyspark.sql import SparkSession
import os

import pyspark.sql.functions as f
from pyspark.sql import types as t
from pyspark.sql.functions import *
from dateutil.parser import parse

#================== integrate wth kafka======================================================#

#================== connection between  spark and kafka=======================================#
#==============================================================================================
spark = SparkSession \
        .builder \
        .master("local[*]") \
        .appName('taxi') \
        .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2') \
        .config("fs.s3a.endpoint", "http://minio:9000") \
        .config("fs.s3a.access.key", "minioadmin") \
        .config("fs.s3a.secret.key", "minioadmin") \
        .config("fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider") \
        .getOrCreate()

#==============================================================================================
#=========================================== ReadStream from kafka===========================#
socketDF = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers","course-kafka:9092") \
    .option("Subscribe", "my_trip")\
    .load()\
    .selectExpr("CAST(key AS STRING)","CAST(value AS STRING)")
#==============================================================================================
#==============================Create schema for create df from json=========================#
schema = t.StructType() \
    .add("vendorid", t.StringType())                    .add("lpep_pickup_datetime", t.StringType()) \
    .add("lpep_dropoff_datetime", t.StringType())       .add("store_and_fwd_flag", t.StringType()) \
    .add("ratecodeid", t.StringType())                  .add("pickup_longitude", t.StringType()) \

#==============================================================================================
#==========================change json to dataframe with schema==============================#
taxiTripsDF = socketDF.select(f.col("value").cast("string")).select(f.from_json(f.col("value"), schema).alias("value")).select("value.*")

#====# 1: Remove spaces from column names====================================================#


# Print to check the data values
#taxiTripsDF.show(1, False)
#display(taxiTripsDF.dtypes)
taxiTripsDF.printSchema()
# connector to mysql


hdfs_query = taxiTripsDF\
    .writeStream\
    .format("parquet")\
    .partitionBy("vendorid")\
    .option("path",'s3a://trip/')\
    .option("checkpointLocation",'s3a://trip/taxi/')\
    .outputMode("append")\
    .start()

hdfs_query.awaitTermination()
