import sqlite3
from tkinter import messagebox
import datetime 

db_nombre = "La_cima.db"
#crear conexion a la base de datos
conexion = sqlite3.connect(db_nombre)
cursor = conexion.cursor()

# creamos la clase Producto
class Producto:
    def __init__(self, codigo, nombre, precio, cantidad, tipo):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad
        self.tipo = tipo

    # Método agregar producto
    def agregar_producto(self, nombre, precio, cantidad, tipo): 
        #creamos la conexion a la base de datos
        conexion = sqlite3.connect(db_nombre) 
        cursor = conexion.cursor() 
        #usamos un try para capturar los posibles errores en la base de datos
        try: 
            #insertamos los datos en la base de datos con una consulta sql 
            cursor.execute("INSERT INTO Producto (nombre, precio, cantidad, tipo) VALUES (?,?, ?, ?)", (nombre, precio, cantidad, tipo)) 
            conexion.commit() 
            #mostramos un mensaje de confirmacion
            messagebox.showinfo("Base de datos", "Producto creado con éxito") 
        except sqlite3.IntegrityError: 
            #mostramos un mensaje de error si el producto ya existe
            messagebox.showwarning("Base de datos", "El producto ya existe") 
        finally: 
            #cerramos la conexion a la base de datos
            conexion.close()       
    def eliminar_producto(self, nombre):
        conexion = sqlite3.connect(db_nombre)
        cursor = conexion.cursor()
        try:
            cursor.execute("DELETE FROM Producto WHERE nombre = ?", (nombre,))
            if cursor.rowcount == 0:
                messagebox.showwarning('Base de datos', f'No se encontró el producto {nombre}')
            else:
                conexion.commit()
                messagebox.showinfo('Base de datos', f'El producto {nombre} ha sido eliminado correctamente')
        except sqlite3.Error as e:
            messagebox.showerror('Base de datos', f'Ocurrió un error al eliminar el producto: {e}')
        finally:
            conexion.close()
    def actualizar_producto(self,nombre, precio, cantidad, tipo,nuevo_nombre,nuevo_precio,nueva_cantidad,nuevo_tipo):
        conexion = sqlite3.connect(db_nombre)
        cursor = conexion.cursor()
        try:
            cursor.execute("UPDATE Producto SET nombre=?, precio = ?, cantidad = ?, tipo = ? WHERE nombre=? AND precio=? AND cantidad=? AND tipo=?",(nuevo_nombre,nuevo_precio,nueva_cantidad,nuevo_tipo,nombre,precio,cantidad,tipo))             
            conexion.commit()
            messagebox.showinfo("Base de datos", "Producto actualizado con éxito")
        except sqlite3.Error as e:
            messagebox.showerror('Base de datos', f'Ocurrió un error al actualizar el producto: {e}')
        finally:
            conexion.close()

    def mostrar_productos(self, tabla):
        conexion = sqlite3.connect(db_nombre)
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Producto")
        for item in tabla.get_children():
            tabla.delete(item)
        for row in cursor.fetchall():
            tabla.insert("", 'end', values=(row[1], row[2], row[3], row[4]))
        conexion.close()          

    def actualizar_cantidad(self, codigo, cantidad_vendida):
        conexion = sqlite3.connect(db_nombre)
        cursor = conexion.cursor()
        try:
            cursor.execute("UPDATE Producto SET cantidad = cantidad - ? WHERE codigo = ?", (cantidad_vendida, codigo))
            conexion.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Base de datos", f"Ocurrió un error al actualizar la cantidad del producto: {e}")
        finally:
            conexion.close()

