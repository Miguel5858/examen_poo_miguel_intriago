import csv

def leer_cotizaciones(cotizacion):
    try:
        datos_intriago = {}
        with open(cotizacion, 'r', encoding='utf-8-sig') as archivo_csv:
            lector_csv = csv.DictReader(archivo_csv, delimiter=';')

            # Obtener las columnas del archivo
            columnas = lector_csv.fieldnames

            # Inicializar el diccionario con listas vacías para cada columna
            for columna in columnas:
                datos_intriago[columna] = []

            # Leer las filas del archivo y organizar los datos en el diccionario
            for fila in lector_csv:
                for columna in columnas:
                    datos_intriago[columna].append(fila[columna])

        return datos_intriago

    except FileNotFoundError:
        print(f"El archivo {cotizacion} no fue encontrado.")
        return None
    except Exception as e:
        print("Ocurrió un error al leer el archivo:", str(e))
        return None

def generar_resumen(datos_intriago):
    if datos_intriago:
        try:
            # Crear un nuevo archivo CSV llamado resumen_cotizaciones_intriago.csv
            with open('resumen_cotizaciones_intriago.csv', 'w', newline='') as archivo_csv:
                # Crear un escritor CSV
                escritor_csv = csv.writer(archivo_csv)

                # Obtener las columnas numéricas
                final_intriago = 'Final'
                maximo_intriago = 'Máximo'
                minimo_intriago = 'Mínimo'
                volumen_intriago = 'Volumen'
                efectivo_intriago = 'Efectivo'

                # Calcular la media, el valor mínimo y el valor máximo para cada columna numérica
                resumen = {}
                for columna in [final_intriago, maximo_intriago, minimo_intriago, volumen_intriago, efectivo_intriago]:
                    valores = datos_intriago[columna]
                    valores_float = [float(valor.replace(',', '.').replace('.', '')) for valor in valores]
                    minimo = round(min(valores_float), 2)
                    maximo = round(max(valores_float), 2)
                    media = round(sum(valores_float) / len(valores_float), 2)
                    resumen[columna] = {
                        'Mínimo': minimo,
                        'Máximo': maximo,
                        'Media': media
                    }

                # Escribir la fila de encabezado
                escritor_csv.writerow(['Columna', 'Mínimo', 'Máximo', 'Media'])

                # Escribir los valores calculados en el archivo CSV
                for columna in [final_intriago, maximo_intriago, minimo_intriago, volumen_intriago, efectivo_intriago]:
                    valores = resumen[columna]
                    escritor_csv.writerow([columna, valores['Mínimo'], valores['Máximo'], valores['Media']])

            print("El archivo resumen_cotizaciones_intriago.csv se ha creado exitosamente con los valores calculados.")

        except Exception as e:
            print("Ocurrió un error al generar el resumen:", str(e))
    else:
        print("No se pudo generar el resumen debido a un error en la lectura de datos.")

if __name__ == "__main__":
    nombre_archivo = 'cotizacion.csv'  # Reemplaza con el nombre de tu archivo CSV

    try:
        # Llama a la función leer_cotizaciones
        datos_intriago = leer_cotizaciones(nombre_archivo)

        if datos_intriago:
            print("Datos leídos exitosamente:")
            for columna, valores in datos_intriago.items():
                print(columna, ":", valores)

            # Llama a la función generar_resumen con el diccionario devuelto por leer_cotizaciones
            generar_resumen(datos_intriago)
            print("Resumen generado exitosamente.")

    except Exception as e:
        print("Error:", str(e))
