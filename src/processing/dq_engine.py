import json
from pyspark.sql.functions import col, when, array, array_remove, lit, size


def load_rules(config_path):
    with open(config_path, "r") as f:
        return json.load(f)["rules"]


def build_condition(rule):
    column = rule["column"]
    condition = rule["condition"]

    if condition == "isNull":
        return col(column).isNull()

    elif condition == "not_contains":
        return col(column).isNotNull() & (~col(column).contains(rule["value"]))

    elif condition == "less_than":
        return col(column) < rule["value"]

    else:
        raise ValueError(f"Unsupported condition: {condition}")


def apply_dq_rules_dynamic(df, config_path):
    rules = load_rules(config_path)

    error_conditions = []

    for rule in rules:
        condition_expr = build_condition(rule)

        error_conditions.append(
            when(condition_expr, lit(rule["error"]))
        )

    df = df.withColumn(
        "error_reason",
        array_remove(array(*error_conditions), None)
    )

    df = df.withColumn(
        "is_valid",
        size(col("error_reason")) == 0
    )

    return df