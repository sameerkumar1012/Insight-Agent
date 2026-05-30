import pandas as pd
import numpy as np


# =====================================
# DATA CLEANING
# =====================================

def clean_data(df):

    print("\nStarting Data Cleaning...\n")

    original_rows = len(df)

    # -----------------------------
    # Normalize column names
    # -----------------------------
    df.columns = (
        df.columns
        .str.lower()
        .str.strip()
        .str.replace(" ", "_")
    )

    # -----------------------------
    # Remove duplicates
    # -----------------------------
    before = len(df)

    df = df.drop_duplicates()

    duplicates_removed = before - len(df)

    # -----------------------------
    # Remove empty rows
    # -----------------------------
    before = len(df)

    df = df.dropna(how="all")

    empty_rows_removed = before - len(df)

    # -----------------------------
    # Clean text columns
    # -----------------------------
    for col in df.select_dtypes(
        include="object"
    ).columns:

        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
        )

    # -----------------------------
    # Remove currency symbols
    # -----------------------------
    for col in df.columns:

        if df[col].dtype == "object":

            df[col] = df[col].replace(
                r"[$₹€,]",
                "",
                regex=True
            )

    # -----------------------------
    # Numeric conversion
    # -----------------------------
    for col in df.columns:

        try:

            converted = pd.to_numeric(
                df[col],
                errors="coerce"
            )

            non_null_ratio = (
                converted.notna().sum()
                /
                len(df)
            )

            if non_null_ratio > 0.8:

                df[col] = converted

        except:
            pass

    # -----------------------------
    # Date detection
    # -----------------------------
    for col in df.columns:

        if df[col].dtype == "object":

            try:

                parsed = pd.to_datetime(
                    df[col],
                    errors="coerce"
                )

                success_ratio = (
                    parsed.notna().sum()
                    /
                    len(df)
                )

                if success_ratio > 0.8:

                    df[col] = parsed

                    print(
                        f"Date column detected: {col}"
                    )

            except:
                pass

    # -----------------------------
    # Smart Missing Value Handling
    # -----------------------------
    for col in df.columns:

        if pd.api.types.is_numeric_dtype(
            df[col]
        ):

            median_value = (
                df[col].median()
            )

            df[col] = df[col].fillna(
                median_value
            )

        else:

            df[col] = df[col].fillna(
                "Unknown"
            )

    # -----------------------------
    # Outlier Detection
    # -----------------------------
    print(
        "\nOutlier Report:"
    )

    for col in df.select_dtypes(
        include=np.number
    ).columns:

        try:

            q1 = df[col].quantile(
                0.25
            )

            q3 = df[col].quantile(
                0.75
            )

            iqr = q3 - q1

            lower = q1 - (
                1.5 * iqr
            )

            upper = q3 + (
                1.5 * iqr
            )

            outliers = df[
                (df[col] < lower)
                |
                (df[col] > upper)
            ]

            if len(outliers) > 0:

                print(
                    f"{col}: "
                    f"{len(outliers)} "
                    f"outliers"
                )

        except:
            pass

    # -----------------------------
    # Cleaning Summary
    # -----------------------------
    print(
        "\nData Quality Report"
    )

    print(
        f"Rows Before: "
        f"{original_rows}"
    )

    print(
        f"Rows After: "
        f"{len(df)}"
    )

    print(
        f"Duplicates Removed: "
        f"{duplicates_removed}"
    )

    print(
        f"Empty Rows Removed: "
        f"{empty_rows_removed}"
    )

    print(
        f"Columns: "
        f"{len(df.columns)}"
    )

    return df


# =====================================
# PROFIT CALCULATION
# =====================================

def calculate_profit(df):

    cols = df.columns.tolist()

    required = [
        "product",
        "type",
        "price",
        "qty"
    ]

    if not all(
        col in cols
        for col in required
    ):

        print(
            "Missing required columns"
        )

        return df

    avg_costs = {}

    profits = []

    for _, row in df.iterrows():

        try:

            product = str(
                row["product"]
            )

            t = str(
                row["type"]
            ).lower().strip()

            price = float(
                row["price"]
            )

            qty = float(
                row["qty"]
            )

            if t == "buy":

                if product not in avg_costs:

                    avg_costs[
                        product
                    ] = []

                avg_costs[
                    product
                ].append(price)

                profits.append(0)

            elif t == "sell":

                if product in avg_costs:

                    avg_cost = (
                        sum(
                            avg_costs[
                                product
                            ]
                        )
                        /
                        len(
                            avg_costs[
                                product
                            ]
                        )
                    )

                    profit = (
                        price
                        - avg_cost
                    ) * qty

                    profits.append(
                        round(
                            profit,
                            2
                        )
                    )

                else:

                    profits.append(0)

            else:

                profits.append(0)

        except:

            profits.append(0)

    df["profit"] = profits

    return df