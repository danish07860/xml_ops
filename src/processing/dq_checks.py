from pyspark.sql.functions import col, when, lit


def apply_dq_rules(df):
    """
    Adds validation flags and error reasons
    """

    df = df.withColumn(
        "error_reason",
        when(col("id").isNull(), "NULL_ID")
        .when(col("email").isNull(), "NULL_EMAIL")
        .when(~col("email").contains("@"), "INVALID_EMAIL")
        .when(col("income") < 0, "NEGATIVE_INCOME")
        .otherwise(None)
    )

    df = df.withColumn(
        "is_valid",
        col("error_reason").isNull()
    )

    return df

def generate_dq_report(df):
    report = {}

    total = df.count()

    report["total_records"] = total
    report["null_id"] = df.filter(col("id").isNull()).count()
    report["null_email"] = df.filter(col("email").isNull()).count()
    report["invalid_email"] = df.filter(~col("email").contains("@")).count()
    report["negative_income"] = df.filter(col("income") < 0).count()

    return report

def split_data(df):
    good_df = df.filter(col("is_valid") == True)
    bad_df = df.filter(col("is_valid") == False)

    return good_df, bad_df

