import reflex as rx
from .stocks_repository import letras_select_all, items_select_all, item_ingegr
from .stocks_repository import item_select_by_id, items_select_by_text
from .stocks_repository import get_usuario
			
from .notify import notify_component
import asyncio
import datetime

def chkCantidad(cantidad):
	try:
		n = int(cantidad)
		if (n > 0):
			return(n)
		else:
			return('Cantidad debe ser mayor que 0')
	except:
		return('Cantidad debe ser numerico')

class State(rx.State):
	role: int = 0
	usuario: str = ''
	opc: str = 'img'
	letras: list[tuple]
	letra: str
	productos: list[list]
	producto: str = ''
	id_producto: int = 0
	cantidad: str = 1
	producto_buscar: str = ''
	error: str = ''

	@rx.event()
	async def handle_notify(self):
		async with self:
			await asyncio.sleep(2)
			self.error = ''

	@rx.event(background=True)
	async def handle_ingresar(self, form_data: dict):
		async with self:
			self.role = get_usuario(form_data['usuario'], form_data['clave'])
			if (self.role > 0):
				self.usuario = form_data['usuario']
			else:
				self.error = 'Usuario o Clave invalidos'
		if (self.error != ''):
			await self.handle_notify()


	@rx.event(background=True)
	async def get_all_letras(self):
		async with self:
			self.letras = letras_select_all()
			self.letra = self.letras[0][0]
			self.productos = items_select_all(self.letra)
			self.id_producto = self.productos[0][0]
			self.producto = item_select_by_id(self.id_producto)

	@rx.event(background=True)
	async def get_letra(self, letra):
		async with self:
			self.productos = items_select_all(letra)
			self.letra = letra
			self.id_producto = self.productos[0][0]
			self.producto = item_select_by_id(self.id_producto)

	@rx.event(background=True)
	async def get_stock(self, id_producto):
		async with self:
			self.id_producto = id_producto
			self.producto = item_select_by_id(self.id_producto)

	# @rx.event(background=True)
	# async def delete_stock_by_id(self, id_stock, id_producto):
	# 	async with self:
	# 		self.stocks = delete_stock_service(id_stock, id_producto)

	@rx.event(background=True)
	async def decrementar(self, id_producto):
		async with self:
			item_ingegr('out', id_producto, 1)
			self.productos = items_select_all(self.letra)

	@rx.event(background=True)
	async def incrementar(self, id_producto):
		async with self:
			item_ingegr('in', id_producto, 1)
			self.productos = items_select_all(self.letra)

	@rx.event()
	def change_cantidad(self, value: str):
		self.cantidad = value

	@rx.event(background=True)
	async def agregar_stock(self, direccion, id_producto):
		async with self:
			cantidad = chkCantidad(self.cantidad)
			if (type(cantidad) == int):
				item_ingegr(direccion, id_producto, cantidad)
				self.productos = items_select_all(self.letra)
				self.producto = self.productos[0][1]
				self.id_producto = self.productos[0][0]
			else:
				self.error = cantidad

		if (self.error != ''):
			await self.handleNotify()


	def buscar_on_change(self, value: str):
		self.producto_buscar = value
		print(self.producto_buscar)

	@rx.event(background=True)
	async def get_productos(self):
		async with self:
			self.error = ''
			self.productos = items_select_by_text(self.producto_buscar)
			if (len(self.productos) > 0):
				self.producto = self.productos[0][1]
				self.letra = self.producto[0][0]
			else:
				self.error = 'No existen productos con esa busqueda'

		if (self.error != ''):
			await self.handleNotify()

	@rx.event()
	async def handleNotify(self):
		async with self:
			await asyncio.sleep(2)
			self.error = ''

@rx.page(route='/', title='Stocks', on_load=State.get_all_letras)
@rx.page(route='/stocks', title='Stocks', on_load=State.get_all_letras)
def stocks_page() -> rx.Component:
	return rx.box(
		rx.vstack(
			rx.card(
				rx.hstack(
					rx.image(
						src = 'logo3x.jpeg', 
						width = '40%',
						height = '100px',
						align = 'center'
					),
					rx.box(
						rx.cond(
							State.role == 0,
							fnc_ingresar(),
							rx.hstack(
								rx.text('Hola ', State.usuario),
								rx.button('Salir')
							),
						),
						margin_x='20px',
						margin_y='20px',
					),
				),
				width='100%',
			),
			rx.box(
				rx.cond(
					State.role > 0,
					fnc_menu(),
				)
			)
		),
		# rx.match(
		# 	State.opc,
		# 	('sal', rx.text('fnc_salir()')),
		# ),
		rx.cond(
			State.error != '',
			notify_component(
					State.error,
					'shield_alert',
					'yellow'
				),
		),
		direction = 'column',
		style = { 'width':'80%', 'margin':'auto' },
		spacing ='2'
	)
	
