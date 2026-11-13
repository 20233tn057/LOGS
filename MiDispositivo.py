import platform
import socket
import subprocess
import uuid
from datetime import datetime
import output

try:
    import psutil
except ImportError:
    psutil = None

ARCHIVO_DISPOSITIVO = output.ARCHIVO_DEVICE_DATA


def obtener_info_dispositivo():
    """
    Recopila información del dispositivo mediante librerías de Python
    y devuelve un diccionario con los datos.
    """
    data = {
        "timestamp": datetime.utcnow().isoformat(),
        "hostname": socket.gethostname(),
        "fqdn": socket.getfqdn(),
        "ip": socket.gethostbyname(socket.gethostname()),
        "mac": ":".join(
            f"{(uuid.getnode() >> ele) & 0xff:02x}"
            for ele in range(40, -1, -8)
        ),
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
    }

    if psutil:
        data.update({
            "cpu_count_logical": psutil.cpu_count(),
            "cpu_count_physical": psutil.cpu_count(logical=False),
            "memory_total": psutil.virtual_memory().total,
            "memory_available": psutil.virtual_memory().available,
            "disk_partitions": [
                {
                    "device": p.device,
                    "mountpoint": p.mountpoint,
                    "fstype": p.fstype
                }
                for p in psutil.disk_partitions()
            ],
            "network_interfaces": {
                k: [str(addr.address) for addr in v]
                for k, v in psutil.net_if_addrs().items()
            }
        })

    return data


def guardar_info_dispositivo(jsonl_file=ARCHIVO_DISPOSITIVO):
    """
    Obtiene la información del dispositivo y la envía al módulo output
    para guardarla en device_data.jsonl.
    """
    print("Guardando información del dispositivo...")
    data = obtener_info_dispositivo()
    output.generar_logs(data, jsonl_file)
    return data


def obtener_comando_red():
    """
    Ejecuta ipconfig /all (Windows) o ifconfig (Linux/macOS)
    y devuelve la salida estructurada en un diccionario.
    """
    sistema = platform.system()
    try:
        if sistema == "Windows":
            resultado = subprocess.run(
                ["ipconfig", "/all"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="ignore"
            )
            salida = resultado.stdout
            comando = "ipconfig /all"
        else:
            resultado = subprocess.run(
                ["ifconfig"],
                capture_output=True,
                text=True
            )
            salida = resultado.stdout
            comando = "ifconfig"

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "command": comando,
            "output": salida
        }
    except Exception as e:
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e)
        }


def guardar_comando_red(jsonl_file=ARCHIVO_DISPOSITIVO):
    """
    Obtiene la salida del comando de red y la envía al módulo output.
    """
    print("Guardando salida del comando de red...")
    data = obtener_comando_red()
    output.generar_logs(data, jsonl_file)
    return data