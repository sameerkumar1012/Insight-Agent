def suggest_chart(question, rows):
    q = question.lower() if question else ""

    if not rows:
        return "none"

    if (
        "trend" in q
        or "monthly" in q
        or "daily" in q
        or "over time" in q
    ):
        return "line"

    if (
        "share" in q
        or "distribution" in q
        or "percentage" in q
    ):
        return "pie"

    return "bar"


def build_chart(rows, chart_type):
    print("Rows count:", len(rows))

    if not rows:
        return None

    if chart_type == "none":
        return None

    keys = list(rows[0].keys())

    if len(keys) < 2:
        return None

    x_key = keys[0]
    y_key = keys[1]

    return {
        "chartType": chart_type,
        "meta": {
            "title": f"{y_key} by {x_key}",
            "description": "Generated automatically from query results"
        },
        "xKey": x_key,
        "series": [
            {
                "dataKey": y_key,
                "label": y_key
            }
        ],
        "data": rows
    }
