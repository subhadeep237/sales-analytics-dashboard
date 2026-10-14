
from src.data_loader import load_raw_sales_data, print_data_summary
from src.cleaning import clean_sales_data, save_cleaned_data
from src.database import create_database

from src.analysis import (
    calculate_main_kpis,
    sales_by_region,
    sales_by_category,
    monthly_sales_trend,
    top_products_by_sales,
    save_analysis_outputs,
)

from src.visualization import (
    plot_sales_by_region,
    plot_sales_by_category,
    plot_monthly_sales_trend,
)


def main():
    print("=" * 60)
    print("SALES ANALYTICS DASHBOARD PROJECT")
    print("=" * 60)

    # 1. Load raw dataset
    raw_df = load_raw_sales_data()

    print("\nRAW DATA SUMMARY")
    print("=" * 60)
    print_data_summary(raw_df)

    # 2. Clean the dataset
    cleaned_df = clean_sales_data(raw_df)

    print("\nCLEANED DATA")
    print("=" * 60)
    print("Rows and columns:", cleaned_df.shape)

    print("\nCleaned columns:")
    for column in cleaned_df.columns:
        print("-", column)

    # 3. Save cleaned data
    save_cleaned_data(cleaned_df)

    # 4. Create SQLite database
    create_database(cleaned_df)

    # 5. Calculate main KPIs
    print("\nMAIN KPIs")
    print("=" * 60)

    main_kpis = calculate_main_kpis()
    print(main_kpis.to_string(index=False))

    # 6. Sales by region
    print("\nSALES BY REGION")
    print("=" * 60)

    region_df = sales_by_region()
    print(region_df.to_string(index=False))

    # 7. Sales by product category
    print("\nSALES BY CATEGORY")
    print("=" * 60)

    category_df = sales_by_category()
    print(category_df.to_string(index=False))

    # 8. Monthly sales trend
    print("\nMONTHLY SALES TREND")
    print("=" * 60)

    monthly_df = monthly_sales_trend()
    print(monthly_df.head(10).to_string(index=False))

    # 9. Top products
    print("\nTOP 10 PRODUCTS BY SALES")
    print("=" * 60)

    top_products_df = top_products_by_sales()
    print(top_products_df.to_string(index=False))

    # 10. Save analysis results as CSV files
    print("\nSAVING ANALYSIS OUTPUTS")
    print("=" * 60)

    save_analysis_outputs()

    # 11. Generate charts
    print("\nGENERATING CHARTS")
    print("=" * 60)

    plot_sales_by_region(region_df)
    plot_sales_by_category(category_df)
    plot_monthly_sales_trend(monthly_df)

    print("\n" + "=" * 60)
    print("PROJECT COMPLETED SUCCESSFULLY!")
    print("=" * 60)


if __name__ == "__main__":
    main()
