import json

ARCHIVO_NETWORK_LOGS = "network_logs.jsonl"
ARCHIVO_DEVICE_DATA = "device_data.jsonl"


def generar_logs(datos, nombre_archivo=ARCHIVO_NETWORK_LOGS):
    """
    Recibe un diccionario de datos y lo guarda como una línea JSON
    en el archivo .jsonl especificado.

    Parámetros:
    datos (dict): Diccionario con la información o evento a registrar.
    nombre_archivo (str): Ruta del archivo .jsonl destino.

    Salida:
    bool: True si se guardó correctamente, False si ocurrió un error.
    """
    try:
        with open(nombre_archivo, "a", encoding="utf-8") as archivo:
            linea_json = json.dumps(datos, ensure_ascii=False)
            archivo.write(linea_json + "\n")
        return True
    except Exception as e:
        print(f"Error al escribir en '{nombre_archivo}': {e}")
        return False


def leer_logs(nombre_archivo=ARCHIVO_NETWORK_LOGS):
    """
    Lee un archivo .jsonl línea por línea y devuelve una lista de diccionarios.

    Parámetros:
    nombre_archivo (str): Ruta del archivo .jsonl a leer.

    Salida:
    list[dict]: Registros cargados desde el archivo.
    """
    registros = []
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if linea:
                    registros.append(json.loads(linea))
    except FileNotFoundError:
        print(f"El archivo '{nombre_archivo}' no existe todavía.")
    except Exception as e:
        print(f"Error al leer '{nombre_archivo}': {e}")

    return registros