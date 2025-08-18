import reflex as rx

config = rx.Config(
    app_name="reflex_stock",
    disable_plugins=[
        "reflex.plugins.sitemap.SitemapPlugin",
        # Add other plugins to disable here if needed
    ],
    db_url="sqlite:///stock.db"
)