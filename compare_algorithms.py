# compare_algorithms.py
import json
from collections import deque

# ----------------- Cargar Procesos -----------------
def cargar_procesos():
    """
    Carga los procesos desde el archivo JSON o usa datos por defecto
    """
    try:
        with open('process_data.json', 'r') as f:
            data = json.load(f)
            procesos = []
            for p in data['processes']:
                procesos.append({
                    'pid': p['id'],
                    'llegada': p['arrival_time'],
                    'rafaga': p['burst_time'],
                    'prioridad': p['priority']
                })
            return procesos
    except FileNotFoundError:
        # Datos por defecto si no existe el archivo
        return [
            {'pid': 'P1', 'llegada': 0, 'rafaga': 8, 'prioridad': 2},
            {'pid': 'P2', 'llegada': 0, 'rafaga': 4, 'prioridad': 1},
            {'pid': 'P3', 'llegada': 0, 'rafaga': 6, 'prioridad': 3},
            {'pid': 'P4', 'llegada': 0, 'rafaga': 6, 'prioridad': 2},
            {'pid': 'P5', 'llegada': 0, 'rafaga': 4, 'prioridad': 4},
            {'pid': 'P6', 'llegada': 0, 'rafaga': 7, 'prioridad': 2}
        ]

# ----------------- FCFS (Primero en Llegar, Primero en Servirse) -----------------
def fcfs_scheduler(procesos):
    procesos = sorted(procesos, key=lambda x: x["llegada"])
    tiempo, linea_tiempo, completados = 0, [], []
    primer_inicio = {}

    for p in procesos:
        if tiempo < p["llegada"]:
            tiempo = p["llegada"]
        inicio = tiempo
        fin = inicio + p["rafaga"]
        if p["pid"] not in primer_inicio:
            primer_inicio[p["pid"]] = inicio
        linea_tiempo.append({"pid": p["pid"], "inicio": inicio, "fin": fin})
        completados.append({"pid": p["pid"], "tiempo_fin": fin})
        tiempo = fin

    return linea_tiempo, completados

# ----------------- Round Robin -----------------
def round_robin_scheduler(procesos, quantum_tiempo=4):
    procesos = [p.copy() for p in sorted(procesos, key=lambda x: x["llegada"])]
    cola = deque()
    linea_tiempo, completados = [], []
    tiempo = 0
    llegados = []
    primer_inicio = {}

    while procesos or cola or llegados:
        # Agregar procesos que han llegado
        llegados += [p for p in procesos if p["llegada"] <= tiempo]
        procesos = [p for p in procesos if p["llegada"] > tiempo]
        for p in llegados:
            if p not in cola:
                cola.append(p)
        llegados = []

        if not cola:
            tiempo += 1
            continue

        p = cola.popleft()
        pid = p["pid"]
        tiempo_ejecucion = min(quantum_tiempo, p["rafaga"])

        if pid not in primer_inicio:
            primer_inicio[pid] = tiempo

        linea_tiempo.append({"pid": pid, "inicio": tiempo, "fin": tiempo + tiempo_ejecucion})
        tiempo += tiempo_ejecucion
        p["rafaga"] -= tiempo_ejecucion

        if p["rafaga"] > 0:
            cola.append(p)
        else:
            completados.append({"pid": pid, "tiempo_fin": tiempo})

    return linea_tiempo, completados

