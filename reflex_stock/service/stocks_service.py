from ..repository.stocks_repository import letras_select_all, productos_select_all, stocks_select_all, \
       producto_select_by_id, delete_stock, decrementar_stock, incrementar_stock, agregar_stock
from ..model.stocks_model import Producto

def letras_select_all_service():
    letras = letras_select_all()
    return letras

def productos_select_all_service(letra: str):
    productos = productos_select_all(letra)
    return productos

def producto_select_by_id_service(id_producto: int):
    producto = producto_select_by_id(id_producto)
    return producto

def stocks_select_all_service(id_producto: int):
    stocks = stocks_select_all(id_producto)
    return stocks

def delete_stock_service(id_stock: int, id_producto: int):
    return delete_stock(id_stock, id_producto)

def decrementar_stock_service(id_stock: int, id_producto: int):
    return decrementar_stock(id_stock, id_producto)

def incrementar_stock_service(id_stock: int, id_producto: int):
    return incrementar_stock(id_stock, id_producto)

def agregar_stock_service(id_producto: int, cantidad: int, mes: int, anio: int):
    return agregar_stock(id_producto, cantidad, mes, anio)

# def select_user_by_email_service(email: str):
#     if(len(email) != 0):
#         return select_user_by_email(email)
#     else:
#         return select_all()
    
# def create_user_service(username: str, password: str, phone: str, name: str):
#     user = select_user_by_email(username)
#     if(len(user) == 0):
#         user_save = User(username=username, password=password, phone=phone, name=name)
#         return create_user(user_save)
#     else:
#         raise BaseException('El usuario ya existe')
    
# def delete_user_service(username: str):
#     return delete_user(username)
