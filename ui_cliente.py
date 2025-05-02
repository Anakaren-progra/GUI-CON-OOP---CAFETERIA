# ui_cliente.py
import customtkinter as ctk
from tkinter import messagebox
import datetime
from backend_oop import BebidaManager, InventarioManager, PuntosManager, PedidoManager, PromocionManager


class ClienteUI:
    def __init__(self,ventana_inicio, nombre_cliente, email):
        self.ventana_inicio = ventana_inicio
        self.nombre_cliente = nombre_cliente
        self.email = email

        self.bebida_manager = BebidaManager()
        self.inventario_manager = InventarioManager()
        self.puntos_manager = PuntosManager()
        self.promocion_manager = PromocionManager()
        self.pedido_manager = PedidoManager()

        self.bebidas = self.bebida_manager.cargar_bebidas()
        self.puntos_data = self.puntos_manager.cargar_puntos()
        self.puntos_acumulados = self.puntos_data.get(self.email, 0)
        self.seleccion_bebidas = {}
        self.precio_extra = 10

        self.ventana = ctk.CTkToplevel()
        self.ventana.title("Entorno del Cliente")
        self.ventana.geometry("700x700")

        

        self.crear_interfaz()

    def mostrar(self):
        self.ventana.deiconify()

    def crear_interfaz(self):
        ctk.CTkLabel(self.ventana, text=f"Bienvenido, {self.nombre_cliente}.", font=("Arial", 16)).pack(pady=10)

        self.pestañas = ctk.CTkTabview(self.ventana)
        self.pestañas.pack(expand=True, fill="both")

        self.tab_productos = self.pestañas.add("Productos")
        self.tab_carrito = self.pestañas.add("Carrito")
        self.tab_puntos = self.pestañas.add("Puntos")

        self.crear_tab_productos()
        self.crear_tab_carrito()
        self.crear_tab_puntos()

        ctk.CTkButton(self.ventana, text="Cerrar Sesión", command=self.cerrar_sesion).pack(pady=10)

    def cerrar_sesion(self):
        self.ventana.destroy()
        self.ventana_inicio.deiconify()
    

    # -------------------------------------
    def crear_tab_productos(self):
        ctk.CTkLabel(self.tab_productos, text="Menú de Productos", font=("Arial", 18)).pack(pady=10)

        scroll = ctk.CTkScrollableFrame(self.tab_productos, width=650, height=420)
        scroll.pack(pady=5)

        categorias_ordenadas = [("Bebida caliente", "☕ Bebidas Calientes"), ("Bebida fria", "❄️ Bebidas Frías"), ("Postre", "🍰 Postres")]

        for categoria_key, categoria_titulo in categorias_ordenadas:
            ctk.CTkLabel(scroll, text=categoria_titulo, font=("Arial", 16)).pack(anchor="w", pady=(10, 4), padx=10)
            productos_categoria = [b for b in self.bebidas if b["categoria"] == categoria_key]

            contenedor = ctk.CTkFrame(scroll, fg_color="transparent")
            contenedor.pack(anchor="w", padx=10)

            for bebida in productos_categoria:
                card = ctk.CTkFrame(contenedor, width=300, height=100, corner_radius=10)
                card.pack_propagate(False)
                card.pack(side="left", padx=10, pady=5)

                icono = "☕" if bebida["categoria"] == "Bebida caliente" else "❄️" if bebida["categoria"] == "Bebida fria" else "🍰"
                ctk.CTkLabel(card, text=f"{icono} {bebida['nombre']}", font=("Arial", 14, "bold"), anchor="w").pack(anchor="w", padx=10, pady=(5, 0))

                precios = bebida.get("precios", {})
                if bebida["categoria"] == "Postre":
                    texto_precio = f"Precio: ${precios.get('precio', '?')}"
                else:
                    texto_precio = f"CH ${precios.get('chico', '?')} | MD ${precios.get('mediano', '?')} | GD ${precios.get('grande', '?')}"

                ctk.CTkLabel(card, text=texto_precio, font=("Arial", 12), anchor="w").pack(anchor="w", padx=10)
                ctk.CTkButton(card, text="Personalizar", width=120, command=lambda b=bebida: self.personalizar_bebida(b)).pack(pady=5)

    def personalizar_bebida(self, bebida, clave_original=None):
        ventana_personalizar = ctk.CTkToplevel()
        ventana_personalizar.title(f"Personalizar {bebida['nombre']}")
        ventana_personalizar.geometry("400x500")
        
        
        

        ctk.CTkLabel(ventana_personalizar, text=f"Personaliza tu {bebida['nombre']}").pack(pady=10)

        if bebida["categoria"] != "Postre":
            tamano_var = ctk.StringVar(value="mediano")
            extras_vars = {}

            ctk.CTkLabel(ventana_personalizar, text="Tamaño:").pack(pady=5)
            for t in ["chico", "mediano", "grande"]:
                ctk.CTkRadioButton(ventana_personalizar, text=t.capitalize(), variable=tamano_var, value=t).pack()

            opciones = ["Leche deslactosada", "Leche de avena", "Azucar extra", "Bombones", "Crema batida"]
            ctk.CTkLabel(ventana_personalizar, text="Extras:").pack(pady=5)
            for extra in opciones:
                var = ctk.BooleanVar()
                extras_vars[extra] = var
                ctk.CTkCheckBox(ventana_personalizar, text=extra, variable=var).pack()

            def guardar():
                clave = f"{bebida['nombre']}_{tamano_var.get()}_{'+'.join([k for k, v in extras_vars.items() if v.get()])}"
                ingredientes_extra = [k for k, v in extras_vars.items() if v.get()]
                inventario = self.inventario_manager.cargar()

                # Validar que hay suficiente inventario para cada extra
                ingredientes_faltantes = []
                for extra in ingredientes_extra:
                    encontrado = False
                    for item in inventario:
                        if item["ingrediente"].lower() == extra.lower():
                            if item["cantidad"] < 15:
                                ingredientes_faltantes.append(extra)
                            encontrado = True
                            break
                    if not encontrado:
                        ingredientes_faltantes.append(extra)  # No registrado

                if ingredientes_faltantes:
                    messagebox.showerror("Ingredientes insuficientes", f"No hay suficiente de: {', '.join(ingredientes_faltantes)}")
                    ventana_personalizar.destroy()
                    return

                # Descontar 15 unidades por cada extra
                for extra in ingredientes_extra:
                    for item in inventario:
                        if item["ingrediente"].lower() == extra.lower():
                            item["cantidad"] -= 15
                            break

                self.inventario_manager.guardar(inventario)
                
                
                
                
                self.seleccion_bebidas[clave] = {
                    "nombre": bebida["nombre"],
                    "tamano": tamano_var.get(),
                    "extras": [k for k, v in extras_vars.items() if v.get()]
                }
                if clave_original and clave_original in self.seleccion_bebidas:
                    del self.seleccion_bebidas[clave_original]
                self.actualizar_carrito()
                ventana_personalizar.destroy()

        else:
            cantidad_var = ctk.IntVar(value=1)
            ctk.CTkLabel(ventana_personalizar, text="Cantidad:").pack(pady=10)
            for i in range(1, 6):
                ctk.CTkRadioButton(ventana_personalizar, text=f"{i} pz", variable=cantidad_var, value=i).pack()

            def guardar():
                clave = f"{bebida['nombre']}_{cantidad_var.get()}_postre"

                # Eliminar la versión anterior si era edición
                if clave_original and clave_original in self.seleccion_bebidas:
                    del self.seleccion_bebidas[clave_original]
                
                self.seleccion_bebidas[clave] = {
                    "nombre": bebida["nombre"],
                    "cantidad": cantidad_var.get()
                }

                self.actualizar_carrito()
                ventana_personalizar.destroy()

        ctk.CTkButton(ventana_personalizar, text="Guardar", command=guardar).pack(pady=10)

    # -------------------------------------
    def crear_tab_carrito(self):
        ctk.CTkLabel(self.tab_carrito, text="Carrito de Compras", font=("Arial", 16)).pack(pady=10)

        self.carrito_frame = ctk.CTkScrollableFrame(self.tab_carrito, width=600, height=300)
        self.carrito_frame.pack(pady=5)
        self.total_compra = ctk.CTkLabel(self.tab_carrito, text="Total: $0", font=("Arial", 14, "bold"))
        self.total_compra.pack(pady=10)

        ctk.CTkButton(self.tab_carrito, text="Actualizar Carrito", command=self.actualizar_carrito).pack(pady=5)
        self.btn_confirmar_compra = ctk.CTkButton(
        self.tab_carrito,
        text="✅ Confirmar Compra",
        fg_color="#5cb85c",
        hover_color="#4cae4c",
        command=self.confirmar_compra
        )
        self.btn_confirmar_compra.pack(pady=10)

    def actualizar_carrito(self):
        for widget in self.carrito_frame.winfo_children():
            widget.destroy()

        total = 0

        for clave, datos in self.seleccion_bebidas.items():
            nombre = datos["nombre"]
            bebida = next((b for b in self.bebidas if b["nombre"] == nombre), None)
            if not bebida:
                continue

            if bebida["categoria"] == "Postre":
                cantidad = datos.get("cantidad", 1)
                precio = float(bebida.get("precios", {}).get("precio", 0)) * cantidad
                descripcion = f"{nombre} - {cantidad} unidad(es)"
            else:
                tamano = datos.get("tamano", "mediano")
                extras = datos.get("extras", [])
                precio = float(bebida.get("precios", {}).get(tamano, 0))
                precio += len(extras) * self.precio_extra
                descripcion = f"{nombre} ({tamano}) - Extras: {', '.join(extras) if extras else 'Ninguno'}"

            total += precio

            # Frame del producto
            frame = ctk.CTkFrame(self.carrito_frame)
            frame.pack(fill="x", padx=5, pady=5)

            ctk.CTkLabel(frame, text=descripcion, font=("Arial", 12)).grid(row=0, column=0, padx=10, sticky="w")
            ctk.CTkLabel(frame, text=f"${precio:.2f}", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=10)

            btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
            btn_frame.grid(row=0, column=2, padx=5)

            ctk.CTkButton(btn_frame, text="✏️ Editar", width=80, command=lambda k=clave: self.editar_producto_carrito(k)).pack(side="left", padx=2)
            ctk.CTkButton(btn_frame, text="🗑️ Eliminar", width=80, fg_color="#d9534f", hover_color="#a94442", command=lambda k=clave: self.eliminar_producto_carrito(k)).pack(side="left", padx=2)

        self.total_compra.configure(text=f"Total: ${total:.2f}")
        

    def confirmar_compra(self):
        self.btn_confirmar_compra.configure(state="disabled")  # 🔒 Evita doble clic

        try:
            if not self.seleccion_bebidas:
                messagebox.showwarning("Carrito vacío", "No hay productos en el carrito.")
                return

            inventario = self.inventario_manager.cargar()
            ingredientes_faltantes = []

            for clave, datos in self.seleccion_bebidas.items():
                if datos.get("promo"):
                    continue

                nombre_bebida = datos["nombre"]
                bebida = next((b for b in self.bebidas if b["nombre"] == nombre_bebida), None)
                if not bebida:
                    continue

                if bebida["categoria"] in ["Bebida caliente", "Bebida fria"]:
                    ingredientes_base = ["Leche", "Cafe", "Agua", "Azucar", "Hielo"]
                    for ingrediente in ingredientes_base:
                        item = next((i for i in inventario if i["ingrediente"].lower() == ingrediente.lower()), None)
                        if item and item["cantidad"] < 15:
                            ingredientes_faltantes.append(ingrediente)

            if ingredientes_faltantes:
                messagebox.showerror("Inventario insuficiente", f"No hay suficiente de: {', '.join(set(ingredientes_faltantes))}.")
                return

            total = float(self.total_compra.cget("text").replace("Total: $", ""))
            puntos_ganados = int((total // 100) * 10)
            self.puntos_acumulados += puntos_ganados
            self.puntos_data[self.email] = self.puntos_acumulados
            self.puntos_manager.guardar_puntos(self.puntos_data)
            self.lbl_puntos.configure(text=f"Tienes {self.puntos_acumulados} puntos")

            pedido = {
                "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "cliente": self.nombre_cliente,
                "email": self.email,
                "productos": [],
                "total": total,
                "estado": "completado"
            }

            for datos in self.seleccion_bebidas.values():
                info = {
                    "nombre": datos["nombre"],
                    "cantidad": datos.get("cantidad", 1)
                }
                if "tamano" in datos:
                    info["tipo"] = "bebida"
                    info["tamano"] = datos["tamano"]
                    info["extras"] = datos.get("extras", [])
                else:
                    info["tipo"] = "postre"

                pedido["productos"].append(info)
                self.pedido_manager.actualizar_inventario(datos["nombre"], info["cantidad"])

            self.pedido_manager.guardar_pedido(pedido)
            self.seleccion_bebidas.clear()
            self.actualizar_carrito()

            messagebox.showinfo(
                "Compra Confirmada",
                f"¡Gracias por tu compra, {self.nombre_cliente}!\n\n"
                f"Total: ${total:.2f}\n"
                f"Puntos ganados: {puntos_ganados}\n"
                f"Puntos totales: {self.puntos_acumulados}"
            )

            self.mostrar_promociones_disponibles()

        except Exception as e:
            print(f"[ERROR en confirmar_compra]: {e}")  # ← útil en pruebas con consola
            messagebox.showerror("Error", "Ocurrió un error al procesar la compra.")

        finally:
            self.btn_confirmar_compra.configure(state="normal")  # 🔓 Reactiva botón


    def eliminar_producto_carrito(self, clave):
        if clave in self.seleccion_bebidas:
            del self.seleccion_bebidas[clave]
            self.actualizar_carrito()

    def editar_producto_carrito(self, clave):
        datos = self.seleccion_bebidas[clave]
        bebida = next((b for b in self.bebidas if b["nombre"] == datos["nombre"]), None)
        if bebida:
            self.personalizar_bebida(bebida,clave)
        else:
            messagebox.showerror("Error", "No se pudo encontrar la bebida original para editar.")

    # -------------------------------------
    def crear_tab_puntos(self):
        ctk.CTkLabel(self.tab_puntos, text="Sistema de Puntos", font=("Arial", 16)).pack(pady=10)
        self.lbl_puntos = ctk.CTkLabel(self.tab_puntos, text=f"Tienes {self.puntos_acumulados} puntos", font=("Arial", 16))
        self.lbl_puntos.pack(pady=10)

        ctk.CTkLabel(self.tab_puntos, text="Promociones disponibles", font=("Arial", 14)).pack(pady=5)

        self.promos_frame_cliente = ctk.CTkScrollableFrame(self.tab_puntos, width=600, height=250)
        self.promos_frame_cliente.pack(pady=5)

        self.mostrar_promociones_disponibles()

    def mostrar_promociones_disponibles(self):
        for widget in self.promos_frame_cliente.winfo_children():
            widget.destroy()

        promociones = self.promocion_manager.cargar_promociones()
        for promo in promociones:
            puede_redimir = self.puntos_acumulados >= promo["costo_puntos"]
    
            frame = ctk.CTkFrame(
                self.promos_frame_cliente,
                fg_color="#2a2a2a" if puede_redimir else "#1f1f1f"  # gris más oscuro si no se puede redimir
            )
            frame.pack(fill="x", padx=5, pady=5)

            texto = f"{promo['nombre']} ({promo['categoria']}) - {promo['costo_puntos']} pts"

            label = ctk.CTkLabel(
                frame,
                text=texto,
                text_color="white" if puede_redimir else "gray70"
            )
            label.pack(side="left", padx=10)

            if puede_redimir:
                ctk.CTkButton(
                    frame,
                    text="Obtener",
                    width=100,
                    command=lambda p=promo: self.redimir_promocion(p)
                ).pack(side="right", padx=5)
            else:
                faltan = promo["costo_puntos"] - self.puntos_acumulados
                ctk.CTkLabel(
                    frame,
                    text=f"Faltan {faltan} puntos",
                    text_color="gray70"
                ).pack(side="right", padx=10)

    def redimir_promocion(self, promo):
        categoria = promo["categoria"]
        productos = [b for b in self.bebidas if b["categoria"] == categoria]
        if not productos:
            messagebox.showwarning("Sin productos", f"No hay productos de categoría {categoria} disponibles.")
            return
        
        

        ventana_redimir = ctk.CTkToplevel()
        ventana_redimir.title("Selecciona tu producto")
        ventana_redimir.geometry("400x400")

        ctk.CTkLabel(ventana_redimir, text=f"Elige 1 {categoria} para redimir").pack(pady=10)
        seleccion = ctk.StringVar()
        nombres = [p["nombre"] for p in productos]
        combo = ctk.CTkOptionMenu(ventana_redimir, values=nombres, variable=seleccion)
        combo.set(nombres[0])
        combo.pack(pady=10)

        def confirmar():
            producto = next((b for b in productos if b["nombre"] == seleccion.get()), None)
            if not producto:
                messagebox.showerror("Error", "Producto no encontrado.")
                ventana_redimir.destroy()
                return

            clave = f"{producto['nombre']}_promo"
            self.seleccion_bebidas[clave] = {
                "nombre": producto["nombre"],
                "promo": True
            }

            if self.puntos_acumulados < promo["costo_puntos"]:
                messagebox.showwarning("Puntos insuficientes", "Ya no tienes los puntos suficientes para esta promoción.")
                ventana_redimir.destroy()
                return
            
            self.puntos_acumulados -= promo["costo_puntos"]
            self.puntos_data[self.email] = self.puntos_acumulados
            self.puntos_manager.guardar_puntos(self.puntos_data)
            self.lbl_puntos.configure(text=f"Tienes {self.puntos_acumulados} puntos")
            self.actualizar_carrito()
            self.mostrar_promociones_disponibles()
            ventana_redimir.destroy()

        ctk.CTkButton(ventana_redimir, text="Confirmar", command=confirmar).pack(pady=10)
            
    


    