# ----------------- AADRR Scheduler -----------------
def aadrr_scheduler(procesos, A=10, B=5):
    """
    Implementación simplificada de AADRR
    """
    import math
    import copy
    
    procesos = [p.copy() for p in procesos]
    tiempo = 0
    linea_tiempo = []
    completados = []
    primer_inicio = {}
    
    while procesos:
        # Calcular quantum dinámico (mediana de ráfagas)
        rafagas = [p["rafaga"] for p in procesos]
        rafagas.sort()
        quantum = rafagas[len(rafagas) // 2]  # Mediana
        
        # Calcular rangos: A * ráfaga + B * prioridad
        for p in procesos:
            p["rank"] = A * p["rafaga"] + B * p["prioridad"]
        
        # Ordenar por rank (ascendente)
        procesos.sort(key=lambda x: x["rank"])
        
        i = 0
        while i < len(procesos):
            p = procesos[i]
            pid = p["pid"]
            
            if pid not in primer_inicio:
                primer_inicio[pid] = tiempo
            
            # Condición de finalización anticipada
            if p["rafaga"] <= math.sqrt(quantum):
                tiempo_ejecucion = p["rafaga"]
                p["rafaga"] = 0
                
                linea_tiempo.append({"pid": pid, "inicio": tiempo, "fin": tiempo + tiempo_ejecucion})
                tiempo += tiempo_ejecucion
                
                completados.append({"pid": pid, "tiempo_fin": tiempo})
                procesos.pop(i)
            else:
                tiempo_ejecucion = min(quantum, p["rafaga"])
                p["rafaga"] -= tiempo_ejecucion
                
                linea_tiempo.append({"pid": pid, "inicio": tiempo, "fin": tiempo + tiempo_ejecucion})
                tiempo += tiempo_ejecucion
                i += 1
    
    return linea_tiempo, completados

# ----------------- Impresor Unificado de Métricas -----------------
def imprimir_metricas(linea_tiempo, completados, procesos, nombre_algoritmo):
    # Crear mapeo de procesos
    pid_a_proceso = {p["pid"]: p for p in procesos}
    primeros_inicios = {}
    
    # Encontrar primer inicio de cada proceso
    for segmento in linea_tiempo:
        pid = segmento["pid"]
        if pid not in primeros_inicios:
            primeros_inicios[pid] = segmento["inicio"]

    resultados = []

    # Calcular métricas para cada proceso completado
    for p in completados:
        pid = p["pid"]
        fin = p["tiempo_fin"]
        proceso_original = pid_a_proceso[pid]
        
        llegada = proceso_original["llegada"]
        rafaga = proceso_original["rafaga"]
        tat = fin - llegada  # Tiempo de Retorno
        wt = tat - rafaga    # Tiempo de Espera
        rt = primeros_inicios[pid] - llegada  # Tiempo de Respuesta
        
        resultados.append((pid, llegada, rafaga, fin, tat, wt, rt))

    print(f"\n{'='*60}")
    print(f"📊 PLANIFICADOR: {nombre_algoritmo}")
    print(f"{'='*60}")
    print("Proceso | Llegada | Ráfaga | Finaliz. | TAT   | TE    | TR")
    print("-" * 65)
    
    for r in resultados:
        print(f"{r[0]:<8} {r[1]:<8} {r[2]:<8} {r[3]:<10} {r[4]:<6} {r[5]:<6} {r[6]:<6}")

    # Calcular promedios
    tat_promedio = round(sum(r[4] for r in resultados) / len(resultados), 2)
    wt_promedio = round(sum(r[5] for r in resultados) / len(resultados), 2)
    rt_promedio = round(sum(r[6] for r in resultados) / len(resultados), 2)

    print(f"\n📈 MÉTRICAS PROMEDIO:")
    print(f"• Tiempo de Retorno (TAT): {tat_promedio} ms")
    print(f"• Tiempo de Espera (TE):   {wt_promedio} ms")
    print(f"• Tiempo de Respuesta (TR): {rt_promedio} ms")

    return tat_promedio, wt_promedio, rt_promedio

# ----------------- Ejecutor Principal -----------------
def ejecutar_y_comparar():
    print("🚀 INICIANDO COMPARACIÓN DE ALGORITMOS DE PLANIFICACIÓN")
    print("=" * 70)
    
    algoritmos = {
        "AADRR": aadrr_scheduler,
        "FCFS": fcfs_scheduler,
        "RR": lambda p: round_robin_scheduler(p, quantum_tiempo=4),
    }

    comparacion = []

    for nombre, planificador in algoritmos.items():
        print(f"\n🎯 EJECUTANDO: {nombre}")
        
        # Cargar procesos frescos para cada algoritmo
        procesos = cargar_procesos()
        
        # Ejecutar el planificador
        linea_tiempo, completados = planificador(procesos)
        
        # Calcular y mostrar métricas
        tat_prom, wt_prom, rt_prom = imprimir_metricas(linea_tiempo, completados, procesos, nombre)
        comparacion.append((nombre, tat_prom, wt_prom, rt_prom))

    # Mostrar comparación final
    print("\n" + "=" * 70)
    print("🏆 COMPARACIÓN FINAL - RESUMEN")
    print("=" * 70)
    print("Algoritmo    | TAT Prom | TE Prom  | TR Prom")
    print("-" * 45)
    
    for nombre, tat, wt, rt in comparacion:
        print(f"{nombre:<13}| {tat:<9}| {wt:<9}| {rt:<9}")

    # Encontrar el mejor algoritmo
    mejor_tat = min(comparacion, key=lambda x: x[1])
    mejor_te = min(comparacion, key=lambda x: x[2])
    mejor_tr = min(comparacion, key=lambda x: x[3])
    
    print(f"\n✅ MEJORES RESULTADOS:")
    print(f"   • Mejor TAT: {mejor_tat[0]} ({mejor_tat[1]} ms)")
    print(f"   • Mejor TE:  {mejor_te[0]} ({mejor_te[2]} ms)")
    print(f"   • Mejor TR:  {mejor_tr[0]} ({mejor_tr[3]} ms)")

    # Algoritmo general más balanceado
    mejor_general = min(comparacion, key=lambda x: (x[1] + x[2]) / 2)
    print(f"   • Más balanceado: {mejor_general[0]}")

if __name__ == "__main__":
    ejecutar_y_comparar()