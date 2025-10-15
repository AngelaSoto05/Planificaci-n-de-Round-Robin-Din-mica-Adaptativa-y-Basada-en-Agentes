import statistics

class AgentePlanificacion:
    def __init__(self, procesos, A=10, B=5):
        self.procesos = [p.copy() for p in procesos]
        self.A = A
        self.B = B
        self.registro_quantum = []
        self.registro_agente = []
        for p in self.procesos:
            p["rafaga_restante"] = p["burst"]
            p["tiempo_completado"] = None
            p["tiempo_respuesta"] = None  # 🆕 Seguimiento del tiempo de respuesta

    def calcular_prioridad(self, proceso):
        return self.A * proceso["burst"] + self.B * proceso["priority"]

    def calcular_quantum_tiempo_dinamico(self):
        listos = [p["rafaga_restante"] for p in self.procesos if p["rafaga_restante"] > 0]
        return int(statistics.median(listos)) if listos else 1

    def ordenar_procesos_por_prioridad(self, procesos_listos):
        return sorted(procesos_listos, key=lambda p: self.calcular_prioridad(p))

    def ejecutar(self):
        tiempo = 0
        ciclo = 0
        linea_tiempo = []
        completados = []

        while any(p["rafaga_restante"] > 0 for p in self.procesos):
            procesos_listos = [p for p in self.procesos if p["arrival"] <= tiempo and p["rafaga_restante"] > 0]
            if not procesos_listos:
                tiempo += 1
                continue

            quantum_dinamico = self.calcular_quantum_tiempo_dinamico()
            ordenados = self.ordenar_procesos_por_prioridad(procesos_listos)

            self.registro_quantum.append((tiempo, quantum_dinamico))
            self.registro_agente.append({
                "ciclo": ciclo,
                "tiempo_inicio": tiempo,
                "dtq": quantum_dinamico,
                "pids_ordenados": [p["pid"] for p in ordenados]
            })
            ciclo += 1

            for p in ordenados:
                if p["arrival"] > tiempo or p["rafaga_restante"] == 0:
                    continue

                # 🆕 Establecer tiempo de respuesta solo en la primera ejecución
                if p["tiempo_respuesta"] is None:
                    p["tiempo_respuesta"] = tiempo - p["arrival"]

                tiempo_ejecucion = min(p["rafaga_restante"], quantum_dinamico)
                linea_tiempo.append({"pid": p["pid"], "inicio": tiempo, "fin": tiempo + tiempo_ejecucion})
                tiempo += tiempo_ejecucion
                p["rafaga_restante"] -= tiempo_ejecucion

                if p["rafaga_restante"] == 0:
                    p["tiempo_completado"] = tiempo
                    completados.append({
                        "pid": p["pid"],
                        "tiempo_final": tiempo,
                        "llegada": p["arrival"],
                        "burst": p["burst"],
                        "completado": p["tiempo_completado"],
                        "tat": p["tiempo_completado"] - p["arrival"],
                        "wt": p["tiempo_completado"] - p["arrival"] - p["burst"],
                        "rt": p["tiempo_respuesta"]  # ✅ Agregar tiempo de respuesta
                    })

                break  # ejecutar 1 proceso por ciclo como Round-Robin

        return linea_tiempo, completados, self.registro_quantum, self.registro_agente