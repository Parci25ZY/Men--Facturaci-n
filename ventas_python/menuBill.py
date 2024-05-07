from components import Menu, Valida
from utilities import borrarPantalla, gotoxy
from utilities import reset_color, red_color, green_color, yellow_color, blue_color, purple_color, cyan_color
from clsJson import JsonFile
from company import Company
from customer import RegularClient
from customer import VipClient
from sales import Sale
from product import Product
from iCrud import ICrud
import datetime
import time
import os
from tabulate import tabulate
from functools import reduce
import math

def verificar_cedula(cedula=""):
    if len(cedula) != 10:
        raise ValueError("Longitud de cédula incorrecta (debe ser exactamente 10 caracteres)")
    
    multiplicadores = [2, 1, 2, 1, 2, 1, 2, 1, 2]
    ced_array = [int(d) for d in cedula[:9]]
    ultimo_digito = int(cedula[9])
    
    resultado = [(i * j) if (i * j) < 10 else (i * j) - 9 for i, j in zip(ced_array, multiplicadores)]
    suma_resultado = sum(resultado)
    verificacion = math.ceil(float(suma_resultado) / 10) * 10 - suma_resultado
    
    return ultimo_digito == verificacion


def draw_frame(character):
    print(character * 90)
    for _ in range(24):
        print(character + " " * 88 + character)
    print(character * 90)

def get_frame_character():
    frame_char = input(blue_color + "¿Cómo deseas tu marco? Ingrese Caracter: ")
    return frame_char[0] if frame_char else "*"

def draw_custom_frame():
    # Limpiar pantalla y dibujar marco especial en las esquinas superior e inferior
    borrarPantalla()
    print(blue_color + "▅" + "▅" * 88 + "▅")
    for _ in range(22):
        print("▅" + " " * 88 + "▅")
    print("▅" + "▅" * 88 + "▅" + reset_color)

path, _ = os.path.split(os.path.abspath(__file__))

borrarPantalla()
frame_character = get_frame_character()

