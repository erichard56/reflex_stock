import reflex as rx
from .service.stocks_page import stocks_page

app = rx.App()
app.add_page(stocks_page)

