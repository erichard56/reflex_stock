import reflex as rx
from ..model.stocks_model import Producto, Stock, StockLapso
from .stocks_service import letras_select_all_service, productos_select_all_service, stocks_select_all_service, \
			producto_select_by_id_service, \
			delete_stock_service, decrementar_stock_service, incrementar_stock_service, agregar_stock_service
# from .notify import notify_component
import asyncio
import datetime

meses = [ 'filler',
		  'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
		  'Julio', 'Agosto', 'Septiembre', 'Noviembre', 'Diciembre' ]
class StockState(rx.State):
	letras: list[tuple]
	productos: list[tuple[Producto]]
	stocks: list[tuple[StockLapso]]
	producto: str = ''
	cantidad: str = '1'
	mes: str = meses[datetime.date.today().month]
	anio: str = str(datetime.date.today().year)
	# user_buscar: str
	# error: str = ''

	@rx.event(background=True)
	async def get_all_letras(self):
		async with self:
			self.letras = letras_select_all_service()
			self.productos = productos_select_all_service(self.letras[0][0])
			self.producto = producto_select_by_id_service(self.productos[0][0])
			self.stocks = stocks_select_all_service(self.productos[0][0])

	@rx.event(background=True)
	async def get_letra(self, letra):
		async with self:
			self.productos = productos_select_all_service(letra)
			self.producto = producto_select_by_id_service(self.productos[0][0])
			self.stocks = stocks_select_all_service(self.productos[0][0])

	@rx.event(background=True)
	async def get_stock(self, id_producto):
		async with self:
			self.producto = producto_select_by_id_service(id_producto)
			self.stocks = stocks_select_all_service(id_producto)

	@rx.event(background=True)
	async def delete_stock_by_id(self, id_stock, id_producto):
		async with self:
			self.stocks = delete_stock_service(id_stock, id_producto)

	@rx.event(background=True)
	async def decrementar(self, id_stock, id_producto):
		async with self:
			self.stocks = decrementar_stock_service(id_stock, id_producto)

	@rx.event(background=True)
	async def incrementar(self, id_stock, id_producto):
		async with self:
			self.stocks = incrementar_stock_service(id_stock, id_producto)

	@rx.event()
	def change_cantidad(self, value: str):
		self.cantidad = value

	@rx.event()
	def change_mes(self, value: str):
		self.mes = value

	@rx.event()
	def change_anio(self, value: str):
		self.anio = value

	@rx.event()
	def agregar_stock(self, id_producto):
		imes = meses.index(self.mes) + 1
		agregar_stock_service(id_producto, self.cantidad, imes, self.anio)
		self.stocks = stocks_select_all_service(id_producto)

	# @rx.event(background=True)
	# async def agregar_stock(self): #, data: dict):
		# pass
		# async with self:
		# 	pass
		# 	try:
		# 		self.users = create_user_service(username=data['username'], password=data['password'],
		# 					phone=data['phone'], name=data['name'])
		# 	except BaseException as be:
		# 		print(be.args)
		# 		self.error = be.args
		# await self.handleNotify()

	# @rx.event(background=True)
	# async def get_user_by_email(self):
	# 	async with self:
	# 		self.users = select_user_by_email_service(self.user_buscar)

	# async def handleNotify(self):
	# 	async with self:
	# 		await asyncio.sleep(2)
	# 		self.error = ''

	# @rx.event(background=True)
	# async def create_user(self, data: dict):
	# 	async with self:
	# 		try:
	# 			self.users = create_user_service(username=data['username'], password=data['password'],
	# 						phone=data['phone'], name=data['name'])
	# 		except BaseException as be:
	# 			print(be.args)
	# 			self.error = be.args
	# 	await self.handleNotify()
		
	# def buscar_on_change(self, value: str):
	# 	self.user_buscar = value

	# @rx.event(background=True)
	# async def delete_user_by_email(self, email):
	# 	async with self:
	# 		self.users = delete_user_service(email)


