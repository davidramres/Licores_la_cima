from datetime import datetime
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import messagebox, ttk
from tkinter import *
from PIL import Image, ImageTk
from PIL import *

class Controlador():
    def __init__(self):
        pass

    def limpiar_marco(self,marco):        
        for widget in marco.winfo_children():
            widget.destroy()        
        
    def obtener_fecha(self):
        fecha=datetime.now().strftime("%d/%m/%Y")
        return fecha
    
    def llenar_tabla(self,tabla,clase_tabla):
        clase_tabla.mostrar_productos(tabla)
        
    def llenar_tabla_clientes(self,tabla,clase_tabla):
        clase_tabla.mostrar_clientes(tabla)
    
    def llenar_tabla_ventas(self,tabla,clase_tabla):
        clase_tabla.mostrar_historia_ventas(tabla)
        
    def llenar_tabla_empleados(self,tabla,clase_tabla):
        clase_tabla.mostrar_empleados(tabla)
    
    def datos_comboclase(self,nombre_clase):#metodo para llenar el combobox
        conexion = sqlite3.connect("La_cima.db")  # Conecta a tu base de datos
        cursor = conexion.cursor()
        # Consulta SQL para obtener los valores de 'cantidad' de la tabla 'producto'
        cursor.execute(f"SELECT nombre FROM {nombre_clase}")
        datos = cursor.fetchall()
        conexion.close()
        return [dato[0] for dato in datos]  # Extrae los valores de la tupla
    
    # Crear una función que se ejecutará cuando se seleccione un elemento
    def seleccionar(event,combo):
        seleccion = combo.get()
        return seleccion
    
    def obtener_detalles_producto(self, nombre_producto): # Conectar a la base de datos 
        conexion = sqlite3.connect("La_cima.db") 
        cursor = conexion.cursor() # Consulta SQL para obtener los detalles del producto seleccionado 
        cursor.execute("SELECT precio, cantidad, tipo FROM Producto WHERE nombre=?", (nombre_producto,)) 
        resultado = cursor.fetchone() 
        conexion.close() 
        if resultado: 
            return {'precio': resultado[0], 'cantidad': resultado[1], 'tipo': resultado[2]} 
        else: 
            return ("Producto no encontrado")
        
    def obtener_codigo_producto(self, nombre_producto): # Conectar a la base de datos 
        conexion = sqlite3.connect("La_cima.db") 
        cursor = conexion.cursor() # Consulta SQL para obtener los detalles del producto seleccionado 
        cursor.execute("SELECT codigo FROM Producto WHERE nombre=?", (nombre_producto,)) 
        resultado = cursor.fetchone() 
        conexion.close() 
        if resultado: 
            return  resultado[0]
        else: 
            return messagebox.showwarning("Base de datos", "Producto no encontrado")
        
    def obtener_codigo_cliente(self, nombre_cliente): # Conectar a la base de datos 
        conexion = sqlite3.connect("La_cima.db") 
        cursor = conexion.cursor() # Consulta SQL para obtener los detalles del producto seleccionado 
        cursor.execute("SELECT codigo FROM Cliente WHERE nombre=?", (nombre_cliente,)) 
        resultado = cursor.fetchone() 
        conexion.close() 
        if resultado: 
            return  resultado[0]
        else: 
            return messagebox.showwarning("Base de datos", "Cliente no encontrado")
        
    def obtener_codigo_empleado(self, nombre_empleado): # Conectar a la base de datos 
        conexion = sqlite3.connect("La_cima.db") 
        cursor = conexion.cursor() # Consulta SQL para obtener los detalles del producto seleccionado 
        cursor.execute("SELECT codigo FROM Empleado WHERE nombre=?", (nombre_empleado,)) 
        resultado = cursor.fetchone() 
        conexion.close() 
        if resultado: 
            return  resultado[0]
        else: 
            return messagebox.showwarning("Base de datos", "Empleado no encontrado")
    
    def obtener_codigo_venta(self): # Conectar a la base de datos 
        conexion = sqlite3.connect("La_cima.db") 
        cursor = conexion.cursor() # Consulta SQL para obtener los detalles del producto seleccionado 
        cursor.execute("SELECT codigo FROM Venta") 
        resultado = cursor.fetchone() 
        conexion.close() 
        if resultado: 
            return  resultado[0]
        else: 
            return messagebox.showwarning("Base de datos", "Venta no encontrada")
    
    def crear_tablabd_usuarios(self):    
        conexion = sqlite3.connect('La_cima.db')
        cursor = conexion.cursor()
        #borrar tabla usuarios
        cursor.execute("DROP TABLE IF EXISTS usuario")
        # Crear tabla Usuarios
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuario (
            codigo INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            contraseña TEXT NOT NULL            
        )
        """)
        cursor.execute(f'''INSERT INTO usuario (usuario,contraseña)
                       VALUES ("lacima","123")''')
        conexion.commit()
        conexion.close()
        
    def verificar_usuario(self, vent_principal, vent_inicio, usuario, contraseña):
        self.crear_tablabd_usuarios()
        # Conectar a la base de datos        
        conexion = sqlite3.connect("La_cima.db")
        cursor = conexion.cursor()
        # Ejecutar la consulta para verificar el usuario y la contraseña
        cursor.execute('SELECT * FROM usuario WHERE usuario=? AND contraseña=?', (usuario, contraseña))
        resultado = cursor.fetchone()
        # Cerrar la conexión a la base de datos
        conexion.close()
        # Verificar el resultado de la consulta
        if resultado:
            messagebox.showinfo("Inicio de sesión", "Inicio de sesión exitoso")
            vent_inicio.destroy()  # Cierra la ventana de inicio de sesión
            vent_principal.deiconify()  # Muestra la ventana principal
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
            
    def generar_reporte_mas_vendidos():
        """
        Genera un gráfico de barras para los productos más vendidos.
        """
        conexion = sqlite3.connect("La_cima.db")
        consulta = "SELECT nombreProducto, totalVendido FROM ProductosMasVendidos LIMIT 10"
        df = pd.read_sql_query(consulta, conexion)
        conexion.close()

        if df.empty:
            print("No hay datos disponibles para los productos más vendidos.")
            return
        else:
            plt.figure(figsize=(10, 6))
            plt.barh(df['nombreProducto'], df['totalVendido'], color='skyblue')
            plt.xlabel('Cantidad Vendida')
            plt.ylabel('Producto')
            plt.title('Top 10 Productos más Vendidos')
            plt.gca().invert_yaxis()
            plt.tight_layout()
            plt.show()

        return

    def generar_reporte_menos_vendidos():
        """
        Genera un gráfico de barras para los productos menos vendidos.
        """
        conexion = sqlite3.connect("La_cima.db")
        consulta = "SELECT nombreProducto, totalVendido FROM ProductosMenosVendidos LIMIT 10"
        df = pd.read_sql_query(consulta, conexion)
        conexion.close()

        if df.empty:
            print("No hay datos disponibles para los productos menos vendidos.")
            return
        else:
            plt.figure(figsize=(10, 6))
            plt.barh(df['nombreProducto'], df['totalVendido'], color='salmon')
            plt.xlabel('Cantidad Vendida')
            plt.ylabel('Producto')
            plt.title('Top 10 Productos Menos Vendidos')
            plt.gca().invert_yaxis()
            plt.tight_layout()
            plt.show()

        return    


    def generar_reporte_ventas_por_cliente(cliente, ventana_reporte, imagen_fondo):
        # Conectar a la base de datos y realizar la consulta
        conexion = sqlite3.connect("La_cima.db")
        consulta = f"SELECT nombreProducto, cantidad, subtotal, fechaVenta FROM ProductosPorCliente WHERE nombreCliente = '{cliente}'"
        df = pd.read_sql_query(consulta, conexion)
        conexion.close()
        
        if df.empty:
            messagebox.showwarning("Base de datos", f"No se encontraron compras para el cliente {cliente}")
            return       
    
        fondo = Label(ventana_reporte, image=imagen_fondo)
        fondo.place(x=0, y=0, relwidth=1, relheight=1)
        etiqueta = Label(ventana_reporte, text=f"Reporte de Compras del Cliente: {cliente}")
        etiqueta.pack()
        tree = ttk.Treeview(ventana_reporte)
        tree["columns"] = ("nombreProducto", "cantidad", "subtotal", "fechaVenta")
        tree.column("#0", width=0, stretch=NO)
        tree.column("nombreProducto", width=200, anchor=CENTER)
        tree.column("cantidad", width=100, anchor=CENTER)
        tree.column("subtotal", width=100, anchor=CENTER)
        tree.column("fechaVenta", width=150, anchor=CENTER)
        tree.heading("nombreProducto", text="Producto")
        tree.heading("cantidad", text="Cantidad")
        tree.heading("subtotal", text="Subtotal")
        tree.heading("fechaVenta", text="Fecha de Venta")
        tree.pack()
    
        for i, row in df.iterrows():
            tree.insert("", "end", values=(row["nombreProducto"], row["cantidad"], row["subtotal"], row["fechaVenta"]))
    
        total = df["subtotal"].sum()
        eti_total = Label(ventana_reporte, text=f"Total: {total} $")
        eti_total.pack()
        
        def exportar_csv(): 
            nombre_archivo = f"reporte_compras_cliente_{cliente}.csv" 
            df['Total'] = total
            df.to_csv(nombre_archivo, index=False) 
            messagebox.showinfo("Exportar CSV", f"Reporte exportado como {nombre_archivo}")            
             
        boton_exportar = Button(ventana_reporte, text="Exportar a CSV", command=exportar_csv) 
        boton_exportar.pack()        
        Button(ventana_reporte, text="Salir", command=ventana_reporte.destroy).pack()
        

    def generar_reporte_ventas_por_empleado(empleado, ventana_reporte, imagen_fondo):
        # Conectar a la base de datos y realizar la consulta
        conexion = sqlite3.connect("La_cima.db")
        consulta = f"SELECT fechaVenta, totalVenta,nombreCliente FROM VentasPorEmpleado WHERE nombreEmpleado = '{empleado}'"
        df = pd.read_sql_query(consulta, conexion)
        conexion.close()
    
        if df.empty:
            messagebox.showwarning("Base de datos", f"No se encontraron ventas para el empleado {empleado}")
            return
    
        fondo = Label(ventana_reporte, image=imagen_fondo)
        fondo.place(x=0, y=0, relwidth=1, relheight=1)
        etiqueta = Label(ventana_reporte, text=f"Reporte de Ventas del Empleado: {empleado}")
        etiqueta.pack()
        tree = ttk.Treeview(ventana_reporte)
        tree["columns"] = ("nombreCliente", "fechaVenta", "totalVenta")
        tree.column("#0", width=0, stretch=NO)
        tree.column("nombreCliente", width=200, anchor=CENTER)
        tree.column("fechaVenta", width=150, anchor=CENTER)
        tree.column("totalVenta", width=100, anchor=CENTER)
        tree.heading("nombreCliente", text="Cliente")
        tree.heading("fechaVenta", text="Fecha de Venta")
        tree.heading("totalVenta", text="Total de Ventas")
        tree.pack()
    
        for i, row in df.iterrows():
            tree.insert("", "end", values=(row["nombreCliente"], row["fechaVenta"], row["totalVenta"]))
    
        total = df["totalVenta"].sum()
        eti_total = Label(ventana_reporte, text=f"Total: {total} $")
        eti_total.pack()
        
        def exportar_csv(): 
            nombre_archivo = f"reporte_compras_empleado_{empleado}.csv" 
            df['Total'] = total 
            df.to_csv(nombre_archivo, index=False) 
            messagebox.showinfo("Exportar CSV", f"Reporte exportado como {nombre_archivo}")            
             
        boton_exportar = Button(ventana_reporte, text="Exportar a CSV", command=exportar_csv) 
        boton_exportar.pack() 
        
        Button(ventana_reporte, text="Salir", command=ventana_reporte.destroy).pack()

    def generar_reporte_ventas_totales(ventana_reporte, imagen_fondo):
        # Conectar a la base de datos y realizar la consulta
        conexion = sqlite3.connect("La_cima.db")
        consulta = "SELECT fechaVenta, totalVenta,nombreCliente,nombreEmpleado FROM HistorialDeVentasConNombres"
        df = pd.read_sql_query(consulta, conexion)
        conexion.close()

        fondo = Label(ventana_reporte, image=imagen_fondo)
        fondo.place(x=0, y=0, relwidth=1, relheight=1)
        etiqueta = Label(ventana_reporte, text="Reporte de Ventas Totales")
        etiqueta.pack()
        tree = ttk.Treeview(ventana_reporte)
        tree["columns"] = ("fechaVenta", "totalVenta","nombreCliente","nombreEmpleado")
        tree.column("#0", width=0, stretch=NO)
        tree.column("fechaVenta", width=150, anchor=CENTER)
        tree.column("totalVenta", width=100, anchor=CENTER)
        tree.column("nombreCliente", width=200, anchor=CENTER)
        tree.column("nombreEmpleado", width=200, anchor=CENTER)
        tree.heading("fechaVenta", text="Fecha de Venta")
        tree.heading("totalVenta", text="Total de Ventas")
        tree.heading("nombreCliente", text="Cliente")
        tree.heading("nombreEmpleado", text="Empleado")
        tree.pack()
    
        for i, row in df.iterrows():
            tree.insert("", "end", values=(row["fechaVenta"], row["totalVenta"],row["nombreCliente"],row["nombreEmpleado"]))
    
        total = df["totalVenta"].sum()
        eti_total = Label(ventana_reporte, text=f"Total: {total} $")
        eti_total.pack()
        
        def exportar_csv(): 
            nombre_archivo = f"reporte_total_ventas.csv" 
            df['Total'] = total
            df.to_csv(nombre_archivo, index=False) 
            messagebox.showinfo("Exportar CSV", f"Reporte exportado como {nombre_archivo}")            
             
        boton_exportar = Button(ventana_reporte, text="Exportar a CSV", command=exportar_csv) 
        boton_exportar.pack() 
        
        
        Button(ventana_reporte, text="Salir", command=ventana_reporte.destroy).pack()    

    def generar_reporte_ventas_fecha(fecha, ventana_reporte, imagen_fondo):
        conexion = sqlite3.connect("La_cima.db")
        consulta = f"SELECT * FROM ReporteVentasCompleto WHERE fecha = '{fecha}'"
        df = pd.read_sql_query(consulta, conexion)
        conexion.close()

        if df.empty:
            messagebox.showinfo("Reporte de Ventas por Fecha", f"No se encontraron ventas para la fecha {fecha}.")
            return

        fondo = Label(ventana_reporte, image=imagen_fondo)
        fondo.place(x=0, y=0, relwidth=1, relheight=1)
        etiqueta = Label(ventana_reporte, text="Reporte de Ventas por Fecha")
        etiqueta.pack()
        tree = ttk.Treeview(ventana_reporte)
        tree["columns"] = ("fecha", "ventas_totales", "nombre_cliente", "nombre_empleado")
        tree.column("#0", width=0, stretch=NO)
        tree.column("fecha", width=150, anchor=CENTER)
        tree.column("ventas_totales", width=100, anchor=CENTER)
        tree.column("nombre_cliente", width=200, anchor=CENTER)
        tree.column("nombre_empleado", width=200, anchor=CENTER)
        tree.heading("fecha", text="Fecha de Venta")
        tree.heading("ventas_totales", text="Total de Ventas")
        tree.heading("nombre_cliente", text="Cliente")
        tree.heading("nombre_empleado", text="Empleado")
        tree.pack()

        for i, row in df.iterrows():
            tree.insert("", "end", values=(row["fecha"], row["ventas_totales"], row["nombre_cliente"], row["nombre_empleado"]))

        total = df["ventas_totales"].sum()
        eti_total = Label(ventana_reporte, text=f"Total: {total} $")
        eti_total.pack()
        fecha_formateada = fecha.replace('/', '-')# le cambiamos de formato a la fecha para guardar correctamente el archivo csv
        
        def exportar_csv():
            nombre_archivo = f"reporte_ventas_fecha_{fecha_formateada}.csv"
            df['Total'] = total
            df.to_csv(nombre_archivo, index=False)
            messagebox.showinfo("Exportar CSV", f"Reporte exportado como {nombre_archivo}")

        boton_exportar = Button(ventana_reporte, text="Exportar a CSV", command=exportar_csv)
        boton_exportar.pack()

        Button(ventana_reporte, text="Salir", command=ventana_reporte.destroy).pack()