def fnc_ingresar() -> rx.Component:
	return rx.form(
		rx.hstack(
			rx.input(placeholder='Usuario', type='text', name='usuario'),
			rx.input(placeholder='Clave', type='password', name='clave'),
			rx.button(rx.icon('smile'), 'Ingresar', type='submit'),
		),
		on_submit=State.handle_ingresar,
		reset_on_submit=True,
	)

def fnc_menu() -> rx.Component:
	return rx.box(
		# rx.hstack(
		# 	rx.foreach(State.letras, row_letras),
		# 	justify = 'center',
		# 	style = { 'margin_top':'1px' }
		# ),
		rx.center(
			rx.hstack(
				rx.input( placeholder = 'Producto??', on_change = State.buscar_on_change ),
				rx.button( 'Buscar', on_click = State.get_productos ),
			),
		),
		table_producto(State.producto_buscar),
		rx.cond(
			State.error != '',
			notify_component(
					State.error,
					'shield_alert',
					'yellow'
				),
		),

		# rx.box(
		# 	rx.hstack(
		# 		# rx.button(rx.icon('users-round'), 'Personas', on_click=State.evt_personas()),
		# 		# rx.button(rx.icon('calendar-days'), 'Agenda', on_click=State.evt_agendas_lista()),
		# 		# rx.button(rx.icon('ticket'), 'Eventos', on_click=State.evt_eventos_lista()),
		# 		# rx.button(rx.icon('house'), 'Casas', on_click=State.evt_casas_lista()),
		# 		# rx.button(rx.icon('graduation-cap'), 'Grados', on_click=State.evt_grados_lista()),
		# 		# rx.button(rx.icon('list'), 'Tipo Eventos', on_click=State.evt_tipoeventos_lista()),
		# 		# rx.button(rx.icon('list'), 'Extras', on_click=State.evt_tipoextras_lista()),
		# 	),
		# ),
		width='100%',
	)

def row_letras(letra: tuple) -> rx.Component:
	return rx.button(
			letra[0], 
			on_click = State.get_letra(letra[0])
		)

def table_producto(busq) -> rx.Component:
	return rx.card(
		rx.table.root(
			rx.table.header( 
				rx.table.row(
					rx.table.column_header_cell('Producto', width='30%'),
					rx.table.column_header_cell('Deposito', width='20%'),
					rx.table.column_header_cell('Stock', width='10%'),
					rx.table.column_header_cell('Precio', width='10%'),
					rx.table.column_header_cell('Precio de Venta', width='10%'),
					rx.table.column_header_cell('Imagen', width='10%'),
					rx.table.column_header_cell('Acciones', width='10%')
				),			
			),
			rx.cond(
				busq != '',
				rx.table.body(
					rx.foreach(State.productos, row_productos)
				),
			),
		),
	)

def row_productos(producto) -> rx.Component:
	return rx.table.row(
		rx.table.cell(rx.text(producto[1])),
		rx.table.cell(rx.text(producto[2])),
		rx.table.cell(rx.text(producto[3])),
		rx.table.cell(rx.text(producto[4])),
		rx.table.cell(rx.text(producto[5])),
		rx.image(src=producto[6], width='50%'),
		rx.table.cell(
			rx.hstack(
				rx.button(rx.icon("plus", on_click = State.incrementar(producto[0]))),
				# rx.button(rx.icon('trash-2')), #, on_click = State.delete_stock_by_id(producto[0]))),
				rx.button(rx.icon("minus", on_click = State.decrementar(producto[0]))),
				ingegr('in', producto[0]),
				ingegr('out', producto[0]),
				# rx.button('Ingreso', on_click = State.agregar_stock(State.id_producto) ),
				# rx.button('Salida', on_click = State.agregar_stock(State.id_producto) ),
			)
		),
	)

def ingegr(direccion, id) -> rx.Component:
	return rx.box(
		rx.dialog.root(
			rx.cond(
				direccion == 'in', 
				rx.dialog.trigger(rx.button("Ingreso")),
				rx.dialog.trigger(rx.button("Egreso")),
			),
			rx.dialog.content(
				rx.hstack(
					rx.cond(
						direccion == 'in', 
						rx.dialog.title(rx.button("Ingreso")),
						rx.dialog.title(rx.button("Egreso")),
					),
					rx.text("Cantidad: ", margin_bottom="4px", weight="bold"),
					rx.input(default_value="1", placeholder="1", on_change=State.change_cantidad()),
					rx.dialog.close(rx.button("Cancel", color_scheme="gray", variant="soft")),
					rx.dialog.close(rx.button("Save"), on_click=State.agregar_stock(direccion, id)),
				),
				spacing="3",
			),
		)
	)

app = rx.App()
app.add_page(stocks_page)