@rx.page(route='/stocks', title='Stocs Vero', on_load=StockState.get_all_letras)
def stocks_page() -> rx.Component:
	return rx.flex(
		rx.heading(
			'Stocks Vero', 
			align='center'
		),
		rx.hstack(
			rx.foreach(StockState.letras, row_letras)
		),
		rx.flex(
			table_producto(),
			table_stock(),
		),
		# rx.hstack(
		# 	buscar_user_component(),
		# 	create_user_dialogo_component(),
		# 	justify = 'center',
		# 	style = {'margin_top':'30px'}
		# ),
		# table_use(UserState.users),
		# rx.cond(
		# 	UserState.error != '',
		# 	notify_component(
		# 			UserState.error,
		# 			'shield_alert',
		# 			'yellow'
		# 		),
		# ),
		direction = 'column',
		style = {'width':'72vw', 'margin':'auto'},
		spacing ='2'
	)

def row_letras(letra: tuple) -> rx.Component:
	return rx.button(
			letra[0], 
			on_click=StockState.get_letra(letra[0])
		)

def table_producto() -> rx.Component:
	return rx.table.root(
		rx.table.header( 
			rx.table.row(
				rx.table.column_header_cell(
					rx.heading('Productos'),
					justify = 'center',
					min_width='33vw'
				),
			),			
		),
		rx.table.body(
			rx.foreach(StockState.productos, row_productos)
		),
		style= {'border': 'thick double'},
	)

def row_productos(producto: Producto) -> rx.Component:
	return rx.table.row(
		rx.table.cell(
		rx.button(
			producto[1], 
			variant='ghost',
			size='3',
			on_click=StockState.get_stock(producto[0])
		),
		align='right',
		)
	)

def table_stock() -> rx.Component:
	return rx.table.root(
		rx.table.header( 
			rx.table.row(
				rx.table.column_header_cell(
					rx.heading(
						StockState.producto.replace('"', ''), 
						color_scheme='orange',
					),
					min_width='33vw',
					justify='center', 
					col_span=4,
				),
			),
			rx.table.row(
				rx.table.column_header_cell('Cantidad', justify = 'center'),
				rx.table.column_header_cell('Vencimiento', justify = 'center'),
				rx.table.column_header_cell('Meses', justify = 'center'),
				rx.table.column_header_cell('Acciones', justify = 'center'),
			),			
		),
		rx.table.body(
			rx.foreach(StockState.stocks, row_stocks),
			rx.table.row(
				rx.table.cell(
					rx.select(
						[str(i) for i in range(1, 20)],
						value = StockState.cantidad, # '1',
						on_change=StockState.change_cantidad()
					),
				),
				rx.table.cell(
					rx.select(
						[ mes for mes in meses ],
						value = StockState.mes,
						on_change=StockState.change_mes()
					)
				),
				rx.table.cell(
					rx.select(
						[str(i) for i in range(datetime.date.today().year - 3, datetime.date.today().year + 5)],
						value = StockState.anio,
						on_change=StockState.change_anio()
					),
				),
				rx.table.cell(
					rx.button(
						'Agregar', 
						size = '2',
						on_click=StockState.agregar_stock(31)
					)
				),
			)
		),
		style= {'border': 'thick double'},
	)

def row_stocks(stock: StockLapso) -> rx.Component:
	return rx.table.row(
		rx.table.cell(stock[1], justify = 'center'),
		rx.table.cell(stock[3], justify = 'center'),
		rx.table.cell(stock[4], justify = 'center', style={'background_color':'red'}),
		rx.table.cell(
			rx.hstack(
				delete_stock_dialogo_component(stock[0], stock[2]),
				rx.button(
					rx.icon("minus", on_click=StockState.decrementar(stock[0], stock[2])),
				),
				rx.button(
        			rx.icon("plus", on_click=StockState.incrementar(stock[0], stock[2])),
				)
			)
		),
	)

