# """Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from .service.stocks_page import stocks_page

# class State(rx.State):
# 	"""The app state."""

# 	...

# def hstack(letra) -> rx.Component:
# 	return rx.table.column_header_cell(
# 			rx.link(
# 				letra,
# 				href = '/productos/' + str(letra)
# 			)
# 		)

# def hstack2(producto) -> rx.Component:
# 	return rx.table.column_header_cell(
# 			rx.link(
# 				producto.producto,
# 				href = '/productos/' + str(producto.id)
# 			)
# 		)


	


# @rx.page(route='/')
# def index() -> rx.Component:
# 	return rx.text('hola')



# 	letra = '3'

# 	q1 = 'SELECT * FROM productos WHERE SUBSTR(producto, 1, 1) = ' + \
# 		letra + ' ORDER BY producto'
# 	cursor.execute(q1)
# 	productos = cursor.fetchall()

# 	# id_producto = productos[0][0]

# 	q1 = 'SELECT * FROM stocks where id_producto = ' + str(1)
# 	cursor.execute(q1)
# 	stocks = cursor.fetchall()

	# return rx.container(
		# rx.table.root(
		# 	rx.table.header(
		# 		rx.table.row(
		# 			rx.table.column_header_cell('Vero Stock')
		# 		)
		# 	),
		# ),
# 		rx.table.root(
# 			rx.table.header(
# 				rx.table.row(
# 					rx.foreach(letras, hstack)
# 				)
# 			),
# 		),
# 		rx.table.root(
# 			rx.table.header(
# 				rx.table.row(
# 					rx.table.column_header_cell('Productos'),
# 					rx.table.column_header_cell('Stocks')
# 				),
# 			),
# 			rx.table.body(
# 				rx.table.row(
# 					rx.foreach(productos, hstack2)
# 				)
# 			)
# 		),
	# 	spacing="5",
	# 	justify="center",
	# 	min_height="85vh",
	# )

app = rx.App()
app.add_page(stocks_page)
# app.add_page(productos, route='/productos/[letra]')
