# aadrr.py
import os
import json
from agente import  AgentePlanificacion

def cargar_procesos(archivo="datos_procesos.json"):
    """Carga los datos de procesos desde un archivo JSON"""
    directorio_base = os.path.dirname(os.path.abspath(__file__))
    ruta_completa = os.path.join(directorio_base, archivo)
    with open(ruta_completa, "r") as f:
        return json.load(f)

def planificador_aadrr(procesos):
    """Ejecuta el planificador AADRR basado en agentes"""
    agente = AgentePlanificacion(procesos)
    linea_tiempo, completados, registro_quantum, registro_agente = agente.ejecutar()
    return linea_tiempo, completados, registro_quantum, registro_agente

# Prueba por línea de comandos
if __name__ == "__main__":
    procesos = cargar_procesos()
    linea_tiempo, completados, registro_quantum, registro_agente = planificador_aadrr(procesos)

    print("\nLínea de Tiempo de Ejecución:")
    for segmento in linea_tiempo:
        print(f"{segmento['pid']}: {segmento['inicio']} → {segmento['fin']}")

    print("\n📋 Tabla de Completado de Procesos:")
    for p in completados:
        print(f"{p['pid']} completado en {p['completado']} | TAT={p['tat']} | WT={p['wt']}")

    print("\n🌀 Registro de Quantum Dinámico:")
    for tiempo, quantum in registro_quantum:
        print(f"Tiempo {tiempo}: DTQ = {quantum}")

    print("\n🤖 Registro de Decisiones del Agente:")
    for entrada in registro_agente:
        print(f"Ciclo {entrada['ciclo']} @ {entrada['tiempo_inicio']}: "
              f"DTQ={entrada['dtq']} | Ordenados: {entrada['pids_ordenados']}")