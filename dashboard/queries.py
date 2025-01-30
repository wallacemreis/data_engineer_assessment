import logging
from typing import Optional

import duckdb
import pandas as pd

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

DB_PATH = "/db/analytics.duckdb"


def execute_query(query: str, params: tuple = ()) -> Optional[pd.DataFrame]:
    """
    Executes an SQL query in DuckDB and returns the result as a Pandas DataFrame.

    Args:
        query (str): The SQL query to execute.
        params (tuple, optional): Query parameters (default is an empty tuple).

    Returns:
        Optional[pd.DataFrame]: The query result as a DataFrame, or None if empty.
    """
    try:
        with duckdb.connect(DB_PATH) as conn:
            result = conn.execute(query, params).df()
            return result if not result.empty else None
    except Exception as e:
        logging.error(f"Error executing query: {e}")
        return None


def get_sales_over_time() -> Optional[pd.DataFrame]:
    """
    Retrieves total sales and profit aggregated monthly.

    Returns:
        Optional[pd.DataFrame]: DataFrame with columns [month, total_sales, total_profit].
    """
    query = """
    SELECT 
        strftime('%Y-%m', order_date) AS month,
        SUM(adjusted_sales) AS total_sales,
        SUM(adjusted_profit) AS total_profit
    FROM main_analytics.fact_orders
    GROUP BY 1
    ORDER BY 1
    """
    return execute_query(query)


def get_top_categories(limit: int = 10) -> Optional[pd.DataFrame]:
    """
    Retrieves the top-selling product categories.

    Args:
        limit (int): Number of top categories to return (default is 10).

    Returns:
        Optional[pd.DataFrame]: DataFrame with columns [category, total_sales, total_profit].
    """
    query = """
    SELECT 
        p.category,
        SUM(foi.adjusted_sales) AS total_sales,
        SUM(foi.adjusted_profit) AS total_profit
    FROM main_analytics.fact_order_items foi
    JOIN main_analytics.dim_products p ON foi.product_sk = p.product_sk
    GROUP BY 1
    ORDER BY 2 DESC
    LIMIT ?
    """
    return execute_query(query, (limit,))


def get_return_rate() -> Optional[pd.DataFrame]:
    """
    Calculates the overall order return rate.

    Returns:
        Optional[pd.DataFrame]: DataFrame with a single column [return_rate].
    """
    query = """
    SELECT 
        SUM(CASE WHEN is_return_order THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS return_rate
    FROM main_analytics.fact_orders;
    """
    return execute_query(query)


def get_return_rate_per_customer() -> Optional[pd.DataFrame]:
    """
    Calculates the return rate per unique customer.

    Returns:
        Optional[pd.DataFrame]: DataFrame with a single column [return_rate_per_customer].
    """
    query = """
    SELECT 
        SUM(CASE WHEN is_return_order THEN 1 ELSE 0 END) * 100.0 / COUNT(DISTINCT customer_sk) AS return_rate_per_customer
    FROM main_analytics.fact_orders;
    """
    return execute_query(query)


def get_top_return_customers(limit: int = 5) -> Optional[pd.DataFrame]:
    """
    Retrieves the top 5 customers with the highest return rate.

    Args:
        limit (int): Number of customers to return (default is 5).

    Returns:
        Optional[pd.DataFrame]: DataFrame with columns [customer_name, total_orders, returned_orders, return_rate].
    """
    query = """
    SELECT 
        c.customer_name,
        COUNT(DISTINCT f.order_id) AS total_orders,
        COUNT(DISTINCT CASE WHEN f.is_return_order THEN f.order_id END) AS returned_orders,
        ROUND(
            COUNT(DISTINCT CASE WHEN f.is_return_order THEN f.order_id END) * 100.0 
            / COUNT(DISTINCT f.order_id), 2
        ) AS return_rate
    FROM main_analytics.fact_orders f
    JOIN main_analytics.dim_customers c ON f.customer_sk = c.customer_sk
    GROUP BY c.customer_name
    HAVING COUNT(DISTINCT f.order_id) > 5  
    ORDER BY return_rate DESC
    LIMIT ?;
    """
    return execute_query(query, (limit,))


def get_return_metrics() -> Optional[pd.DataFrame]:
    """
    Retrieves total returned orders and return rate per customer.

    Returns:
        Optional[pd.DataFrame]: DataFrame with columns [total_orders_returned, return_rate_per_customer].
    """
    query = """
    SELECT 
        SUM(CASE WHEN is_return_order THEN 1 ELSE 0 END) AS total_orders_returned,
        SUM(CASE WHEN is_return_order THEN 1 ELSE 0 END) * 100.0 / COUNT(DISTINCT customer_sk) AS return_rate_per_customer
    FROM main_analytics.fact_orders;
    """
    return execute_query(query)