# Clase Cliente
class Cliente:
    def __init__(self, codigo, nombre, direccion, telefono):
        self.codigo = codigo
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.historial_compras = []

    # Métodos
    def agregar_cliente(self, nombre, direccion, telefono): 
        #creamos la conexion a la base de datos
        conexion = sqlite3.connect(db_nombre) 
        cursor = conexion.cursor() 
        #usamos un try para capturar los posibles errores en la base de datos
        try: 
            #insertamos los datos en la base de datos con una consulta sql 
            cursor.execute("INSERT INTO Cliente (nombre, direccion, telefono) VALUES (?, ?, ?)", (nombre, direccion, telefono)) 
            conexion.commit() 
            #mostramos un mensaje de confirmacion
            messagebox.showinfo("Base de datos", "Cliente ingresado con éxito") 
        except sqlite3.IntegrityError: 
            #mostramos un mensaje de error si el cliente ya existe
            messagebox.showwarning("Base de datos", "El clienteya existe") 
        finally: 
            #cerramos la conexion a la base de datos
            conexion.close()   

    def eliminar_cliente(self, nombre):
        conexion = sqlite3.connect(db_nombre)
        cursor = conexion.cursor()
        try:
            cursor.execute("DELETE FROM Cliente WHERE nombre = ?", (nombre,))
            if cursor.rowcount == 0:
                messagebox.showwarning('Base de datos', f'No se encontró el cliente {nombre}')
            else:
                conexion.commit()
                messagebox.showinfo('Base de datos', f'El cliente {nombre} ha sido eliminado correctamente')
        except sqlite3.Error as e:
            messagebox.showerror('Base de datos', f'Ocurrió un error al eliminar el producto: {e}')
        finally:
            conexion.close()

            
    def editar_cliente(self,nombre, direccion, telefono, nuevo_nombre, nueva_direccion, nuevo_telefono):
        conexion = sqlite3.connect(db_nombre)
        cursor = conexion.cursor()
        try:
            cursor.execute("UPDATE Cliente SET nombre=?, direccion = ?, telefono = ? WHERE nombre=? AND direccion=? AND telefono=?",(nuevo_nombre,nueva_direccion,nuevo_telefono,nombre,direccion,telefono)) 
            conexion.commit()
            messagebox.showinfo("Base de datos", "Cliente actualizado con éxito")
        except sqlite3.Error as e:
            messagebox.showerror('Base de datos', f'Ocurrio un error al actualizar el cliente: {e}')
        finally:
            conexion.close()
            
    def mostrar_clientes(self, tabla):
        conexion = sqlite3.connect(db_nombre)
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Cliente")
        for item in tabla.get_children():
            tabla.delete(item)
        for row in cursor.fetchall():
            tabla.insert("", 'end', values=(row[1], row[2], row[3]))
        conexion.close()



    def agregar_compra(self, venta):
        self.historial_compras.append(venta)

    def obtener_historial_compras(self):
        return self.historial_compras


# Clase Empleado
class Empleado:
    def __init__(self, codigo, nombre, direccion, telefono):
        self.codigo = codigo
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.historial_ventas = []

    # Métodos
    def agregar_empleado(self, nombre, direccion, telefono): 
        #creamos la conexion a la base de datos
        conexion = sqlite3.connect(db_nombre) 
        cursor = conexion.cursor() 
        #usamos un try para capturar los posibles errores en la base de datos
        try: 
            #insertamos los datos en la base de datos con una consulta sql 
            cursor.execute("INSERT INTO Empleado (nombre, direccion, telefono) VALUES (?, ?, ?)", (nombre, direccion, telefono)) 
            conexion.commit() 
            #mostramos un mensaje de confirmacion
            messagebox.showinfo("Base de datos", "Empleado ingresado con éxito") 
        except sqlite3.IntegrityError: 
            #mostramos un mensaje de error si el Empleado ya existe
            messagebox.showwarning("Base de datos", "El Empleado ya existe") 
        finally: 
            #cerramos la conexion a la base de datos
            conexion.close()   

    def eliminar_empleado(self, nombre):
        conexion = sqlite3.connect(db_nombre)
        cursor = conexion.cursor()
        try:
            cursor.execute("DELETE FROM Empleado WHERE nombre = ?", (nombre,))
            if cursor.rowcount == 0:
                messagebox.showwarning('Base de datos', f'No se encontró el Empleado {nombre}')
            else:
                conexion.commit()
                messagebox.showinfo('Base de datos', f'El Empleado {nombre} ha sido eliminado correctamente')
        except sqlite3.Error as e:
            messagebox.showerror('Base de datos', f'Ocurrió un error al eliminar el Empleado: {e}')
        finally:
            conexion.close()

            
    def editar_empleado(self,nombre, direccion, telefono, nuevo_nombre, nueva_direccion, nuevo_telefono):
        conexion = sqlite3.connect(db_nombre)
        cursor = conexion.cursor()
        try:
            cursor.execute("UPDATE Empleado SET nombre=?, direccion = ?, telefono = ? WHERE nombre=? AND direccion=? AND telefono=?",(nuevo_nombre,nueva_direccion,nuevo_telefono,nombre,direccion,telefono)) 
            conexion.commit()
            messagebox.showinfo("Base de datos", "Empleado actualizado con éxito")
        except sqlite3.Error as e:
            messagebox.showerror('Base de datos', f'Ocurrio un error al actualizar el Empleado: {e}')
        finally:
            conexion.close()
            
    def mostrar_empleados(self, tabla):
        conexion = sqlite3.connect(db_nombre)
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Empleado")
        for item in tabla.get_children():
            tabla.delete(item)
        for row in cursor.fetchall():
            tabla.insert("", 'end', values=(row[1], row[2], row[3]))
        conexion.close()
        
