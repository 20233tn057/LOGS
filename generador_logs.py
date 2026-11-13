import random
import re
import socket
import subprocess
import platform
from datetime import datetime
import MiDispositivo
import output

# ==========================================
# Configuración Global
# ==========================================
ARCHIVO_LOG = output.ARCHIVO_NETWORK_LOGS


def obtener_ip_local():
    """
    Obtiene la dirección IP local activa del equipo actual.
    Autor: Jenifer Reyes
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return "127.0.0.1"


def obtener_gateway_red():
    """
    Obtiene la puerta de enlace predeterminada del sistema.
    Autor: Jenifer Reyes
    """
    sistema = platform.system().lower()

    try:
        if sistema == "darwin":
            salida = subprocess.check_output(["route", "-n", "get", "default"], text=True, stderr=subprocess.STDOUT)
            coincidencia = re.search(r"gateway:\s+([0-9.]+)", salida)
            if coincidencia:
                return coincidencia.group(1)

        elif sistema == "linux":
            for comando in (["ip", "route", "show", "default"], ["route", "-n"]):
                try:
                    salida = subprocess.check_output(comando, text=True, stderr=subprocess.STDOUT)
                    coincidencia = re.search(r"(?:default|0\.0\.0\.0)\s+([0-9.]+)", salida)
                    if coincidencia:
                        return coincidencia.group(1)
                except Exception:
                    continue

        elif sistema == "windows":
            salida = subprocess.check_output(["ipconfig"], text=True, stderr=subprocess.STDOUT)
            coincidencia = re.search(r"Predeterminado.*?:\s*([0-9.]+)", salida, re.IGNORECASE)
            if coincidencia:
                return coincidencia.group(1)
    except Exception:
        pass

    return "No disponible"


def obtener_mac_red():
    """
    Obtiene la dirección MAC de la interfaz de red principal.
    Autor: Jenifer Reyes
    """
    sistema = platform.system().lower()

    try:
        if sistema == "darwin":
            salida = subprocess.check_output(["ifconfig", "-a"], text=True, stderr=subprocess.STDOUT)
            coincidencia = re.search(r"ether\s+([0-9A-Fa-f:]+)", salida)
            if coincidencia:
                return coincidencia.group(1)

        elif sistema == "linux":
            salida = subprocess.check_output(["ip", "link"], text=True, stderr=subprocess.STDOUT)
            coincidencia = re.search(r"link/ether\s+([0-9A-Fa-f:]+)", salida)
            if coincidencia:
                return coincidencia.group(1)

        elif sistema == "windows":
            salida = subprocess.check_output(["ipconfig", "/all"], text=True, stderr=subprocess.STDOUT)
            coincidencia = re.search(r"Direcci[oó]n\s+f[ií]sica.*?:\s*([0-9A-Fa-f-]+)", salida)
            if coincidencia:
                return coincidencia.group(1)
    except Exception:
        pass

    return "No disponible"


def obtener_info_red():
    """
    Reúne la información de red y del dispositivo apoyándose en MiDispositivo.
    Autor: Jenifer Reyes
    """
    info_dispositivo = MiDispositivo.obtener_info_dispositivo()

    return {
        "timestamp": datetime.now().isoformat(),
        "tipo": "info_red",
        "hostname": info_dispositivo.get("hostname", socket.gethostname()),
        "ip_local": obtener_ip_local(),
        "gateway": obtener_gateway_red(),
        "mac_address": obtener_mac_red(),
        "sistema_operativo": info_dispositivo.get("system", platform.system()),
        "version_sistema": info_dispositivo.get("release", platform.release())
    }


def registrar_datos_equipo_y_red():
    """
    Coordina el guardado de los datos del dispositivo (vía MiDispositivo -> output)
    y registra la información de red actual (vía output.generar_logs).
    """
    MiDispositivo.guardar_info_dispositivo()
    MiDispositivo.guardar_comando_red()

    info_red = obtener_info_red()
    output.generar_logs(info_red, ARCHIVO_LOG)
    return info_red


def mostrar_info_red():
    """
    Muestra en pantalla la información técnica de la red del equipo.
    Autor: Jenifer Reyes
    """
    info = obtener_info_red()
    print("=== INFORMACIÓN DE RED ===")
    for clave, valor in info.items():
        print(f"{clave}: {valor}")
    return info


def generar_ip():
    """
    Genera una dirección IPv4 aleatoria.
    Autor: Jenifer Reyes
    """
    return f"{random.randint(1, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"


def crear_evento_red(ip_origen, ip_destino):
    """
    Crea un diccionario que representa un evento de red con datos simulados.
    Autor: Jenifer Reyes
    """
    puertos_comunes = [80, 443, 22, 53, 8080]
    estados = ["PERMITIDO", "BLOQUEADO", "SOSPECHOSO"]
    protocolos = ["TCP", "UDP"]
    usuarios = ["admin", "invitado", "analista", "sistema"]

    return {
        "timestamp": datetime.now().isoformat(),
        "ip_origen": ip_origen,
        "ip_destino": ip_destino,
        "puerto_destino": random.choice(puertos_comunes),
        "protocolo": random.choice(protocolos),
        "bytes_enviados": random.randint(64, 4096),
        "estado": random.choice(estados),
        "latencia_ms": random.randint(5, 120),
        "usuario": random.choice(usuarios)
    }


def simular_trafico(cantidad_eventos=10):
    """
    Genera múltiples eventos de tráfico de red y los envía a output.generar_logs().
    Autor: Jenifer Reyes
    """
    print(f"Iniciando simulación de {cantidad_eventos} eventos de red...")

    for _ in range(cantidad_eventos):
        ip_src = generar_ip()
        ip_dst = "192.168.1.1"

        evento = crear_evento_red(ip_src, ip_dst)
        output.generar_logs(evento, ARCHIVO_LOG)

    print(f"¡Simulación completada! Registros enviados a '{ARCHIVO_LOG}'.")


def leer_logs_bloqueados(nombre_archivo=ARCHIVO_LOG):
    """
    Consulta los registros desde output y filtra únicamente los que tienen
    el campo 'estado' igual a 'BLOQUEADO'.
    Autor: Jenifer Reyes
    """
    registros = output.leer_logs(nombre_archivo)
    registros_bloqueados = [
        evento for evento in registros
        if evento.get("estado") == "BLOQUEADO"
    ]

    print("=== EVENTOS BLOQUEADOS ===")
    if not registros_bloqueados:
        print("No se encontraron registros bloqueados.")
    else:
        for evento in registros_bloqueados:
            print(
                f"[{evento['timestamp']}] IP: {evento['ip_origen']} | "
                f"Usuario: {evento['usuario']} | Latencia: {evento['latencia_ms']}ms | "
                f"Estado: {evento['estado']}"
            )

    return registros_bloqueados