def get_total_orders() -> Optional[pd.DataFrame]:
    """
    Retrieves the total number of unique orders.

    Returns:
        Optional[pd.DataFrame]: DataFrame with a single column [total_orders].
    """
    query = "SELECT COUNT(DISTINCT order_id) AS total_orders FROM main_analytics.fact_orders;"
    return execute_query(query)


def get_total_customers() -> Optional[pd.DataFrame]:
    """
    Retrieves the total number of unique customers.

    Returns:
        Optional[pd.DataFrame]: DataFrame with a single column [total_customers].
    """
    query = "SELECT COUNT(DISTINCT customer_sk) AS total_customers FROM main_analytics.fact_orders;"
    return execute_query(query)


def get_avg_ticket() -> Optional[pd.DataFrame]:
    """
    Calculates the average revenue per customer.

    Returns:
        Optional[pd.DataFrame]: DataFrame with a single column [avg_ticket].
    """
    query = """
    SELECT SUM(adjusted_sales) / COUNT(DISTINCT customer_sk) AS avg_ticket
    FROM main_analytics.fact_orders;
    """
    return execute_query(query)


def get_avg_orders_per_customer() -> Optional[pd.DataFrame]:
    """
    Calculates the average number of orders per customer.

    Returns:
        Optional[pd.DataFrame]: DataFrame with a single column [avg_orders_per_customer].
    """
    query = """
    SELECT COUNT(DISTINCT order_id) * 1.0 / COUNT(DISTINCT customer_sk) AS avg_orders_per_customer
    FROM main_analytics.fact_orders;
    """
    return execute_query(query)


def get_top_customers(limit: int = 10) -> Optional[pd.DataFrame]:
    """
    Retrieves the top customers based on total sales.

    Args:
        limit (int): Number of top customers to return (default is 10).

    Returns:
        Optional[pd.DataFrame]: DataFrame with columns [customer_name, total_sales].
    """
    query = """
    SELECT 
        c.customer_name,
        SUM(foi.adjusted_sales) AS total_sales
    FROM main_analytics.fact_order_items foi
    JOIN main_analytics.dim_customers c ON foi.customer_sk = c.customer_sk
    GROUP BY c.customer_name
    ORDER BY total_sales DESC
    LIMIT ?
    """
    return execute_query(query, (limit,))


def get_top_managers(limit: int = 10) -> Optional[pd.DataFrame]:
    """
    Retrieves the top managers based on total sales performance.

    Args:
        limit (int): Number of top managers to return (default is 10).

    Returns:
        Optional[pd.DataFrame]: DataFrame with columns [manager, total_sales].
    """
    query = """
    SELECT 
        m.manager,
        SUM(fo.adjusted_sales) AS total_sales
    FROM main_analytics.fact_orders fo
    JOIN main_analytics.dim_managers m ON fo.manager_id = m.manager_id
    GROUP BY m.manager
    ORDER BY total_sales DESC
    LIMIT ?
    """
    return execute_query(query, (limit,))


def get_avg_delivery_time() -> Optional[pd.DataFrame]:
    """
    Calculates the average delivery time.

    Returns:
        Optional[pd.DataFrame]: DataFrame with a single column [avg_delivery_time].
    """
    query = """
    SELECT AVG(avg_delivery_time) AS avg_delivery_time FROM main_analytics.fact_orders;
    """
    return execute_query(query)


def get_contribution_margin() -> Optional[pd.DataFrame]:
    """
    Calculates the contribution margin.

    Returns:
        Optional[pd.DataFrame]: DataFrame with a single column [contribution_margin].
    """
    query = """
    SELECT SUM(adjusted_profit) * 100.0 / SUM(adjusted_sales) AS contribution_margin FROM main_analytics.fact_orders;
    """
    return execute_query(query)


def get_net_revenue() -> Optional[pd.DataFrame]:
    """
    Retrieves the total net revenue, which is the sum of adjusted sales.

    Returns:
        Optional[pd.DataFrame]: DataFrame with a single column [net_revenue].
    """
    query = """
    SELECT 
        COALESCE(SUM(adjusted_sales), 0) AS net_revenue
    FROM main_analytics.fact_orders;
    """
    return execute_query(query)


def get_effective_profit_margin() -> Optional[pd.DataFrame]:
    """
    Calculates the effective profit margin as a percentage of adjusted sales.

    Returns:
        Optional[pd.DataFrame]: DataFrame with a single column [effective_profit_margin].
    """
    query = """
    SELECT 
        CASE 
            WHEN SUM(adjusted_sales) > 0 
            THEN (SUM(adjusted_profit) * 100.0) / SUM(adjusted_sales) 
            ELSE 0 
        END AS effective_profit_margin
    FROM main_analytics.fact_orders;
    """
    return execute_query(query)
