import sys

import matplotlib.pyplot as plt
from pyspark.sql import SparkSession
from pyspark.sql import HiveContext
from pyspark.sql.types import StructType,StructField
from pyspark.sql.types import StringType, IntegerType, DoubleType
import seaborn as sns
import numpy as np


def plotNumberOfSongsOverYear(df, pl):
    df = df \
        .filter("year != 0") \
        .groupby("year") \
        .count() \
        .sort("year")
    df.show(200)

    # sqlContext.registerDataFrameAsTable(df, "songsTable")
    # df = sqlContext.sql("Select * from songsTable")
    # df = df.toPandas()
    # # df.plot.scatter(x='year', y='count')
    # # df.plot.area(x='year', y='count')
    # df.plot.bar(x='year', y='count')
    #
    # plt.savefig('songsoveryear.png')


def plotCorrelation1(df, pl):
    df = df.na.drop().filter('song_hotness != "nan"')
    df = df.withColumn("song_hotness", df.song_hotness.cast(DoubleType()))
    df.show()
    df.printSchema()

    sqlContext.registerDataFrameAsTable(df, "songsTable")
    df = sqlContext.sql("Select * from songsTable")
    df = df.toPandas()
    df.plot.hexbin(x="tempo", y="loudness", C="song_hotness", gridsize=20)

    plt.savefig('correlation.png')




spark = SparkSession.builder \
    .appName("Songs-Analysis") \
    .getOrCreate()

sc = spark.sparkContext
sqlContext = HiveContext(sc)

# Define the Song DataFrame Schema
songSchema = StructType([
    StructField('title', StringType(), True),
    StructField('artist', StringType(), True),
    StructField('year', IntegerType(), True),
    StructField('location', StringType(), True),
    StructField('duration', DoubleType(), True),
    StructField('tempo', DoubleType(), True),
    StructField('loudness', DoubleType(), True),
    StructField('artist_hotness', DoubleType(), True),
    StructField('song_hotness', DoubleType(), True)
])

# Read the data from the songs.csv and generate the DataFrame
data = spark.read\
    .options(header='true', inferSchema='true', schema=songSchema) \
    .option("delimiter", "|") \
    .csv(sys.argv[1])

# Initialise the plot parameters
plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

# 1. Get the number of songs per year
plotNumberOfSongsOverYear(data, plt)

# 2. Get a correlation between loudness, tempo and hotness
# plotCorrelation1(data, plt)

spark.stop()