class CrudClients(ICrud):
    def create(self):
        # Lógica para ingresar un nuevo cliente
        draw_custom_frame()
        # Mensaje de encabezado centrado
        header_text = "𝙍𝙚𝙜𝙞𝙨𝙩𝙧𝙤 𝙙𝙚𝙡 𝙘𝙡𝙞𝙚𝙣𝙩𝙚"
        header_length = len(header_text)
        header_spaces = (90 - header_length) // 2
        gotoxy(header_spaces, 3)
        print(blue_color + header_text)
        gotoxy(16, 4)
        print("𝗘𝗺𝗽𝗿𝗲𝘀𝗮: 𝗖𝗼𝗿𝗽𝗼𝗿𝗮𝗰𝗶ó𝗻 𝗲𝗹 𝗥𝗼𝘀𝗮𝗱𝗼 𝗿𝘂𝗰: 𝟬𝟴𝟳𝟲𝟱𝟰𝟯𝟮𝟵𝟰𝟬𝟬𝟭")
    
        while True:
            gotoxy(15, 7)
            nombre = input("➲ Nombre: ")
            gotoxy(15, 9)
            apellido = input("➲ Apellido: ")
    
            # Bucle para solicitar la cédula hasta que sea válida
            while True:
                gotoxy(15, 11)
                dni = input("➲ Cedula: ")
                try:
                    if len(dni) != 10 or not dni.isdigit():
                        raise ValueError("Longitud de cédula incorrecta o contiene caracteres no numéricos")
    
                    if verificar_cedula(dni):
                        # Cédula válida, verificar si ya está registrado
                        path, _ = os.path.split(os.path.abspath(__file__))
                        json_file = JsonFile(path + '/archivos/clients.json')
                        clients_data = json_file.read()
                        dni_existe = any(client["dni"] == dni for client in clients_data)
                        if dni_existe:
                            gotoxy(15, 13)
                            print(red_color + "Cliente ya registrado. Por favor, ingrese una cédula diferente." + reset_color)
                        else:
                            # Validar tipo de cliente (Regular o VIP)
                            gotoxy(15, 13)
                            card_input = input("➲ ¿Es un cliente VIP? (s/n): ")
                            card_type = True if card_input.lower() == "s" else False
                            if card_type:
                                new_client = VipClient(nombre, apellido, dni, card=True)
                            else:
                                new_client = RegularClient(nombre, apellido, dni, card=False)
    
                            # Guardar el cliente en el archivo JSON
                            new_client_dict = new_client.getJson()
                            clients_data.append(new_client_dict)
                            json_file.save(clients_data)
    
                            # Mensaje de confirmación dentro del marco
                            gotoxy(15, 15)
                            print(f'{new_client} Cedula: {dni}')
                            gotoxy(15, 17)
                            print(green_color + "¡Cliente creado Exitosamente!")
                            time.sleep(3)
                            return  # Salir de la función después de crear el cliente
                    else:
                        gotoxy(15, 13)
                        print(red_color + "Cédula inválida, por favor ingrese una cédula válida." + reset_color)
                except ValueError as e:
                    gotoxy(15, 13)
                    print(f"\u001b[31m❝{str(e)}❞.\u001b[0m")

    def update(self):
        draw_custom_frame()
        # Solicitar la cédula del cliente a actualizar
        gotoxy(15,4)
        print(blue_color + "𝗘𝗺𝗽𝗿𝗲𝘀𝗮: 𝗖𝗼𝗿𝗽𝗼𝗿𝗮𝗰𝗶ó𝗻 𝗲𝗹 𝗥𝗼𝘀𝗮𝗱𝗼 𝗿𝘂𝗰: 𝟬𝟴𝟳𝟲𝟱𝟰𝟯𝟮𝟵𝟰𝟬𝟬𝟭")
        gotoxy(15, 6)
        print(blue_color + '❝𝐀𝐜𝐭𝐮𝐚𝐥𝐢𝐳𝐚𝐜𝐢ó𝐧 𝐝𝐞𝐥 𝐂𝐥𝐢𝐞𝐧𝐭𝐞❞')
        gotoxy(15, 7)

        dni = input("➲ Ingrese la cédula del cliente a actualizar: ")

        # Verificar si el cliente existe en el sistema
        json_file = JsonFile(path + '/archivos/clients.json')
        clients_data = json_file.read()

        client_data = json_file.find("dni", dni)

        if not client_data:
            gotoxy(15, 9)
            print(red_color + "𝐄𝐥 𝐜𝐥𝐢𝐞𝐧𝐭𝐞 𝐜𝐨𝐧 𝐥𝐚 𝐜é𝐝𝐮𝐥𝐚 𝐞𝐬𝐩𝐞𝐜𝐢𝐟𝐢𝐜𝐚𝐝𝐚 𝐧𝐨 𝐞𝐱𝐢𝐬𝐭𝐞." + reset_color)
            time.sleep(3)
            return
        # Crear una instancia de RegularClient con los datos del cliente encontrado
        client_info = client_data[0]
        first_name = client_info.get("nombre", "")
        last_name = client_info.get("apellido", "")
        dni = client_info.get("dni", "")
        card = client_info.get("card", False)  # Establecer el valor por defecto como False si no está presente

        client = RegularClient(first_name=first_name, last_name=last_name, dni=dni, card=card)

        # Mostrar la información actual del cliente
        gotoxy(15, 9)
        print(blue_color + "Información actual del cliente:")
        gotoxy(15, 10)
        print(f"Nombre: {client.first_name}")
        gotoxy(15, 11)
        print(f"Apellido: {client.last_name}")
        gotoxy(15, 12)
        print(f"Cédula: {client.dni}")
        gotoxy(15, 13)
        print(f"Tipo de cliente: {'VIP' if client.card else 'Regular'}")
        gotoxy(15, 14)
        # Solicitar y procesar la actualización de datos
        new_name = input(blue_color + "➲ Nuevo nombre (deje vacío para mantener el actual): " + reset_color).strip()
        gotoxy(15, 15)
        new_last_name = input(blue_color + "➲ Nuevo apellido (deje vacío para mantener el actual): " + reset_color).strip()
        # Actualizar los campos del cliente si se proporcionan nuevos valores
        if new_name:
            client.first_name = new_name
            
        if new_last_name:
            client.last_name = new_last_name

        gotoxy(15, 16)
        # Preguntar al usuario si desea cambiar el tipo de cliente
        change_type_input = input(blue_color + "➲ ¿Deseas cambiarle el tipo de cliente? (s/n): " + reset_color)
        change_type = True if change_type_input.lower() == "s" else False

        # Actualizar el tipo de cliente y el valor si es necesario
        gotoxy(15, 17)
        if change_type:
            card_input = input(blue_color + "➲ ¿Es un cliente VIP? (s/n): " + reset_color)
            card_type = True if card_input.lower() == "s" else False
            client.card = card_type  # Actualizar el tipo de cliente

            # Actualizar el valor en función del tipo de cliente
            if client.card:  # Si el cliente es VIP
                client.value = 10000
            else:  # Si el cliente es Regular
                client.value = 0
        # Guardar los cambios en el archivo JSON
        updated_data = {"nombre": client.first_name, "apellido": client.last_name, "card": client.card, "valor": client.value}
        json_file.update("dni", dni, updated_data)

        # Obtener nuevamente los datos del cliente actualizados después de la modificación
        client_data = json_file.find("dni", dni)

        # Guardar los datos actualizados en el archivo JSON
        if client_data:
            gotoxy(15, 20)
            print(green_color + "¡Cliente actualizado exitosamente!" + reset_color)
        else:
            gotoxy(15, 20)
            print(red_color + "Error al guardar los datos actualizados del cliente." + reset_color)

        time.sleep(3)
    
    def delete(self):
        draw_custom_frame()
        # Solicitar la cédula del cliente a eliminar
        gotoxy(15, 4)
        print(blue_color + '𝐄𝐥𝐢𝐦𝐢𝐧𝐚𝐜𝐢ó𝐧 𝐝𝐞 𝐂𝐥𝐢𝐞𝐧𝐭𝐞')
        gotoxy(15, 6)
        dni = input("➲ Ingrese la cédula del cliente a eliminar: ")

        # Verificar si el cliente existe en el sistema
        json_file = JsonFile(path + '/archivos/clients.json')
        client_data = json_file.find("dni", dni)

        if not client_data:
            gotoxy(15, 9)
            print("El cliente con la cédula especificada no existe.")
            time.sleep(3)
            return

        # Mostrar la información del cliente a eliminar
        client_info = client_data[0]
        first_name = client_info.get("nombre", "")
        last_name = client_info.get("apellido", "")
        dni = client_info.get("dni", "")
        card = client_info.get("card", False)  # Establecer el valor por defecto como False si no está presente

        client = RegularClient(first_name=first_name, last_name=last_name, dni=dni, card=card)

        # Mostrar la información del cliente antes de confirmar la eliminación
        gotoxy(15, 4)
        print('𝐄𝐥𝐢𝐦𝐢𝐧𝐚𝐜𝐢ó𝐧 𝐝𝐞 𝐂𝐥𝐢𝐞𝐧𝐭𝐞')
        gotoxy(15, 8)
        print(f"Información del cliente:")
        gotoxy(15, 9)
        print(f"Nombre: {client.fullName()}")
        gotoxy(15, 10)
        print(f"Cédula: {client.dni}")
        gotoxy(15, 11)
        print(f"Tipo de cliente: {'VIP' if client.card else 'Regular'}")

        # Confirmar la eliminación del cliente
        gotoxy(15, 12)
        confirm_delete = input(f"¿Estás seguro de eliminar al cliente {client.fullName()}? (s/n): ")

        if confirm_delete.lower() == "s":
            # Eliminar al cliente del archivo JSON
            json_file.delete("dni", dni)
            gotoxy(15, 14)
            print(green_color + f"¡Cliente {client.fullName()} eliminado exitosamente!")
        else:
            gotoxy(15, 14)
            print(red_color + "Operación de eliminación cancelada.")

        time.sleep(3)

    def consult(self):
        draw_custom_frame()
        # Obtener todos los clientes del archivo JSON
        json_file = JsonFile(path + '/archivos/clients.json')
        clients_data = json_file.read()

        # Verificar si hay clientes registrados
        if not clients_data:
            gotoxy(15, 4)
            print(red_color + "No hay clientes registrados." + reset_color)
            time.sleep(3)
            return

        # Mostrar la lista de clientes
        gotoxy(15, 4)
        print(blue_color + "𝐂𝐨𝐧𝐬𝐮𝐥𝐭𝐚 𝐝𝐞 𝐂𝐥𝐢𝐞𝐧𝐭𝐞𝐬 𝐲 𝐂𝐚𝐭𝐞𝐠𝐨𝐫𝐢𝐚𝐬:")
        row = 6
        for client_info in clients_data:
            gotoxy(15, row)
            print(f"Nombre: {client_info['nombre']}")
            gotoxy(15, row + 1)
            print(f"Apellido: {client_info['apellido']}")
            gotoxy(15, row + 2)
            print(f"Cédula: {client_info['dni']}")
            gotoxy(15, row + 3)
            card_type = "VIP" if client_info['card'] else "Regular"
            print(f"Tipo de cliente: {card_type}")
            row += 5  # Incrementar la fila para el siguiente cliente
        time.sleep(5) 
