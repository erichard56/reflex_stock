import reflex as rx

def fnc_logs_one(log):
	return rx.table.row(
		rx.table.cell(rx.text(log[0])),
		rx.table.cell(rx.text(log[1])),
		rx.table.cell(rx.text(log[2])),
		rx.table.cell(rx.text(log[3])),
		rx.table.cell(rx.text(log[4])),
	)

def fnc_logs(producto, logs) -> rx.Component:
	return rx.box(
		rx.flex(
			rx.card(
				rx.heading(producto),
			),
			rx.card(
				rx.table.root(
					rx.table.header( 
						rx.table.row(
							rx.table.column_header_cell('Tipo'),
							rx.table.column_header_cell('Desde'),
							rx.table.column_header_cell('Hasta'),
							rx.table.column_header_cell('Usuario'),
							rx.table.column_header_cell('Fecha'),
						),			
					),
					rx.table.body(
						rx.foreach(logs, fnc_logs_one)
					),
				),
			),
		),
		width='100%',
	)
