from pyspark.sql import SparkSession


from pyspark.sql.types import StructType, StructField, StringType, LongType, DateType

schema = StructType([
    StructField("dob", DateType(), True),
    StructField("email", StringType(), True),
    StructField("id", LongType(), False),   
    StructField("income", LongType(), True),
    StructField("name", StringType(), True),
    StructField("phone", LongType(), True)
])


def get_spark():
    return SparkSession.builder \
        .appName("XML Pipeline") \
        .getOrCreate()

def load_xml(path):
    spark = get_spark()

    df = spark.read \
        .format("xml") \
        .option("rowTag", "customer") \
        .schema(schema) \
        .load(path)

    return df