###################################################################################################

class CrudProducts(ICrud):
    def create(self):
        draw_custom_frame()
        gotoxy(30, 3)
        print(blue_color + "𝙍𝙚𝙜𝙞𝙨𝙩𝙧𝙤 𝙙𝙚 𝙋𝙧𝙤𝙙𝙪𝙘𝙩𝙤𝙨" + reset_color)
    
        def print_error_message(message):
            # Función para imprimir un mensaje de error con el formato deseado
            gotoxy(15, 16)
            print(red_color + message + reset_color)
    
        def clear_error_message():
            # Función para limpiar el mensaje de error en la pantalla
            gotoxy(15, 16)
            print(" " * 50)  # Borra la línea de mensaje de error
    
        # Leer datos actuales del archivo JSON
        path, _ = os.path.split(os.path.abspath(__file__))
        json_file = JsonFile(path + '/archivos/products.json')
        productos = json_file.read()
    
        # Validación del ID del producto
        while True:
            gotoxy(15, 6)
            id_producto = input(blue_color + "➲ ID del producto: ")
            if not id_producto.isdigit() or int(id_producto) <= 0:
                print_error_message("El ID debe ser un número entero positivo.")
                time.sleep(2)  # Tiempo para visualizar el mensaje de error
                clear_error_message()  # Limpiar el mensaje de error
                continue
            
            id_producto = int(id_producto)
    
            # Verificar si el ID ya existe en la lista de productos
            id_existente = any(producto["id"] == id_producto for producto in productos)
            if id_existente:
                print_error_message("Este producto ya se encuentra registrado.")
                time.sleep(2)  # Tiempo para visualizar el mensaje de error
                clear_error_message()  # Limpiar el mensaje de error
                continue
            
            # Si pasa todas las validaciones, romper el bucle
            break
        
        # Validación de la descripción del producto
        while True:
            gotoxy(15, 8)
            descripcion = input("➲ Descripción del producto: ")
            if not descripcion.strip():
                print_error_message("La descripción no puede estar vacía.")
                time.sleep(2)  # Tiempo para visualizar el mensaje de error
                clear_error_message()  # Limpiar el mensaje de error
            else:
                break
            
        # Validación del precio del producto
        while True:
            gotoxy(15, 10)
            precio = input(blue_color + "➲ Precio del producto: ")
            if not precio.replace('.', '', 1).isdigit() or float(precio) <= 0:
                print_error_message("El precio debe ser un número positivo.")
                time.sleep(2)  # Tiempo para visualizar el mensaje de error
                clear_error_message()  # Limpiar el mensaje de error
            else:
                precio = float(precio)
                break
            
        # Validación del stock del producto
        while True:
            gotoxy(15, 12)
            stock = input(blue_color + "➲ Cantidad en stock: ")
            if not stock.isdigit() or int(stock) < 0:
                print_error_message("La cantidad en stock debe ser un número positivo.")
                time.sleep(2)  # Tiempo para visualizar el mensaje de error
                clear_error_message()  # Limpiar el mensaje de error
            else:
                stock = int(stock)
                break
            
        gotoxy(15, 14)
        confirmar = input(blue_color + "¿Está seguro de guardar este producto? (s/n): ")
    
        if confirmar.lower() == "s":
            nuevo_producto = {
                "id": id_producto,
                "descripcion": descripcion,
                "precio": precio,
                "stock": stock
            }
            # Agregar el nuevo producto a la lista de productos
            productos.append(nuevo_producto)
            json_file.save(productos)

            gotoxy(15, 16)
            print(green_color + "Producto Guardado en Bodega" + reset_color)
        else:
            gotoxy(15, 16)
            print(red_color + "Producto Cancelado" + reset_color)

        print(blue_color)
        time.sleep(4)
    
    def update(self):
        draw_custom_frame()
        gotoxy(30, 3)
        print(blue_color + "𝐀𝐜𝐭𝐮𝐚𝐥𝐢𝐳𝐚𝐜𝐢ó𝐧 𝐝𝐞 𝐏𝐫𝐨𝐝𝐮𝐜𝐭𝐨𝐬 𝐞𝐧 𝐁𝐨𝐝𝐞𝐠𝐚" + reset_color)

        while True:
            # Solicitar el ID del producto a actualizar
            gotoxy(15, 6)
            id_producto = input(blue_color + "➲ Ingrese el ID del producto a buscar: ")

            # Leer datos del archivo JSON de productos
            path, _ = os.path.split(os.path.abspath(__file__))
            json_file = JsonFile(path + '/archivos/products.json')
            productos = json_file.read()

            # Buscar el producto por ID
            product_found = None
            for producto in productos:
                if str(producto["id"]) == id_producto:
                    product_found = producto
                    break

            if product_found:
                # Mostrar información del producto encontrado
                gotoxy(15, 8)
                print(blue_color + "Información del Producto:" + reset_color)
                gotoxy(15, 9)
                print(blue_color + f"ID: {product_found['id']}")
                gotoxy(15, 10)
                print(blue_color + f"Descripción: {product_found['descripcion']}")
                gotoxy(15, 11)
                print(blue_color + f"Precio: {product_found['precio']}")
                gotoxy(15, 12)
                print(blue_color + f"Stock: {product_found['stock']}")

                gotoxy(15, 7)  # Posición del mensaje de error
                print(" " * 70) 

                # Pedir al usuario que ingrese nuevos datos para actualizar el producto
                gotoxy(15, 14)
                new_id = input(blue_color + "ID Nuevo (deje vacío para mantener el actual): ")
                gotoxy(15, 15)
                new_desc = input(blue_color + "Descripción Nueva (deje vacío para mantener la actual): ")
                gotoxy(15, 16)
                new_price = input(blue_color + "Precio Nuevo (deje vacío para mantener el actual): ")
                gotoxy(15, 17)
                new_stock = input(blue_color + "Stock Nuevo (deje vacío para mantener el actual): ")

                # Actualizar los datos del producto si se ingresaron nuevos valores
                if new_id:
                    product_found['id'] = new_id
                if new_desc:
                    product_found['descripcion'] = new_desc
                if new_price:
                    product_found['precio'] = new_price
                if new_stock:
                    product_found['stock'] = new_stock

                # Preguntar al usuario si desea guardar los cambios
                gotoxy(15, 18)
                save_changes = input("¿Deseas guardar los cambios del producto? (s/n): ")
                if save_changes.lower() == 's':
                    json_file.save(productos)
                    gotoxy(15, 19)
                    print(green_color + "¡Cambios guardados correctamente!")
                else:
                    gotoxy(15, 19)
                    print(red_color + "Cambios no guardados.")

                # Esperar antes de regresar al menú
                gotoxy(15, 20)
                print(blue_color + 'Regresando al Menú Producto')
                time.sleep(4)
                return  # Regresar al menú producto

            else:
                # Mostrar mensaje si el producto no se encuentra
                gotoxy(15, 7)
                print(red_color + "El producto con el ID especificado no existe. Intente nuevamente." + reset_color)
                time.sleep(2)  # Esperar antes de volver a pedir el ID

    def delete(self):
        draw_custom_frame()
        gotoxy(30, 3)
        print(blue_color + "𝐄𝐥𝐢𝐦𝐢𝐧𝐚𝐜𝐢ó𝐧 𝐝𝐞 𝐏𝐫𝐨𝐝𝐮𝐜𝐭𝐨𝐬 𝐞𝐧 𝐁𝐨𝐝𝐞𝐠𝐚" + reset_color)

        while True:
            # Solicitar el ID del producto a eliminar
            gotoxy(15, 6)
            id_producto = input(blue_color + "➲ Ingrese el ID del producto a eliminar: ")

            # Leer datos del archivo JSON de productos
            path, _ = os.path.split(os.path.abspath(__file__))
            json_file = JsonFile(path + '/archivos/products.json')
            productos = json_file.read()

            # Buscar el producto por ID
            product_found = None
            for producto in productos:
                if str(producto["id"]) == id_producto:
                    product_found = producto
                    break

            if product_found:
                # Mostrar información del producto encontrado
                gotoxy(15, 8)
                print(blue_color + "Información del Producto a Eliminar:")
                gotoxy(15, 9)
                print(f"ID: {product_found['id']}")
                gotoxy(15, 10)
                print(f"Descripción: {product_found['descripcion']}")
                gotoxy(15, 11)
                print(f"Precio: {product_found['precio']}")
                gotoxy(15, 12)
                print(f"Stock: {product_found['stock']}")

                gotoxy(15, 7)  # Posición del mensaje de error
                print(" " * 70)
                # Confirmar la eliminación del producto
                gotoxy(15, 14)
                confirm_delete = input(blue_color + "¿Estás seguro de eliminar este producto? (s/n): ")

                if confirm_delete.lower() == "s":
                    # Eliminar el producto de la lista de productos
                    productos.remove(product_found)
                    json_file.save(productos)
                    gotoxy(15, 16)
                    print(green_color + "¡Producto eliminado correctamente!" + reset_color)
                else:
                    gotoxy(15, 16)
                    print(red_color + "Operación de eliminación cancelada." + reset_color)

                # Regresar al menú producto
                gotoxy(15, 17)
                print(blue_color + "Regresando al Menú Producto")
                time.sleep(3)
                break  # Salir del bucle

            else:
                # Mostrar mensaje si el producto no se encuentra
                gotoxy(15, 7)
                print(red_color + "El producto con el ID especificado no existe. Intente nuevamente." + reset_color)
                time.sleep(2)  # Esperar antes de volver a pedir el ID
    
    def consult(self):
        draw_custom_frame()
        # Obtener todos los productos del archivo JSON
        json_file = JsonFile(path + '/archivos/products.json')
        products_data = json_file.read()

        # Verificar si hay productos registrados
        if not products_data:
            gotoxy(15, 4)
            print(red_color + "No hay productos registrados." + reset_color)
            time.sleep(3)
            return
    
        # Mostrar el encabezado "Consulta de Productos y Precios"
        gotoxy(15, 4)
        print(blue_color + "Consulta de Productos y Precios:")

        # Preparar los datos para tabulate
        table_data = []
        for product in products_data:
            table_data.append([
                product.get('id', ''),
                product.get('descripcion', ''),
                product.get('precio', ''),
                product.get('stock', '')
            ])

        # Definir encabezados de la tabla
        headers = ["ID", "Descripción", "Precio", "Stock"]

        # Generar la tabla en formato tabulate
        table = tabulate(table_data, headers=headers, tablefmt="heavy_grid", numalign="center", stralign="center")

        # Establecer la posición y para imprimir la tabla
        start_row = 6  # Establece la fila inicial
        gotoxy(15, start_row)  # Ajusta la posición de la primera línea de la tabla

        # Imprimir la tabla línea por línea con la posición correcta
        table_lines = table.split('\n')
        for line in table_lines:
            gotoxy(15, start_row)
            print(line)
            start_row += 1

        gotoxy(15, 21)
        time.sleep(6)
        print(blue_color + "Regresando al Menu Productos...")
