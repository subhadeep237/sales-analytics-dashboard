
"""
Sales Analysis Module
Analyzes sales data using SQLite queries
and saves analysis results as CSV files.
"""

from pathlib import Path

from src.database import run_query


# =====================================================
# 1. MAIN KPIs
# =====================================================

def calculate_main_kpis():
    query = """
        SELECT
            ROUND(COALESCE(SUM(sales), 0), 2) AS total_sales,
            ROUND(COALESCE(SUM(profit), 0), 2) AS total_profit,
            COUNT(DISTINCT order_id) AS total_orders,
            COUNT(DISTINCT customer_name) AS total_customers,
            ROUND(
                1.0 * COALESCE(SUM(profit), 0)
                / NULLIF(SUM(sales), 0),
                4
            ) AS profit_margin
        FROM sales;
    """

    return run_query(query)


# =====================================================
# 2. SALES BY REGION
# =====================================================

def sales_by_region():
    query = """
        SELECT
            region,
            ROUND(SUM(sales), 2) AS total_sales,
            ROUND(SUM(profit), 2) AS total_profit
        FROM sales
        GROUP BY region
        ORDER BY total_sales DESC;
    """

    return run_query(query)


def calculate_sales_by_region():
    return sales_by_region()


# =====================================================
# 3. SALES BY CATEGORY
# =====================================================

def sales_by_category():
    query = """
        SELECT
            product_category,
            ROUND(SUM(sales), 2) AS total_sales,
            ROUND(SUM(profit), 2) AS total_profit
        FROM sales
        GROUP BY product_category
        ORDER BY total_sales DESC;
    """

    return run_query(query)


def calculate_sales_by_category():
    return sales_by_category()


# =====================================================
# 4. MONTHLY SALES TREND
# =====================================================

def monthly_sales_trend():
    query = """
        SELECT
            order_year,
            order_month,
            order_year_month,
            ROUND(SUM(sales), 2) AS total_sales,
            ROUND(SUM(profit), 2) AS total_profit
        FROM sales
        GROUP BY
            order_year,
            order_month,
            order_year_month
        ORDER BY order_year, order_month;
    """

    return run_query(query)


def calculate_monthly_sales():
    return monthly_sales_trend()


# =====================================================
# 5. TOP PRODUCTS BY SALES
# =====================================================

def top_products_by_sales(limit=10):
    limit = max(1, min(int(limit), 100))

    query = f"""
        SELECT
            product_name,
            product_category,
            ROUND(SUM(sales), 2) AS total_sales,
            ROUND(SUM(profit), 2) AS total_profit,
            SUM(order_quantity) AS total_quantity
        FROM sales
        GROUP BY product_name, product_category
        ORDER BY total_sales DESC
        LIMIT {limit};
    """

    return run_query(query)


def top_products(limit=10):
    return top_products_by_sales(limit)


def calculate_top_products(limit=10):
    return top_products_by_sales(limit)


# =====================================================
# 6. TOP CUSTOMERS BY SALES
# =====================================================

def top_customers_by_sales(limit=10):
    limit = max(1, min(int(limit), 100))

    query = f"""
        SELECT
            customer_name,
            ROUND(SUM(sales), 2) AS total_sales,
            ROUND(SUM(profit), 2) AS total_profit,
            COUNT(DISTINCT order_id) AS total_orders
        FROM sales
        GROUP BY customer_name
        ORDER BY total_sales DESC
        LIMIT {limit};
    """

    return run_query(query)


def top_customers(limit=10):
    return top_customers_by_sales(limit)


def calculate_top_customers(limit=10):
    return top_customers_by_sales(limit)


# =====================================================
# 7. SALES BY CUSTOMER SEGMENT
# =====================================================

def sales_by_segment():
    query = """
        SELECT
            customer_segment,
            ROUND(SUM(sales), 2) AS total_sales,
            ROUND(SUM(profit), 2) AS total_profit,
            COUNT(DISTINCT order_id) AS total_orders
        FROM sales
        GROUP BY customer_segment
        ORDER BY total_sales DESC;
    """

    return run_query(query)


def calculate_sales_by_segment():
    return sales_by_segment()


# =====================================================
# 8. SALES BY SHIPPING MODE
# =====================================================

def sales_by_ship_mode():
    query = """
        SELECT
            ship_mode,
            ROUND(SUM(sales), 2) AS total_sales,
            ROUND(SUM(profit), 2) AS total_profit,
            COUNT(DISTINCT order_id) AS total_orders
        FROM sales
        GROUP BY ship_mode
        ORDER BY total_sales DESC;
    """

    return run_query(query)


def calculate_sales_by_ship_mode():
    return sales_by_ship_mode()


# =====================================================
# 9. SAVE ANALYSIS OUTPUTS
# =====================================================

def save_analysis_outputs():
    """
    Run the analysis queries and save their results
    as CSV files inside data/processed/analysis/.
    """

    output_dir = Path("data/processed/analysis")
    output_dir.mkdir(parents=True, exist_ok=True)

    analyses = {
        "main_kpis": calculate_main_kpis(),
        "sales_by_region": sales_by_region(),
        "sales_by_category": sales_by_category(),
        "monthly_sales_trend": monthly_sales_trend(),
        "top_products_by_sales": top_products_by_sales(),
        "top_customers_by_sales": top_customers_by_sales(),
        "sales_by_segment": sales_by_segment(),
        "sales_by_ship_mode": sales_by_ship_mode(),
    }

    for name, df in analyses.items():
        output_file = output_dir / f"{name}.csv"

        df.to_csv(output_file, index=False)

        print(f"Saved: {output_file}")

    print("\nAll analysis results saved successfully!")

    return analyses
