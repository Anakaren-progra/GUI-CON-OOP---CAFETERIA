# ui_gerente.py
import customtkinter as ctk
from tkinter import messagebox
from backend_oop import InventarioManager, BebidaManager, JSONStorage, PromocionManager
import tkinter as tk

class GerenteUI:
    def __init__(self, ventana_inicio, nombre):
        self.ventana_inicio = ventana_inicio
        self.nombre = nombre
        self.inventario_manager = InventarioManager()
        self.bebida_manager = BebidaManager()
        self.bebidas = self.bebida_manager.cargar_bebidas()

        self.ventana = ctk.CTkToplevel()
        self.ventana.title("Entorno del Gerente")
        self.ventana.geometry("600x700")

        self.crear_interfaz()

    def mostrar(self):
        self.ventana.deiconify()

    def crear_interfaz(self):
        pestañas = ctk.CTkTabview(self.ventana)
        pestañas.pack(expand=True, fill="both")
        self.tab_promociones = pestañas.add("Promociones")
        self.crear_tab_promociones()

        # --- TAB Inventario ---
        tab_inventario = pestañas.add("Inventario")

        ctk.CTkLabel(tab_inventario, text="Gestión de Inventario", font=("Arial", 16)).pack(pady=10)

        self.entry_ingrediente = ctk.CTkEntry(tab_inventario, width=300, placeholder_text="Ingrediente")
        self.entry_cantidad = ctk.CTkEntry(tab_inventario, width=300, placeholder_text="Cantidad")
        self.entry_ingrediente.pack(pady=5)
        self.entry_cantidad.pack(pady=5)

        ctk.CTkButton(tab_inventario, text="Agregar", command=self.agregar_ingrediente).pack(pady=5)

        ctk.CTkLabel(tab_inventario, text="Seleccionar para eliminar o editar:").pack(pady=(10, 0))
        self.ingrediente_seleccionado = ctk.StringVar()
        self.combo_ingredientes = ctk.CTkOptionMenu(tab_inventario, variable=self.ingrediente_seleccionado, values=[""])
        self.combo_ingredientes.pack(pady=5)

        self.entry_nueva_cantidad = ctk.CTkEntry(tab_inventario, width=300, placeholder_text="Nueva cantidad (solo para editar)")
        self.entry_nueva_cantidad.pack(pady=5)

        ctk.CTkButton(tab_inventario, text="Eliminar", command=self.eliminar_ingrediente).pack(pady=5)
        ctk.CTkButton(tab_inventario, text="Editar cantidad", command=self.editar_ingrediente).pack(pady=5)

        self.lista_inventario = ctk.CTkTextbox(tab_inventario, width=400, height=150)
        self.lista_inventario.pack(pady=10)

        self.actualizar_lista_inventario()

        # --- TAB Precios ---
        tab_precios = pestañas.add("Asignar Precios")

        self.seleccion_bebida = ctk.StringVar()
        self.lista_nombres = [b["nombre"] for b in self.bebidas]
        self.combo_bebidas = ctk.CTkOptionMenu(tab_precios, values=self.lista_nombres, variable=self.seleccion_bebida, command=self.llenar_campos_precio)
        self.combo_bebidas.pack(pady=10)

        self.entry_chico = ctk.CTkEntry(tab_precios, placeholder_text="Precio chico")
        self.entry_mediano = ctk.CTkEntry(tab_precios, placeholder_text="Precio mediano")
        self.entry_grande = ctk.CTkEntry(tab_precios, placeholder_text="Precio grande")
        self.entry_extra = ctk.CTkEntry(tab_precios, placeholder_text="Precio ingrediente extra")
        self.entry_postre = ctk.CTkEntry(tab_precios, placeholder_text="Precio postre")

        ctk.CTkButton(tab_precios, text="Guardar Precio", command=self.guardar_precios).pack(pady=10)

        if self.lista_nombres:
            self.seleccion_bebida.set(self.lista_nombres[0])
            self.llenar_campos_precio()

        # --- Botón cerrar sesión ---
        ctk.CTkButton(self.ventana, text="Cerrar Sesión", command=self.cerrar_sesion).pack(pady=10)

    def cerrar_sesion(self):
        self.ventana.destroy()
        self.ventana_inicio.deiconify()
    

    def actualizar_lista_inventario(self):
        self.lista_inventario.delete("1.0", "end")
        inventario = self.inventario_manager.cargar()
        nombres = []
        for item in inventario:
            self.lista_inventario.insert("end", f"{item['ingrediente']}: {item['cantidad']}\n")
            nombres.append(item['ingrediente'])

        self.combo_ingredientes.configure(values=nombres)
        if nombres:
            self.ingrediente_seleccionado.set(nombres[0])

    def agregar_ingrediente(self):
        nombre = self.entry_ingrediente.get()
        cantidad = self.entry_cantidad.get()
        if not nombre or not cantidad:
            messagebox.showerror("Error", "Debe llenar ambos campos")
            return
        self.inventario_manager.agregar_ingrediente(nombre, cantidad)
        self.actualizar_lista_inventario()

    def eliminar_ingrediente(self):
        nombre = self.ingrediente_seleccionado.get()
        if not nombre:
            messagebox.showerror("Error", "Debe seleccionar un ingrediente")
            return
        self.inventario_manager.eliminar_ingrediente(nombre)
        self.actualizar_lista_inventario()

    def editar_ingrediente(self):
        nombre = self.ingrediente_seleccionado.get()
        nueva_cantidad = self.entry_nueva_cantidad.get()
        if not nombre or not nueva_cantidad:
            messagebox.showerror("Error", "Debe seleccionar un ingrediente y definir cantidad")
            return
        self.inventario_manager.editar_ingrediente(nombre, nueva_cantidad)
        self.actualizar_lista_inventario()

    

    def llenar_campos_precio(self, *args):
        self.ocultar_campos_precio()

        nombre = self.seleccion_bebida.get()
        bebida = next((b for b in self.bebidas if b["nombre"] == nombre), None)
        if not bebida:
            return

        precios = bebida.get("precios", {})

        if bebida["categoria"] in ["Bebida fria", "Bebida caliente"]:
            self.entry_chico.pack(pady=3)
            self.entry_mediano.pack(pady=3)
            self.entry_grande.pack(pady=3)
            self.entry_extra.pack(pady=3)

            self.entry_chico.delete(0, "end")
            self.entry_chico.insert(0, precios.get("chico", ""))
            self.entry_mediano.delete(0, "end")
            self.entry_mediano.insert(0, precios.get("mediano", ""))
            self.entry_grande.delete(0, "end")
            self.entry_grande.insert(0, precios.get("grande", ""))
            self.entry_extra.delete(0, "end")
            self.entry_extra.insert(0, precios.get("extra", ""))
        else:
            self.entry_postre.pack(pady=3)
            self.entry_extra.pack(pady=3)

            self.entry_postre.delete(0, "end")
            self.entry_postre.insert(0, precios.get("precio", ""))
            self.entry_extra.delete(0, "end")
            self.entry_extra.insert(0, precios.get("extra", ""))

    def ocultar_campos_precio(self):
        for entry in [self.entry_chico, self.entry_mediano, self.entry_grande, self.entry_extra, self.entry_postre]:
            entry.pack_forget()

    def guardar_precios(self):
        nombre = self.seleccion_bebida.get()
        for bebida in self.bebidas:
            if bebida["nombre"] == nombre:
                if bebida["categoria"] in ["Bebida fria", "Bebida caliente"]:
                    bebida["precios"] = {
                        "chico": self.entry_chico.get(),
                        "mediano": self.entry_mediano.get(),
                        "grande": self.entry_grande.get(),
                        "extra": self.entry_extra.get()
                    }
                else:
                    bebida["precios"] = {
                        "precio": self.entry_postre.get(),
                        "extra": self.entry_extra.get()
                    }
                break

        JSONStorage.guardar("bebidas.json", self.bebidas)
        messagebox.showinfo("Éxito", "Precios actualizados correctamente")

    from backend_oop import PromocionManager

    def crear_tab_promociones(self):
        self.promocion_manager = PromocionManager()
        self.lista_promociones = self.promocion_manager.cargar_promociones()

        ctk.CTkLabel(self.tab_promociones, text="Agregar Promoción", font=("Arial", 16)).pack(pady=10)

        self.entry_nombre_promo = ctk.CTkEntry(self.tab_promociones, width=300, placeholder_text="Nombre de la promoción")
        self.entry_costo_puntos = ctk.CTkEntry(self.tab_promociones, width=300, placeholder_text="Costo en puntos")
        self.combo_categoria_promo = ctk.CTkOptionMenu(self.tab_promociones, values=["Bebida caliente", "Bebida fria", "Postre"])
        self.combo_categoria_promo.set("Bebida caliente")

        for widget in [self.entry_nombre_promo, self.entry_costo_puntos, self.combo_categoria_promo]:
            widget.pack(pady=5)

        ctk.CTkButton(self.tab_promociones, text="Agregar Promoción", command=self.agregar_promocion).pack(pady=10)

        ctk.CTkLabel(self.tab_promociones, text="Promociones disponibles", font=("Arial", 14)).pack(pady=10)
        # Contenedor con canvas
        contenedor_scroll = tk.Frame(self.tab_promociones)
        contenedor_scroll.pack(fill="x", pady=5)

        canvas = tk.Canvas(contenedor_scroll, height=200)
        scroll_x = tk.Scrollbar(contenedor_scroll, orient="horizontal", command=canvas.xview)
        canvas.configure(xscrollcommand=scroll_x.set)

        scroll_x.pack(side="bottom", fill="x")
        canvas.pack(side="top", fill="both", expand=True)

        # Frame interno donde pondremos las promociones
        self.promos_frame = ctk.CTkFrame(canvas)
        canvas.create_window((0, 0), window=self.promos_frame, anchor="nw")

        # Hacer que se actualice el tamaño del canvas automáticamente
        def resize_canvas(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        self.promos_frame.bind("<Configure>", resize_canvas)

        self.actualizar_lista_promos()

    def agregar_promocion(self):
        nombre = self.entry_nombre_promo.get().strip()
        categoria = self.combo_categoria_promo.get()
        try:
            puntos = int(self.entry_costo_puntos.get())
        except ValueError:
            messagebox.showerror("Error", "El costo debe ser un número")
            return

        if not nombre or not categoria or puntos < 0:
            messagebox.showerror("Error", "Complete todos los campos correctamente")
            return

        self.promocion_manager.agregar_promocion(nombre, categoria, puntos)
        messagebox.showinfo("Éxito", "Promoción agregada")
        self.actualizar_lista_promos()

    def actualizar_lista_promos(self):
        for widget in self.promos_frame.winfo_children():
            widget.destroy()

        promociones = self.promocion_manager.cargar_promociones()
        for promo in promociones:
            frame = ctk.CTkFrame(self.promos_frame)
            frame.pack(fill="x", padx=5, pady=5)

            texto = f"{promo['nombre']} - {promo['categoria']} - {promo['costo_puntos']} pts"
            ctk.CTkLabel(frame, text=texto, anchor="w").pack(side="left", padx=10)

            ctk.CTkButton(frame, text="Eliminar", width=80, fg_color="#d9534f",
                      command=lambda n=promo['nombre']: self.eliminar_promocion(n)).pack(side="right", padx=5)

    def eliminar_promocion(self, nombre):
        self.promocion_manager.eliminar_promocion(nombre)
        self.actualizar_lista_promos()