####################################################################################################

class CrudSales(ICrud):
    def create(self):
        # cabecera de la venta
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2);print(blue_color+"Registro de Venta" + reset_color)
        gotoxy(17,3);print(blue_color+Company.get_business_name())
        gotoxy(5,4);print(f"Factura#:F0999999 {' '*3} Fecha:{datetime.datetime.now()}")
        gotoxy(66,4);print("Subtotal:")
        gotoxy(66,5);print("Decuento:")
        gotoxy(66,6);print("Iva     :")
        gotoxy(66,7);print("Total   :")
        gotoxy(15,6);print("Cedula:")
        dni=validar.solo_numeros("Error: Solo numeros",23,6)
        json_file = JsonFile(path+'/archivos/clients.json')
        client = json_file.find("dni",dni)
        if not client:
            gotoxy(35,6);print("Cliente no existe")
            return
        client = client[0]
        cli = RegularClient(client["nombre"],client["apellido"], client["dni"], card=True) 
        sale = Sale(cli)
        gotoxy(35,6);print(cli.fullName())
        gotoxy(2,8);print(green_color+"*"*90+reset_color) 
        gotoxy(5,9);print(purple_color+"Linea") 
        gotoxy(12,9);print("Id_Articulo") 
        gotoxy(24,9);print("Descripcion") 
        gotoxy(38,9);print("Precio") 
        gotoxy(48,9);print("Cantidad") 
        gotoxy(58,9);print("Subtotal") 
        gotoxy(70,9);print("Deseas ingresar productos (s/n)"+reset_color)
        # detalle de la venta
        follow ="s"
        line=1
        while follow.lower()=="s":
            gotoxy(7,9+line);print(line)
            gotoxy(15,9+line);
            id=int(validar.solo_numeros("Error: Solo numeros",15,9+line))
            json_file = JsonFile(path+'/archivos/products.json')
            prods = json_file.find("id",id)
            if not prods:
                gotoxy(24,9+line);print("Producto no existe")
                time.sleep(1)
                gotoxy(24,9+line);print(" "*20)
            else:    
                prods = prods[0]
                product = Product(prods["id"],prods["descripcion"],prods["precio"],prods["stock"])
                gotoxy(24,9+line);print(product.descrip)
                gotoxy(38,9+line);print(product.preci)
                gotoxy(49,9+line);qyt=int(validar.solo_numeros("Error:Solo numeros",49,9+line))
                gotoxy(59,9+line);print(product.preci*qyt)
                sale.add_detail(product,qyt)
                gotoxy(76,4);print(round(sale.subtotal,2))
                gotoxy(76,5);print(round(sale.discount,2))
                gotoxy(76,6);print(round(sale.iva,2))
                gotoxy(76,7);print(round(sale.total,2))
                gotoxy(74,9+line);follow=input() or "s"  
                gotoxy(76,9+line);print(green_color+"✔"+reset_color)  
                line += 1
        gotoxy(15,9+line);print(red_color+"Esta seguro de grabar la venta(s/n):")
        gotoxy(54,9+line);procesar = input().lower()
        if procesar == "s":
            gotoxy(15,10+line);print("😊 Venta Grabada satisfactoriamente 😊"+reset_color)
            # print(sale.getJson())  
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.read()
            ult_invoices = invoices[-1]["factura"]+1
            data = sale.getJson()
            data["factura"]=ult_invoices
            invoices.append(data)
            json_file = JsonFile(path+'/archivos/invoices.json')
            json_file.save(invoices)
        else:
            gotoxy(20,10+line);print("🤣 Venta Cancelada 🤣"+reset_color)    
        time.sleep(2)    

    def update(self):
        draw_custom_frame()
        gotoxy(30, 3)
        print(blue_color + '𝐌𝐨𝐝𝐢𝐟𝐢𝐜𝐚𝐜𝐢𝐨́𝐧 𝐝𝐞 𝐕𝐞𝐧𝐭𝐚' + reset_color)

        while True:
            # Solicitar número de factura a modificar
            gotoxy(15, 5)
            invoice_input = input(blue_color + "Ingrese el número de factura a modificar: " + reset_color)

            if invoice_input.isdigit():
                invoice_number = int(invoice_input)
                json_file = JsonFile(path+'/archivos/invoices.json')
                invoices = json_file.read()

                # Buscar factura con el número ingresado
                found_invoice = None
                for invoice in invoices:
                    if invoice["factura"] == invoice_number:
                        found_invoice = invoice
                        break
                
                # Mostrar detalles de la factura
                detalles_factura = {k: v for k, v in found_invoice.items() if k != 'detalle'}
                detalle_venta = found_invoice["detalle"]

                gotoxy(9, 7)
                print(blue_color+ f"Impresión de la Factura # {invoice_number}" )
                print(tabulate([detalles_factura], headers="keys", tablefmt="heavy_grid", numalign="center"))

                # Mostrar detalle de la venta
                if detalle_venta:
                    gotoxy(9, 14)
                    print(blue_color+ "Detalle de la Venta:")
                    headers = detalle_venta[0].keys()
                    data = [[detalle[key] for key in headers] for detalle in detalle_venta]
                    print(tabulate(data, headers=headers, tablefmt="heavy_grid", numalign="center"))

                    # Confirmar modificación
                    gotoxy(40, 14)
                    modify_confirm = input(blue_color + "¿Desea modificar esta factura? (s/n): " + reset_color)
                    if modify_confirm.lower() == 's':
                        gotoxy(40, 15)
                        product_to_modify = input(blue_color + "Ingrese el producto para cambiar la cantidad: "+ reset_color)
                        gotoxy(40, 16)
                        new_quantity = int(input(blue_color + "Ingrese la nueva cantidad para este producto: "+ reset_color))

                        # Buscar el producto en los detalles de la factura y actualizar la cantidad
                        for detalle in detalle_venta:
                            if detalle["poducto"] == product_to_modify:
                                detalle["cantidad"] = new_quantity
                                break

                        # Recalcular subtotal y total
                        subtotal = sum(detalle["precio"] * detalle["cantidad"] for detalle in detalle_venta)
                        found_invoice["subtotal"] = subtotal
                        found_invoice["total"] = subtotal - found_invoice["descuento"] + found_invoice["iva"]

                        # Guardar cambios en el archivo JSON
                        json_file.save(invoices)
                        gotoxy(40, 17)
                        print(green_color + "¡Cantidad de producto modificada exitosamente!" + reset_color)
                        gotoxy(40, 18)
                        x =input(blue_color + "presione una tecla para continuar...") 
                        return  
                    elif modify_confirm.lower() == 'n':
                        gotoxy(9, 19)
                        print(red_color + "Modificación cancelada." + reset_color)
                        gotoxy(9, 20)
                        x =input(blue_color + "presione una tecla para continuar...")      

                    else:
                        print(red_color + "Opción inválida. Por favor, ingrese 's' para modificar o 'n' para cancelar." + reset_color)
                        continue
                else:
                    gotoxy(15, 20)
                    print(red_color + "No hay detalles de venta para esta factura." + reset_color)
                    continue

    def delete(self):
        draw_custom_frame()
        gotoxy(30, 3)
        print(blue_color + '𝐄𝐥𝐢𝐦𝐢𝐧𝐚𝐜𝐢𝐨́𝐧 𝐝𝐞 𝐅𝐚𝐜𝐭𝐮𝐫𝐚' + reset_color)

        while True:
            # Solicitar número de factura a eliminar
            gotoxy(15, 5)
            invoice_input = input(blue_color + "Ingrese el número de factura a eliminar: " + reset_color)

            if invoice_input.isdigit():
                invoice_number = int(invoice_input)
                json_file = JsonFile(path + '/archivos/invoices.json')
                invoices = json_file.read()

                # Buscar factura con el número ingresado
                found_invoice = None
                for invoice in invoices:
                    if invoice["factura"] == invoice_number:
                        found_invoice = invoice
                        break

                if found_invoice:
                    # Mostrar detalles de la factura
                    detalles_factura = {k: v for k, v in found_invoice.items() if k != 'detalle'}
                    detalle_venta = found_invoice["detalle"]

                    gotoxy(9, 7)
                    print(blue_color + f"Impresión de la Factura # {invoice_number}")
                    print(tabulate([detalles_factura], headers="keys", tablefmt="heavy_grid", numalign="center"))

                    # Mostrar detalle de la venta si existe
                    if detalle_venta:
                        gotoxy(9, 14)
                        print(blue_color + "Detalle de la Venta:")
                        headers = detalle_venta[0].keys()
                        data = [[detalle[key] for key in headers] for detalle in detalle_venta]
                        print(tabulate(data, headers=headers, tablefmt="heavy_grid", numalign="center"))

                    # Confirmar eliminación
                    gotoxy(40, 14)
                    delete_confirm = input(blue_color + "¿Desea eliminar esta factura? (s/n): " + reset_color)
                    if delete_confirm.lower() == 's':
                        # Eliminar factura de la lista
                        invoices.remove(found_invoice)
                        json_file.save(invoices)
                        gotoxy(40, 20)
                        print(green_color + "¡Factura eliminada exitosamente!" + reset_color)
                        gotoxy(40, 22)
                        x = input(blue_color + "Presione una tecla para continuar..." + reset_color)
                        return
                    elif delete_confirm.lower() == 'n':
                        gotoxy(9, 20)
                        print(red_color + "Eliminación cancelada." + reset_color)
                        gotoxy(9, 22)
                        x = input(blue_color + "Presione una tecla para continuar..." + reset_color)
                        return
                    else:
                        print(red_color + "Opción inválida. Por favor, ingrese 's' para eliminar o 'n' para cancelar." + reset_color)
                else:
                    gotoxy(15, 10)
                    print(red_color + "Factura no encontrada." + reset_color)
            else:
                gotoxy(15, 10)
                print(red_color + "Número de factura inválido. Por favor, ingrese un número válido." + reset_color)

    
    def consult(self):
        draw_custom_frame()
        gotoxy(36,3)
        print(blue_color + '𝐂𝐨𝐧𝐬𝐮𝐥𝐭𝐚 𝐝𝐞 𝐕𝐞𝐧𝐭𝐚')
        gotoxy(15,5);invoice= input(blue_color + "Ingrese Factura: ")
        if invoice.isdigit():
            invoice = int(invoice)
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.find("factura", invoice)
            
            if invoices:
                factura = invoices[0]
                detalles_factura = {k: v for k, v in factura.items() if k != 'detalle'}
                detalle_venta = factura["detalle"]
                gotoxy(9,7)
                print(f"Impresion de la Factura # {invoice}")
                print(tabulate([detalles_factura], headers="keys", tablefmt="heavy_grid", numalign="center"))
                # Mostrar el detalle de la venta
                gotoxy(9,14)
                print("Detalle de la Venta:")
                headers = detalle_venta[0].keys() if detalle_venta else []
                data = [[detalle[key] for key in headers] for detalle in detalle_venta]

                if data:
                    print(tabulate(data, headers=headers, tablefmt="heavy_grid", stralign="center", numalign="center"))

                else:
                    gotoxy(15, 8)
                    print(red_color + "No hay detalles de venta para esta factura." + reset_color)
            else:
                    gotoxy(15, 8)
                    print(red_color + "No se encontraron detalles para esta factura." + reset_color)
        else:    
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.read()
            print("Consulta de Facturas")
            for fac in invoices:
                print(f"{fac['factura']}   {fac['Fecha']}   {fac['cliente']}   {fac['total']}")
            
            suma = reduce(lambda total, invoice: round(total+ invoice["total"],2), 
            invoices,0)
            totales_map = list(map(lambda invoice: invoice["total"], invoices))
            total_client = list(filter(lambda invoice: invoice["cliente"] == "Dayanna Vera", invoices))
            max_invoice = max(totales_map)
            min_invoice = min(totales_map)
            tot_invoices = sum(totales_map)
            print("filter cliente: ",total_client)
            print(f"map Facturas:{totales_map}")
            print(f"              max Factura:{max_invoice}")
            print(f"              min Factura:{min_invoice}")
            print(f"              sum Factura:{tot_invoices}")
            print(f"              reduce Facturas:{suma}")
        gotoxy(43,23)
        x =input(blue_color + "Presione una tecla para continuar...")         

