import csv
import os
from datetime import datetime

# Definir la ubicación de la carpeta de Downloads
downloads_folder = os.path.expanduser("~/Downloads/ArchivosExamen")
csv_filename = os.path.join(downloads_folder, "flujo_efectivo.csv")

# Función para ingresar datos financieros
def ingresar_datos():
    fecha = input("Ingrese la fecha (dd-MM-yyyy): ")
    try:
        # Validar formato de fecha
        fecha_dt = datetime.strptime(fecha, "%d-%m-%Y")
    except ValueError:
        print("Formato de fecha incorrecto. Use dd-MM-yyyy.")
        return None

    mes_reporte = fecha_dt.month
    anio_reporte = fecha_dt.year
    tipo_registro = input("Ingrese el tipo de registro (Ingreso/Egreso): ").capitalize()

    if tipo_registro not in ["Ingreso", "Egreso"]:
        print("Tipo de registro inválido. Debe ser 'Ingreso' o 'Egreso'.")
        return None

    try:
        monto = float(input("Ingrese el monto: "))
    except ValueError:
        print("Monto inválido. Debe ser un número.")
        return None

    return {
        "fecha": fecha,
        "mesReporte": mes_reporte,
        "añoReporte": anio_reporte,
        "tipoRegistro": tipo_registro,
        "monto": monto
    }

# Función para guardar los datos en un archivo CSV
def guardar_en_csv(datos):
    existe_archivo = os.path.exists(csv_filename)
    
    with open(csv_filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        
        # Escribir encabezados solo si el archivo no existe
        if not existe_archivo:
            writer.writerow(["fecha", "mesReporte", "añoReporte", "tipoRegistro", "monto"])
        
        # Escribir los datos
        writer.writerow([datos["fecha"], datos["mesReporte"], datos["añoReporte"], datos["tipoRegistro"], datos["monto"]])
    print(f"Datos guardados exitosamente en {csv_filename}")

# Programa principal
def main():
    print("Sistema de Ingreso de Datos Financieros")
    while True:
        datos = ingresar_datos()
        
        if datos:
            guardar_en_csv(datos)
        
        otra_entrada = input("¿Desea ingresar otro registro? (s/n): ").lower()
        if otra_entrada != 's':
            break

if __name__ == "__main__":
    main()