# Clase Venta
class Venta: 
    def __init__(self, fecha, total, codigo_cliente, codigo_empleado): 
        self.fecha = fecha 
        self.total = total 
        self.codigo_cliente = codigo_cliente 
        self.codigo_empleado = codigo_empleado 
        
    def agregar_venta(self): 
        conexion = sqlite3.connect(db_nombre) 
        cursor = conexion.cursor() 
        try: 
            cursor.execute(''' INSERT INTO Venta (fecha, total, codigo_cliente, codigo_empleado) VALUES (?, ?, ?, ?) ''', (self.fecha, self.total, self.codigo_cliente, self.codigo_empleado)) 
            conexion.commit() 
            codigo_venta = cursor.lastrowid  # Obtener el código de la venta
            messagebox.showinfo("Base de datos", "Venta registrada con éxito") 
            return codigo_venta
        except sqlite3.Error as e: 
            messagebox.showerror("Base de datos", f"Error al registrar la venta: {e}") 
            conexion.rollback() 
        finally:
            conexion.close()
        return None

            
    def eliminar_venta(self, codigo_venta):
        conexion = sqlite3.connect(db_nombre)
        cursor = conexion.cursor()
        try:
            cursor.execute("DELETE FROM Venta WHERE codigo = ?", (codigo_venta,))
            if cursor.rowcount == 0:
                messagebox.showwarning('Base de datos', f'No se encontró la venta {codigo_venta}')
            else:
                conexion.commit()
                messagebox.showinfo('Base de datos', f'La venta {codigo_venta} ha sido eliminada correctamente')
        except sqlite3.Error as e:
            messagebox.showerror('Base de datos', f'Ocurrio un error al eliminar la venta: {e}')
        finally:
            conexion.close()
            
    def mostrar_ventas(self, tabla):
        conexion = sqlite3.connect(db_nombre)
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Venta")
        for item in tabla.get_children():
            tabla.delete(item)
        for row in cursor.fetchall():
            tabla.insert("", 'end', values=(row[1], row[2], row[3], row[4], row[5]))
        conexion.close()
        
    def mostrar_historia_ventas(self, tabla):
        conexion = sqlite3.connect(db_nombre)
        cursor = conexion.cursor()
        cursor.execute("SELECT fechaVenta,totalVenta,nombreCliente,nombreEmpleado FROM HistorialDeVentasConNombres")
        for item in tabla.get_children():
            tabla.delete(item)
        for row in cursor.fetchall():
            tabla.insert("", 'end', values=(row[0], row[1], row[2], row[3]))
        conexion.close()
# Clase DetalleVenta
class DetalleVenta:
    def __init__(self, codigo, codigo_venta, codigo_producto, cantidad, precio_unitario, subtotal):
        self.codigo = codigo
        self.codigo_venta = codigo_venta
        self.codigo_producto = codigo_producto
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.subtotal = subtotal

    # Métodos
    def agregar_detalle_venta(self, codigo_venta, codigo_producto, cantidad, precio_unitario, subtotal):
        conexion = sqlite3.connect(db_nombre)
        cursor = conexion.cursor()
        try:
            cursor.execute("INSERT INTO DetalleVenta (codigo_venta, codigo_producto, cantidad, precio_unitario, subtotal) VALUES (?, ?, ?, ?, ?)", (codigo_venta, codigo_producto, cantidad, precio_unitario, subtotal))
            conexion.commit()
        except sqlite3.Error as e:
            messagebox.showerror('Base de datos', f'Ocurrio un error al agregar el detalle de venta: {e}')
        finally:
            conexion.close()

    def eliminar_detalle_venta(self):
        conexion = sqlite3.connect(db_nombre)
        cursor = conexion.cursor()
        try:
            cursor.execute("DELETE FROM DetalleVenta WHERE codigo = ?", (self.codigo,))
            conexion.commit()
            messagebox.showinfo("Base de datos", "Detalle de venta eliminado con éxito")
        except sqlite3.Error as e:
            messagebox.showerror('Base de datos', f'Ocurrio un error al eliminar el detalle de venta: {e}')
        finally:
            conexion.close()

    def obtener_subtotal(self):
        return self.subtotal
    
    def mostrar_detalle_venta(self, tabla):
        conexion = sqlite3.connect(db_nombre)
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM DetalleVenta")
        for item in tabla.get_children():
            tabla.delete(item)
        for row in cursor.fetchall():
            tabla.insert("", 'end', values=(row[1], row[2], row[3], row[4], row[5]))
        conexion.close()
        