# Bucle principal dentro del marco
opc=''
crud_clients = CrudClients()
crud_products = CrudProducts()
while opc !='4':  
    # Limpiar la pantalla
    borrarPantalla()
    # Dibujar el marco
    draw_frame(frame_character)
    # Mostrar el menú principal
    menu_main = Menu("Menu Facturacion", ["1) Clientes","2) Productos","3) Ventas","4) Salir"], 20, 10)
    opc = menu_main.menu()

    if opc == "1":
        # Opciones del menú Clientes
        opc1 = ''
        while opc1 != '5':
            borrarPantalla()
            draw_frame(frame_character)
            menu_clients = Menu("Menu Clientes", ["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"], 20, 10)
            opc1 = menu_clients.menu()
            if opc1 == "1":
                crud_clients.create()
            elif opc1 == "2":
                crud_clients.update()
                pass
            elif opc1 == "3":
                crud_clients.delete()
                pass
            elif opc1 == "4":
                crud_clients.consult()

            gotoxy(15, 21)
            print(blue_color + "Regresando al menu Principal...")
            time.sleep(5)

    elif opc == "2":
        # Opciones del menú Productos
        opc2 = ''
        while opc2 != '5':
            borrarPantalla()
            draw_frame(frame_character)
            menu_products = Menu("Menu Productos", ["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"], 20, 10)
            opc2 = menu_products.menu()
            if opc2 == "1":
                crud_products.create()
            elif opc2 == "2":
                crud_products.update()
                pass
            elif opc2 == "3":
                crud_products.delete()
                pass
            elif opc2 == "4":
                crud_products.consult()

            gotoxy(15, 21)
            print(blue_color + "Regresando al menu Principal...")
            time.sleep(5)

    elif opc == "3":
        # Opciones del menú Ventas
        opc3 =''
        while opc3 != '5':
            borrarPantalla()
            draw_frame(frame_character)
            sales = CrudSales()
            menu_sales = Menu("Menu Ventas", ["1) Registro Venta","2) Consultar","3) Modificar","4) Eliminar","5) Salir"], 20, 10)
            opc3 = menu_sales.menu()
            if opc3 == "1":
                sales.create()
            elif opc3 == "2":
                sales.consult()
            elif opc3 == "3":
                sales.update()
            elif opc3 == "4":
                sales.delete()
            
            gotoxy(15, 21)
            print(blue_color + "Regresando al menu Principal...")
            time.sleep(5)

    elif opc == "4":
        # Salir del programa
        break

# Borrar la pantalla
borrarPantalla()
input("Presione una tecla para salir...")
borrarPantalla()

