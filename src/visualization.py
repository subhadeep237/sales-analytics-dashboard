
"""
Visualization Module
Creates and saves charts for the sales analytics project.
"""

from pathlib import Path

import matplotlib.pyplot as plt


# Directory for saving charts
FIGURES_DIR = Path("results/figures")
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


# =====================================================
# 1. SALES BY REGION
# =====================================================

def plot_sales_by_region(region_df):
    plt.figure(figsize=(10, 6))

    plt.bar(
        region_df["region"],
        region_df["total_sales"]
    )

    plt.title("Total Sales by Region")
    plt.xlabel("Region")
    plt.ylabel("Total Sales")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    output_file = FIGURES_DIR / "sales_by_region.png"
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Saved chart: {output_file}")


# =====================================================
# 2. SALES BY CATEGORY
# =====================================================

def plot_sales_by_category(category_df):
    plt.figure(figsize=(9, 6))

    # The SQL query returns product_category, not category.
    plt.bar(
        category_df["product_category"],
        category_df["total_sales"]
    )

    plt.title("Total Sales by Product Category")
    plt.xlabel("Product Category")
    plt.ylabel("Total Sales")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()

    output_file = FIGURES_DIR / "sales_by_category.png"
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Saved chart: {output_file}")


# =====================================================
# 3. MONTHLY SALES TREND
# =====================================================

def plot_monthly_sales_trend(monthly_df):
    plt.figure(figsize=(12, 6))

    plt.plot(
        monthly_df["order_year_month"],
        monthly_df["total_sales"],
        marker="o",
        linewidth=2
    )

    plt.title("Monthly Sales Trend")
    plt.xlabel("Year-Month")
    plt.ylabel("Total Sales")

    # Display fewer date labels to avoid overcrowding.
    step = max(1, len(monthly_df) // 12)
    tick_positions = list(range(0, len(monthly_df), step))

    plt.xticks(
        tick_positions,
        monthly_df["order_year_month"].iloc[tick_positions],
        rotation=45,
        ha="right"
    )

    plt.tight_layout()

    output_file = FIGURES_DIR / "monthly_sales_trend.png"
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Saved chart: {output_file}")
