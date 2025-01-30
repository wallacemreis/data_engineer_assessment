import dash
import dash.dash_table as dt
import plotly.express as px
import queries

dark_theme = {
    "background": "#000000",
    "text": "#EAEAEA",
    "card": "#000000",
    "border": "#333333",
    "primary": "#FFB74D",
    "font": {
        "family": "'Inter', 'Roboto', sans-serif",
        "weight_title": "600",
        "weight_text": "500",
        "size_title": "24px",
        "size_text": "16px",
    },
}


def create_figure(df, x, y, title, chart_type="line"):
    fig = (
        px.line(df, x=x, y=y, title=title)
        if chart_type == "line"
        else px.bar(df, x=x, y=y, title=title)
    )

    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor=dark_theme["background"],
        paper_bgcolor=dark_theme["background"],
        font=dict(family=dark_theme["font"]["family"], color=dark_theme["text"]),
        xaxis=dict(title_text=x.replace("_", " ").title()),
        yaxis=dict(
            title_text="Metric" if isinstance(y, list) else y.replace("_", " ").title()
        ),
    )

    if chart_type == "bar":
        fig.update_traces(texttemplate="%{y:,.2f}", textposition="auto")

    return fig


app = dash.Dash(__name__)

df_sales = queries.get_sales_over_time()
df_categories = queries.get_top_categories()
df_returns = queries.get_return_rate()
df_return_metrics = queries.get_return_metrics()
df_total_orders = queries.get_total_orders()
df_total_customers = queries.get_total_customers()
df_avg_ticket = queries.get_avg_ticket()
df_avg_orders_per_customer = queries.get_avg_orders_per_customer()
df_return_rate_per_customer = queries.get_return_rate_per_customer()
df_top_return_customers = queries.get_top_return_customers()
df_top_customers = queries.get_top_customers()
df_top_managers = queries.get_top_managers()
df_avg_delivery_time = queries.get_avg_delivery_time()
df_contribution_margin = queries.get_contribution_margin()
df_net_revenue = queries.get_net_revenue()
df_effective_profit_margin = queries.get_effective_profit_margin()

fig_sales = create_figure(
    df_sales, "month", ["total_sales", "total_profit"], "Sales and Profit Over Time"
)
fig_categories = create_figure(
    df_categories, "category", "total_sales", "Top 10 Best-Selling Categories", "bar"
)
fig_top_customers = create_figure(
    df_top_customers, "customer_name", "total_sales", "Top Customers by Sales", "bar"
)
fig_top_managers = create_figure(
    df_top_managers, "manager", "total_sales", "Top Performing Managers", "bar"
)

table_top_return_customers = dt.DataTable(
    columns=[
        {"name": "Customer Name", "id": "customer_name"},
        {"name": "Total Orders", "id": "total_orders"},
        {"name": "Returned Orders", "id": "returned_orders"},
        {"name": "Return Rate (%)", "id": "return_rate"},
    ],
    data=df_top_return_customers.to_dict("records"),
    style_header={
        "backgroundColor": dark_theme["card"],
        "color": dark_theme["primary"],
        "fontWeight": "bold",
        "textAlign": "center",
    },
    style_cell={
        "backgroundColor": dark_theme["card"],
        "color": dark_theme["text"],
        "textAlign": "center",
    },
    style_table={"margin": "auto"},
)


def create_kpi_card(title, value):
    return dash.html.Div(
        [
            dash.html.H3(
                title,
                style={
                    "color": dark_theme["primary"],
                    "fontFamily": dark_theme["font"]["family"],
                    "fontWeight": dark_theme["font"]["weight_title"],
                    "textAlign": "center",
                },
            ),
            dash.html.H2(
                f"{value}",
                style={
                    "fontSize": dark_theme["font"]["size_title"],
                    "color": dark_theme["text"],
                    "fontFamily": dark_theme["font"]["family"],
                    "fontWeight": dark_theme["font"]["weight_text"],
                    "textAlign": "center",
                },
            ),
        ],
        style={
            "textAlign": "center",
            "padding": "15px",
            "border": f"1px solid {dark_theme['border']}",
            "backgroundColor": dark_theme["card"],
            "borderRadius": "10px",
            "width": "230px",
            "height": "110px",
            "margin": "10px",
            "display": "inline-flex",
            "alignItems": "center",
            "justifyContent": "center",
            "flexDirection": "column",
        },
    )


