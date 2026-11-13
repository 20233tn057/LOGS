import json
from flask import Flask, render_template

app = Flask(__name__, template_folder="templates/views")

ARCHIVO_LOG = "network_logs.jsonl"


def leer_logs(filtro="bloqueados"):
    logs = []
    try:
        with open(ARCHIVO_LOG, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if not linea:
                    continue
                evento = json.loads(linea)

                estado = evento.get("estado")
                if filtro == "bloqueados" and estado == "BLOQUEADO":
                    logs.append(evento)
                elif filtro == "no_bloqueados" and estado != "BLOQUEADO":
                    logs.append(evento)
                elif filtro == "todos":
                    logs.append(evento)
    except FileNotFoundError:
        print(f"El archivo {ARCHIVO_LOG} no existe aún. Ejecuta generador_logs.py primero.")

    return logs


# Ruta por defecto y /bloqueados
@app.route("/")
@app.route("/bloqueados")
def bloqueados():
    lista = leer_logs("bloqueados")
    return render_template("incidentes.html", lista=lista, titulo="Eventos Bloqueados")


# Ruta /no_bloqueados
@app.route("/no_bloqueados")
def no_bloqueados():
    lista = leer_logs("no_bloqueados")
    return render_template("incidentes.html", lista=lista, titulo="Eventos No Bloqueados")


# Ruta /todos
@app.route("/todos")
def todos():
    lista = leer_logs("todos")
    return render_template("incidentes.html", lista=lista, titulo="Todos los Eventos")


if __name__ == "__main__":
    app.run(debug=True)