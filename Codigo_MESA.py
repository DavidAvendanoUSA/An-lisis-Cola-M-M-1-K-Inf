"""
M/M/n Queueing Simulation - Python Mesa Version
Adaptado para los casos específicos: ρ = 0.3, 0.7, 0.9
"""

import random
import math
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

class Customer(Agent):
    """Agente que representa un cliente en el sistema de colas"""
    def __init__(self, unique_id, model, arrival_time):
        super().__init__(unique_id, model)
        self.arrival_time = arrival_time
        self.service_start_time = None
        self.is_being_served = False
        self.has_been_served = False

class Server(Agent):
    """Agente que representa un servidor en el sistema"""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.current_customer = None
        self.is_busy = False
        self.service_start_time = None

class MMnQueueModel(Model):
    """Modelo M/M/n de simulación de colas"""
    
    def __init__(self, rho=0.7, mean_service_time=1.0, max_run_time=340000, stats_reset_time=5000):
        """
        rho: factor de utilización (λ/μ)
        mean_service_time: tiempo medio de servicio (1/μ)
        """
        super().__init__()
        self.schedule = RandomActivation(self)
        
        # Calcular lambda basado en rho y mu
        self.mu = 1.0 / mean_service_time  # tasa de servicio
        self.lambda_ = rho * self.mu       # tasa de llegada
        self.rho = rho
        
        self.mean_service_time = mean_service_time
        self.max_run_time = max_run_time
        self.stats_reset_time = stats_reset_time
        self.num_servers = 1  # Modelo M/M/1
        
        # Variables de estado
        self.current_time = 0
        self.next_arrival_time = self.generate_next_arrival()
        self.queue = []
        self.customer_counter = 0
        
        # Estadísticas
        self.total_customers_served = 0
        self.total_queue_time = 0
        self.total_system_time = 0
        self.total_queue_length_sum = 0
        self.total_busy_servers_sum = 0
        self.time_last_event = 0
        
        # Crear servidor único (M/M/1)
        self.server = Server("server_0", self)
        self.schedule.add(self.server)
        self.servers = [self.server]
        
        # Configurar recolección de datos
        self.datacollector = DataCollector(
            model_reporters={
                "avg_queue_length": "avg_queue_length",
                "avg_time_in_queue": "avg_time_in_queue", 
                "avg_time_in_system": "avg_time_in_system",
                "server_utilization": "server_utilization",
                "queue_length": lambda m: len(m.queue),
                "busy_servers": lambda m: 1 if m.server.is_busy else 0,
                "current_time": "current_time"
            }
        )
    
    def generate_next_arrival(self):
        """Genera el tiempo para el próximo arribo"""
        return self.current_time + random.expovariate(self.lambda_)
    
    def generate_service_time(self):
        """Genera el tiempo de servicio"""
        return random.expovariate(self.mu)
    
    @property
    def avg_queue_length(self):
        if self.current_time > 0:
            return self.total_queue_length_sum / self.current_time
        return 0
    
    @property
    def avg_time_in_queue(self):
        if self.total_customers_served > 0:
            return self.total_queue_time / self.total_customers_served
        return 0
    
    @property
    def avg_time_in_system(self):
        if self.total_customers_served > 0:
            return self.total_system_time / self.total_customers_served
        return 0
    
    @property
    def server_utilization(self):
        if self.current_time > 0:
            return (self.total_busy_servers_sum / self.current_time) * 100
        return 0
    
    def step(self):
        """Avanza un paso en la simulación"""
        # Actualizar estadísticas acumulativas
        time_elapsed = self.current_time - self.time_last_event
        self.total_queue_length_sum += len(self.queue) * time_elapsed
        self.total_busy_servers_sum += (1 if self.server.is_busy else 0) * time_elapsed
        self.time_last_event = self.current_time
        
        # Procesar llegadas
        if self.current_time >= self.next_arrival_time and self.current_time < self.max_run_time:
            customer = Customer(f"customer_{self.customer_counter}", self, self.current_time)
            self.customer_counter += 1
            self.schedule.add(customer)
            
            if not self.server.is_busy:
                # Atender inmediatamente
                customer.service_start_time = self.current_time
                customer.is_being_served = True
                self.server.current_customer = customer
                self.server.is_busy = True
                self.server.service_start_time = self.current_time
            else:
                # Poner en cola
                self.queue.append(customer)
            
            self.next_arrival_time = self.generate_next_arrival()
        
        # Procesar servicio
        if self.server.is_busy and self.server.current_customer:
            service_time_elapsed = self.current_time - self.server.service_start_time
            expected_service_time = self.generate_service_time()
            
            if service_time_elapsed >= expected_service_time:
                # Completar servicio
                customer = self.server.current_customer
                customer.is_being_served = False
                customer.has_been_served = True
                
                queue_time = customer.service_start_time - customer.arrival_time
                system_time = self.current_time - customer.arrival_time
                
                self.total_queue_time += queue_time
                self.total_system_time += system_time
                self.total_customers_served += 1
                
                # Liberar servidor
                self.server.current_customer = None
                self.server.is_busy = False
                self.server.service_start_time = None
                
                # Atender siguiente en cola
                if self.queue:
                    next_customer = self.queue.pop(0)
                    next_customer.service_start_time = self.current_time
                    next_customer.is_being_served = True
                    self.server.current_customer = next_customer
                    self.server.is_busy = True
                    self.server.service_start_time = self.current_time
        
        # Avanzar tiempo (incremento más pequeño para mayor precisión)
        self.current_time += 0.01
        
        # Recolectar datos cada 1000 unidades de tiempo
        if int(self.current_time) % 1000 == 0:
            self.datacollector.collect(self)