def delete_stock_dialogo_component(id_stock: int, id_producto: int) -> rx.Component:
	return rx.dialog.root(
		rx.dialog.trigger(
			rx.button(
				rx.icon('trash-2')
			)
		),
		rx.dialog.content(
			rx.dialog.title('Eliminar entrada'),
			rx.dialog.description('Está seguro de quere eliminar??'),
			rx.flex(
				rx.dialog.close(
					rx.button(
						'Cancelar',
						color_scheme = 'gray',
						variant = 'soft'
					),
				),
				rx.dialog.close(
					rx.button(
						'Confirmar', 
						on_click=StockState.delete_stock_by_id(id_stock, id_producto)),
				),
				spacing = '3',
				margin_top = '16px',
				justify = 'end',
			)
		)
	)



# rx.table.row(
# 		rx.table.cell(user.name),
# 		rx.table.cell(user.username),
# 		rx.table.cell(user.phone),
# 		rx.table.cell(
# 			rx.hstack(
# 				delete_user_dialogo_component(user.username),
# 			)
# 		)
# 	)

# def table_use(list_user: list[User]) -> rx.Component:
# 		return rx.table.root(
# 			 rx.table.header(
# 				rx.table.row(
# 					 rx.table.column_header_cell('Nombre'),
# 					 rx.table.column_header_cell('Email'),
# 					 rx.table.column_header_cell('Telefono'),
# 					 rx.table.column_header_cell('Accion')
# 				)
# 			 ),
# 			 rx.table.body(
# 				rx.foreach(list_user, row_table)
# 			 )
# 		)

# def row_table(user: User) -> rx.Component:
# 	return rx.table.row(
# 		rx.table.cell(user.name),
# 		rx.table.cell(user.username),
# 		rx.table.cell(user.phone),
# 		rx.table.cell(
# 			rx.hstack(
# 				delete_user_dialogo_component(user.username),
# 			)
# 		)
# 	)

# def buscar_user_component() -> rx.Component:
# 	return rx.hstack(
# 		rx.input(placeholder='Ingrese email', on_change=UserState.buscar_on_change),
# 		rx.button('Buscar usuario', on_click=UserState.get_user_by_email)
# 	)

# def create_user_dialogo_component() -> rx.Component:
# 	return rx.dialog.root(
# 		rx.dialog.trigger(rx.button('Crear usuario')),
# 		rx.dialog.content(
# 			rx.flex(
# 				rx.dialog.title('Crear usuario'),
# 				create_user_form(),
# 				justify = 'center',
# 				align = 'center',
# 				direction = 'column',
# 			),
# 			rx.flex(
# 				rx.dialog.close(
# 					rx.button('Cancelar', color_scheme='gray', variant='soft')
# 				),
# 				spacing = '3',
# 				margin_top = '16px',
# 				justify = 'end'
# 			),
# 			style = {'width':'300px'}
# 		),
# 	)

# def create_user_form() -> rx.Component:
# 	return rx.form(
# 		rx.vstack(
# 			rx.input(
# 				placeholder = 'Nombre',
# 				name = 'name'
# 			),
# 			rx.input(
# 				placeholder = 'Email',
# 				name = 'username'
# 			),
# 			rx.input(
# 				placeholder = 'Contraseña',
# 				name = 'password',
# 				type = 'password'
# 			),
# 			rx.input(
# 				placeholder = 'Teléfono',
# 				name = 'phone'
# 			),
# 			rx.dialog.close(
# 				rx.button('Guardar', type='submit')
# 			),
# 		),
# 		on_submit=UserState.create_user,
# 	)

# def delete_user_dialogo_component(username: str) -> rx.Component:
# 	return rx.dialog.root(
# 		rx.dialog.trigger(
# 			rx.button(
# 				rx.icon('trash-2')
# 			)
# 		),
# 		rx.dialog.content(
# 			rx.dialog.title('Eliminar usuario'),
# 			rx.dialog.description('Está seguro de quere eliminar el usuario ', username),
# 			rx.flex(
# 				rx.dialog.close(
# 					rx.button(
# 						'Cancelar',
# 						color_scheme = 'gray',
# 						variant = 'soft'
# 					),
# 				),
# 				rx.dialog.close(
# 					rx.button('Confirmar', on_click=UserState.delete_user_by_email(username)),
# 				),
# 				spacing = '3',
# 				margin_top = '16px',
# 				justify = 'end',
# 			)
# 		)
# 	)


app = rx.App()
app.add_page(stocks_page)

