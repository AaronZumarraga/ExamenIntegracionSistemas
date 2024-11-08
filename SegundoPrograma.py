import pyodbc
import csv
import os

# Configuración de la conexión a SQL Server con autenticación de Windows
server = 'MSI'  # Cambia a tu servidor de SQL Server
database = 'Contabilidadbdd'  # Cambia al nombre de tu base de datos

# Ruta del archivo CSV en la carpeta de Downloads
csv_filepath = os.path.expanduser("~/Downloads/ArchivosExamen/flujo_efectivo.csv")

# Función para establecer la conexión a SQL Server
def conectar_sql_server():
    try:
        conexion = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"Trusted_Connection=yes;"
        )
        print("Conexión exitosa a SQL Server.")
        return conexion
    except pyodbc.Error as e:
        print("Error al conectar con SQL Server:", e)
        return None

# Función para cargar datos desde el archivo CSV a la base de datos
def cargar_datos_a_sql(conexion):
    cursor = conexion.cursor()

    # Comprobar si el archivo CSV existe
    if not os.path.exists(csv_filepath):
        print(f"El archivo {csv_filepath} no existe.")
        return

    # Leer el archivo CSV y cargar cada registro en la tabla SQL Server
    with open(csv_filepath, mode="r") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Saltar la fila de encabezado

        for row in csv_reader:
            fecha = row[0]
            mesReporte = int(row[1])
            añoReporte = int(row[2])
            tipoRegistro = row[3]
            monto = float(row[4])

            # Insertar datos en la tabla
            try:
                cursor.execute("""
                    INSERT INTO flujo_efectivo (fecha, mesReporte, añoReporte, tipoRegistro, monto)
                    VALUES (?, ?, ?, ?, ?)
                """, fecha, mesReporte, añoReporte, tipoRegistro, monto)
                conexion.commit()
                print(f"Registro insertado: {fecha}, {mesReporte}, {añoReporte}, {tipoRegistro}, {monto}")
            except pyodbc.Error as e:
                print("Error al insertar en SQL Server:", e)
    
    print("Todos los datos se han cargado correctamente en la base de datos.")
    cursor.close()

# Programa principal
def main():
    conexion = conectar_sql_server()
    if conexion:
        cargar_datos_a_sql(conexion)
        conexion.close()
        print("Conexión cerrada.")

if __name__ == "__main__":
    main()
