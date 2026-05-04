from pyspark.sql.functions import col, when, array, array_remove, lit, sum, count


def apply_dq_rules(df):
    """
    Adds validation flags and supports MULTIPLE error reasons per row
    """

    df = df.withColumn(
        "error_reason",
        array_remove(array(
            when(col("id").isNull(), lit("NULL_ID")),
            when(col("email").isNull(), lit("NULL_EMAIL")),
            when(
                col("email").isNotNull() & (~col("email").contains("@")),
                lit("INVALID_EMAIL")
            ),
            when(col("income") < 0, lit("NEGATIVE_INCOME"))
        ), None)
    )

    df = df.withColumn(
        "is_valid",
        (col("error_reason").isNull()) | (col("error_reason") == array())
    )

    return df


# 🚀 OPTIMIZED SINGLE-PASS DQ REPORT
def generate_dq_report(df):
    agg_df = df.agg(
        count("*").alias("total_records"),

        sum(when(col("id").isNull(), 1).otherwise(0)).alias("null_id"),

        sum(when(col("email").isNull(), 1).otherwise(0)).alias("null_email"),

        sum(
            when(
                col("email").isNotNull() & (~col("email").contains("@")),
                1
            ).otherwise(0)
        ).alias("invalid_email"),

        sum(when(col("income") < 0, 1).otherwise(0)).alias("negative_income"),
    )

    return agg_df.collect()[0].asDict()


def split_data(df):
    """
    Split using is_valid flag (clean + efficient)
    """
    good_df = df.filter(col("is_valid") == True)
    bad_df = df.filter(col("is_valid") == False)

    return good_df, bad_df