app.layout = dash.html.Div(
    children=[
        dash.html.H1(
            "Sales Dashboard",
            style={
                "textAlign": "center",
                "color": dark_theme["text"],
                "fontFamily": dark_theme["font"]["family"],
                "fontWeight": dark_theme["font"]["weight_title"],
            },
        ),
        # Sales and Categories
        dash.dcc.Graph(id="sales_graph", figure=fig_sales),
        dash.dcc.Graph(id="category_graph", figure=fig_categories),
        # Returns Overview
        dash.html.Div(
            [
                dash.html.H3(
                    "Returns Overview",
                    style={
                        "color": dark_theme["primary"],
                        "fontFamily": dark_theme["font"]["family"],
                        "fontWeight": dark_theme["font"]["weight_title"],
                        "fontSize": dark_theme["font"]["size_title"],
                    },
                ),
                create_kpi_card("Return Rate", f"{df_returns.iloc[0, 0]:.2f}%"),
                create_kpi_card(
                    "Total Orders Returned",
                    f"{df_return_metrics.iloc[0, 0]:,.0f}",
                ),
                create_kpi_card(
                    "Return Rate per Customer",
                    f"{df_return_metrics.iloc[0, 1]:.2f}%",
                ),
                dash.html.H4(
                    "Top 5 Customers with Highest Return Rates",
                    style={
                        "color": dark_theme["primary"],
                        "textAlign": "center",
                        "marginTop": "20px",
                        "fontFamily": dark_theme["font"]["family"],
                    },
                ),
                table_top_return_customers,
            ],
            style={
                "textAlign": "center",
                "padding": "20px",
                "border": f"1px solid {dark_theme['border']}",
                "backgroundColor": dark_theme["card"],
                "borderRadius": "10px",
            },
        ),
        # Customer Insights
        dash.html.Div(
            [
                dash.html.H3(
                    "Customer Insights",
                    style={
                        "color": dark_theme["primary"],
                        "fontFamily": dark_theme["font"]["family"],
                        "fontWeight": dark_theme["font"]["weight_title"],
                        "fontSize": dark_theme["font"]["size_title"],
                    },
                ),
                create_kpi_card(
                    "Total Customers", f"{df_total_customers.iloc[0, 0]:,.0f}"
                ),
                create_kpi_card("Avg Ticket Size", f"${df_avg_ticket.iloc[0, 0]:,.2f}"),
                create_kpi_card(
                    "Avg Orders per Customer",
                    f"{df_avg_orders_per_customer.iloc[0, 0]:,.1f}",
                ),
                dash.dcc.Graph(id="top_customers", figure=fig_top_customers),
            ],
            style={
                "textAlign": "center",
                "padding": "20px",
                "border": f"1px solid {dark_theme['border']}",
                "backgroundColor": dark_theme["card"],
                "borderRadius": "10px",
            },
        ),
        # Manager Performance
        dash.dcc.Graph(id="top_managers", figure=fig_top_managers),
        # Financial Performance
        dash.html.Div(
            [
                dash.html.H3(
                    "Financial Performance",
                    style={
                        "color": dark_theme["primary"],
                        "fontFamily": dark_theme["font"]["family"],
                        "fontWeight": dark_theme["font"]["weight_title"],
                        "fontSize": dark_theme["font"]["size_title"],
                    },
                ),
                create_kpi_card(
                    "Contribution Margin", f"{df_contribution_margin.iloc[0, 0]:.2f}%"
                ),
                create_kpi_card("Net Revenue", f"${df_net_revenue.iloc[0, 0]:,.2f}"),
                create_kpi_card(
                    "Effective Profit Margin",
                    f"{df_effective_profit_margin.iloc[0, 0]:.2f}%",
                ),
            ],
            style={
                "textAlign": "center",
                "padding": "20px",
                "border": f"1px solid {dark_theme['border']}",
                "backgroundColor": dark_theme["card"],
                "borderRadius": "10px",
            },
        ),
        # Logistics Performance
        dash.html.Div(
            [
                dash.html.H3(
                    "Logistics Performance",
                    style={
                        "color": dark_theme["primary"],
                        "fontFamily": dark_theme["font"]["family"],
                        "fontWeight": dark_theme["font"]["weight_title"],
                        "fontSize": dark_theme["font"]["size_title"],
                    },
                ),
                create_kpi_card(
                    "Avg Delivery Time", f"{df_avg_delivery_time.iloc[0, 0]:.1f} days"
                ),
            ],
            style={
                "textAlign": "center",
                "padding": "20px",
                "border": f"1px solid {dark_theme['border']}",
                "backgroundColor": dark_theme["card"],
                "borderRadius": "10px",
            },
        ),
    ],
    style={
        "backgroundColor": dark_theme["background"],
        "color": dark_theme["text"],
        "padding": "20px",
    },
)

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8051)
