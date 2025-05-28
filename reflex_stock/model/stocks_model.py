import reflex as rx
from typing import Optional
from sqlmodel import Field

class Producto(rx.Model, table=True):
	id: Optional[int] = Field(default=None, primary_key=True)
	producto: str
	id_clase: int
	id_subclase: int

class Stock(rx.Model, table=True):
	id: Optional[int] = Field(default=None, primary_key=True)
	cantidad: int
	id_producto: int
	mes: int
	anio: int

class StockLapso(rx.Model, table=True):
	id: Optional[int] = Field(default=None, primary_key=True)
	cantidad: int
	id_producto: int
	mmanio: str
	lapso: int

# class Clase(rx.Model, table=True):
# 	id: Optional[int] = Field(default=None, primary_key=True)
# 	clase: str

# class SubClase(rx.Model, table=True):
# 	id: Optional[int] = Field(default=None, primary_key=True)
# 	subclase: int
# 	id_clase: int
