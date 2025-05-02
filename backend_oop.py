# backendcafe.py

import json
import os

class JSONStorage:
    @staticmethod
    def cargar(filename, default=[]):
        if not os.path.exists(filename):
            return default
        with open(filename, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return default

    @staticmethod
    def guardar(filename, data):
        try:
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error al guardar en {filename}: {e}")
            return False


class UsuarioManager:
    FILE = "usuarios.json"

    def guardar_usuario(self, nombre, email, contrasena, edad):
        usuarios = JSONStorage.cargar(self.FILE)
        usuarios.append({
            "nombre": nombre,
            "email": email,
            "contrasena": contrasena,
            "edad": edad
        })
        JSONStorage.guardar(self.FILE, usuarios)


class EmpleadoManager:
    FILE = "empleados.json"

    def guardar_empleado(self, nombre, email, contrasena, rol):
        empleados = JSONStorage.cargar(self.FILE)
        empleados.append({
            "nombre": nombre,
            "email": email,
            "contrasena": contrasena,
            "rol": rol
        })
        JSONStorage.guardar(self.FILE, empleados)


class AuthManager:
    def validar_login(self, email, contrasena):
        empleados = JSONStorage.cargar("empleados.json")
        for emp in empleados:
            if emp["email"] == email and emp["contrasena"] == contrasena:
                return emp["rol"], emp["nombre"]

        usuarios = JSONStorage.cargar("usuarios.json")
        for user in usuarios:
            if user["email"] == email and user["contrasena"] == contrasena:
                return "cliente", user["nombre"]

        return None, None


class InventarioManager:
    FILE = "inventario.json"

    def cargar(self):
        return JSONStorage.cargar(self.FILE)

    def guardar(self, inventario):
        JSONStorage.guardar(self.FILE, inventario)

    def agregar_ingrediente(self, nombre, cantidad):
        inventario = self.cargar()
        cantidad = int(cantidad)
        for item in inventario:
            if item["ingrediente"] == nombre:
                item["cantidad"] += cantidad
                break
        else:
            inventario.append({"ingrediente": nombre, "cantidad": cantidad})
        self.guardar(inventario)

    def eliminar_ingrediente(self, nombre):
        inventario = self.cargar()
        inventario = [item for item in inventario if item["ingrediente"] != nombre]
        self.guardar(inventario)

    def editar_ingrediente(self, nombre, nueva_cantidad):
        inventario = self.cargar()
        for item in inventario:
            if item["ingrediente"].lower() == nombre.lower():
                try:
                    item["cantidad"] = float(nueva_cantidad)
                    self.guardar(inventario)
                    return True
                except ValueError:
                    raise ValueError("Cantidad inválida")
        raise ValueError("Ingrediente no encontrado")



class BebidaManager:
    FILE = "bebidas.json"

    def cargar_bebidas(self):
        return JSONStorage.cargar(self.FILE, default=[])

    def agregar_bebida(self, nombre, categoria, ingredientes, cantidades):
        bebidas = self.cargar_bebidas()
        for bebida in bebidas:
            if bebida["nombre"].lower() == nombre.lower():
                return "Error: La bebida ya está registrada"
        nueva = {
            "nombre": nombre,
            "categoria": categoria,
            "ingredientes": ingredientes,
            "cantidades": cantidades
        }
        bebidas.append(nueva)
        JSONStorage.guardar(self.FILE, bebidas)
        return "Producto registrado exitosamente"


class PuntosManager:
    FILE = "puntos.json"

    def cargar_puntos(self):
        return JSONStorage.cargar(self.FILE, default={})

    def guardar_puntos(self, puntos_data):
        JSONStorage.guardar(self.FILE, puntos_data)


class PedidoManager:
    FILE = "historial_pedidos.json"

    def cargar_historial(self):
        return JSONStorage.cargar(self.FILE)

    def guardar_pedido(self, pedido):
        historial = self.cargar_historial()
        historial.append(pedido)
        JSONStorage.guardar(self.FILE, historial)

    def actualizar_inventario(self, nombre_producto, cantidad_usada):
        bebidas = BebidaManager().cargar_bebidas()
        inventario = InventarioManager().cargar()

        producto = next((b for b in bebidas if b["nombre"] == nombre_producto), None)
        if not producto:
            return False

        for ingrediente, cantidad_str in zip(producto["ingredientes"], producto["cantidades"]):
            cantidad_num = float(''.join(filter(str.isdigit, cantidad_str)))
            cantidad_total = cantidad_num * cantidad_usada
            for item in inventario:
                if item["ingrediente"] == ingrediente:
                    item["cantidad"] = max(0, item["cantidad"] - cantidad_total)
                    break

        InventarioManager().guardar(inventario)
        return True
    
class PromocionManager:
    FILE = "promociones.json"

    def cargar_promociones(self):
        return JSONStorage.cargar(self.FILE, default=[])

    def guardar_promociones(self, promociones):
        JSONStorage.guardar(self.FILE, promociones)

    def agregar_promocion(self, nombre, categoria, costo_puntos):
        promociones = self.cargar_promociones()
        promociones.append({
            "nombre": nombre,
            "categoria": categoria,
            "costo_puntos": costo_puntos
        })
        self.guardar_promociones(promociones)

    def eliminar_promocion(self, nombre):
        promociones = self.cargar_promociones()
        promociones = [p for p in promociones if p["nombre"] != nombre]
        self.guardar_promociones(promociones)

