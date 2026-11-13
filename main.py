import generador_logs


def ejecutar_orquestacion():
    print("Ejecutando main...\n")

    # 1. Recolectar y guardar información del dispositivo y de la red
    generador_logs.registrar_datos_equipo_y_red()
    print()

    # 2. Mostrar resumen de red en consola
    generador_logs.mostrar_info_red()
    print()

    # 3. Simular tráfico de red y guardarlo en network_logs.jsonl vía output.py
    generador_logs.simular_trafico(10)
    print()

    # 4. Consultar y mostrar eventos bloqueados
    generador_logs.leer_logs_bloqueados()

    print("\nProceso main terminado.")


if __name__ == "__main__":
    ejecutar_orquestacion()