def run_simulation(rho_value, simulation_name):
    """Ejecuta una simulación para un valor de rho específico"""
    print(f"\n{'='*60}")
    print(f"SIMULACIÓN: {simulation_name} (ρ = {rho_value})")
    print(f"{'='*60}")
    
    model = MMnQueueModel(
        rho=rho_value,
        mean_service_time=1.0,
        max_run_time=340000,  # Similar a tu simulación
        stats_reset_time=5000
    )
    
    # Ejecutar simulación
    for i in range(500000):  # Máximo de pasos
        if model.current_time >= model.max_run_time:
            break
        model.step()
    
    # Resultados de la simulación
    print("=== RESULTADOS DE LA SIMULACIÓN ===")
    print(f"Tiempo final: {model.current_time:.2f}")
    print(f"Clientes atendidos: {model.total_customers_served}")
    print(f"Longitud promedio de cola: {model.avg_queue_length:.3f}")
    print(f"Tiempo promedio en cola: {model.avg_time_in_queue:.3f}")
    print(f"Tiempo promedio en sistema: {model.avg_time_in_system:.3f}")
    print(f"Utilización del servidor: {model.server_utilization:.1f}%")
    
    # Valores teóricos esperados
    print("\n=== VALORES TEÓRICOS ESPERADOS ===")
    if rho_value < 1:
        Ns = rho_value / (1 - rho_value)
        Ts = 1 / (model.mu - model.lambda_)
        Nw = (rho_value ** 2) / (1 - rho_value)
        Tw = rho_value / (model.mu - model.lambda_)
        
        print(f"Nw teórico: {Nw:.3f}")
        print(f"Tw teórico: {Tw:.3f}")
        print(f"Ns teórico: {Ns:.3f}")
        print(f"Ts teórico: {Ts:.3f}")
        print(f"Utilización teórica: {rho_value * 100:.1f}%")
        
        # Calcular errores
        error_Nw = abs(model.avg_queue_length - Nw) / Nw * 100
        error_Tw = abs(model.avg_time_in_queue - Tw) / Tw * 100
        
        print(f"\nError relativo Nw: {error_Nw:.2f}%")
        print(f"Error relativo Tw: {error_Tw:.2f}%")
    
    return model

# Ejecutar las tres simulaciones
if __name__ == "__main__":
    # Tus tres casos específicos
    casos = [
        (0.3, "Carga baja"),
        (0.7, "Carga media"), 
        (0.9, "Carga alta")
    ]
    
    resultados = []
    for rho, nombre in casos:
        model = run_simulation(rho, nombre)
        resultados.append((rho, nombre, model))
    
    print(f"\n{'='*60}")
    print("RESUMEN DE TODAS LAS SIMULACIONES")
    print(f"{'='*60}")