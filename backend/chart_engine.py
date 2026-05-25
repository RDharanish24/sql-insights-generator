"""
Chart Recommendation Engine
Analyzes query result columns and data to recommend the best visualization type.
"""


def recommend_chart(columns: list, data: list, question: str = "") -> dict:
    """
    Analyze columns, data, and the user question to recommend a chart type.
    
    Returns:
        dict with keys: type ("bar"|"line"|"none"), x_column, y_column, title
    """
    if not columns or not data or len(data) < 2:
        return {"type": "none", "x_column": None, "y_column": None, "title": None}

    # Normalize column names for matching
    col_lower = [c.lower() for c in columns]
    question_lower = question.lower() if question else ""

    # --- Identify column roles ---
    time_keywords = ["date", "month", "year", "quarter", "week", "day", "period", "time"]
    category_keywords = ["name", "country", "category", "product", "region", "city", "user", "type", "brand", "status"]

    time_cols = []
    category_cols = []
    numeric_cols = []

    for i, col in enumerate(col_lower):
        # Check if this column matches time patterns
        if any(kw in col for kw in time_keywords):
            time_cols.append(columns[i])
        # Check if this column matches category patterns
        elif any(kw in col for kw in category_keywords):
            category_cols.append(columns[i])

    # Identify numeric columns by inspecting actual data values
    for i, col in enumerate(columns):
        if col in time_cols or col in category_cols:
            continue
        # Check if most values in this column are numeric
        numeric_count = 0
        for row in data:
            try:
                val = row[i]
                if isinstance(val, (int, float)):
                    numeric_count += 1
                elif isinstance(val, str):
                    float(val)
                    numeric_count += 1
            except (ValueError, TypeError, IndexError):
                pass
        if numeric_count > len(data) * 0.5:
            numeric_cols.append(columns[i])

    # If no explicit categories or time cols found, check data types directly
    if not time_cols and not category_cols and len(columns) >= 2:
        # First column might be category if it's all strings
        first_col_strings = all(isinstance(row[0], str) for row in data if row)
        if first_col_strings:
            category_cols.append(columns[0])
        # Remaining numeric columns
        for i in range(1, len(columns)):
            if columns[i] not in numeric_cols:
                is_numeric = all(isinstance(row[i], (int, float)) for row in data if row)
                if is_numeric:
                    numeric_cols.append(columns[i])

    # --- Determine chart type ---

    # Check question for time-related intent
    time_question_keywords = ["trend", "over time", "monthly", "daily", "weekly", "yearly", "growth", "by month", "by year", "by date"]
    question_suggests_time = any(kw in question_lower for kw in time_question_keywords)

    # LINE CHART: time series data
    if time_cols and numeric_cols:
        y_col = _pick_best_numeric(numeric_cols, question_lower)
        title = _generate_title(question, "line")
        return {
            "type": "line",
            "x_column": time_cols[0],
            "y_column": y_col,
            "title": title
        }

    # LINE CHART: question suggests time even if column names don't explicitly say "date"
    if question_suggests_time and category_cols and numeric_cols:
        y_col = _pick_best_numeric(numeric_cols, question_lower)
        title = _generate_title(question, "line")
        return {
            "type": "line",
            "x_column": category_cols[0],
            "y_column": y_col,
            "title": title
        }

    # BAR CHART: categorical data with numeric values
    if category_cols and numeric_cols:
        y_col = _pick_best_numeric(numeric_cols, question_lower)
        title = _generate_title(question, "bar")
        return {
            "type": "bar",
            "x_column": category_cols[0],
            "y_column": y_col,
            "title": title
        }

    # FALLBACK: If we have at least 2 columns and multiple rows, try bar chart
    if len(columns) >= 2 and len(data) >= 2:
        # Use first column as x, second as y
        y_col = numeric_cols[0] if numeric_cols else columns[1]
        title = _generate_title(question, "bar")
        return {
            "type": "bar",
            "x_column": columns[0],
            "y_column": y_col,
            "title": title
        }

    return {"type": "none", "x_column": None, "y_column": None, "title": None}


def _pick_best_numeric(numeric_cols: list, question_lower: str) -> str:
    """Pick the most relevant numeric column based on the question."""
    # Prefer columns whose names appear in the question
    revenue_keywords = ["revenue", "amount", "total", "sales", "sum", "spend", "price", "cost"]
    count_keywords = ["count", "number", "quantity", "orders", "how many"]

    for col in numeric_cols:
        col_l = col.lower()
        if any(kw in col_l for kw in revenue_keywords) and any(kw in question_lower for kw in revenue_keywords):
            return col
        if any(kw in col_l for kw in count_keywords) and any(kw in question_lower for kw in count_keywords):
            return col

    # Default to the first numeric column
    return numeric_cols[0]


def _generate_title(question: str, chart_type: str) -> str:
    """Generate a clean chart title from the user question."""
    if not question:
        return "Query Results"

    # Clean up the question into a title
    title = question.strip().rstrip("?").strip()
    # Capitalize first letter
    if title:
        title = title[0].upper() + title[1:]
    return title
