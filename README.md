# Análisis Cola M/M/1/K/∞

Se realizo análisis describe un sistema de colas bajo la notación de Kendall **M/M/1/K/∞**, donde:
- El primer **M** indica que los tiempos entre llegadas siguen una distribución exponencial (proceso de Poisson con tasa $\lambda$).
- El segundo **M** señala que los tiempos de servicio también son exponenciales (con tasa $\mu$).
- El número **1** corresponde a la existencia de un único servidor.

## ## Calculo de NS, TS y Nw

- **λ**: tasa promedio de llegadas.
- **μ**: tasa promedio de servicio.
- **ρ = λ/μ**: coeficiente de utilización o intensidad de tráfico.
- **Nₛ**: valor esperado de clientes en todo el sistema.
- **Tₛ**: tiempo promedio de permanencia en el sistema.
- **N𝑤**: número medio de clientes únicamente en la cola.
- **T𝑤**: tiempo medio de espera en la cola.

### Probabilidades de estado
En esta primera etapa se determinan las **probabilidades de estado** *Pn*​, que representan la probabilidad de que en el sistema haya exactamente *n* clientes (ya sea esperando en la cola o siendo atendidos).

La expresión matemática es:

Cuando el valor de p es distinto de 1 la distribución de probabilidades de estado es: 

$$
P_0 = \frac{1 - \rho}{1 - \rho^{K+1}}
$$

$$
P_n = \frac{(1 - \rho)\rho^n}{1 - \rho^{K+1}}, \quad n = 0, 1, ..., K
$$

$$
P_K = \frac{(1 - \rho)\rho^K}{1 - \rho^{K+1}}
$$

En el caso límite  de cuando  es**ρ = 1**  la distribución de probabilidades de estado es: 

$$
P_n = \frac{1}{K + 1}, \quad n = 0, 1, ..., K
$$
## Número esperado de clientes en el sistema (*Ns*)
Este valor representa la **cantidad promedio de clientes que se encuentran dentro del sistema** (tanto en servicio como esperando en la cola). Su cálculo es importante porque brinda una medida del nivel de congestión: a mayor *Ns*​, mayor es la saturación del sistema. Además, esta métrica sirve como base para determinar el tiempo promedio en el sistema mediante la Ley de Little.

$$
N_s = \frac{\rho[1 - (K+1)\rho^K + K\rho^{K+1}]}{(1-\rho)(1-\rho^{K+1})}
$$

## Tiempo promedio en el sistema (Ts)

En esta etapa se determina el **tiempo promedio en el sistema** *Ts*​, que cuantifica el tiempo total que un cliente pasa en el sistema desde su llegada hasta su salida, considerando tanto el tiempo de espera en la cola como el tiempo de servicio recibido.

La expresión matemática que relaciona este tiempo con el número promedio de clientes en el sistema es:
$$
T_s = \frac{N_s}{\lambda(1 - P_K)}
$$
## Número esperado de clientes en cola (Nw)
Esta métrica mide el **promedio de clientes que se encuentran esperando su turno sin ser atendidos**. Se obtiene restando del número esperado de clientes en el sistema aquellos que están en servicio (cuando el servidor está ocupado). El valor de *Nw*​ permite analizar el nivel de congestión exclusivamente en la cola, lo cual es crucial para evaluar la comodidad de los usuarios y la eficiencia del sistema.
$$
N_w = N_s - (1 - P_0)
$$
$$
P_0 = \frac{1 - \rho}{1 - \rho^{K+1}}
$$
## Tiempo promedio de espera en cola (Tw)
El tiempo promedio en la cola corresponde al **tiempo que un cliente debe esperar antes de recibir servicio**. Se calcula dividiendo el número esperado de clientes en la cola *Nw*​ entre la tasa efectiva de llegada *λe*​. Esta métrica es fundamental porque refleja la **experiencia directa del cliente con respecto a la espera**, y suele ser uno de los indicadores más relevantes al evaluar la calidad del servicio.
$$
T_w = \frac{N_q}{\lambda_e}
$$
# Simulaciones

## Resultados Teoricos

### 1: ρ = 0.3 

- $\lambda = 0.3$
- $\mu = 1.0$
- $\rho = \lambda / \mu = 0.3$
#### Resultados: 
$$
N_s = \frac{\rho}{1 - \rho} = \frac{0.3}{0.7} = 0.4286
$$
$$
T_s = \frac{1}{\mu - \lambda} = \frac{1}{0.7} = 1.4286
$$
$$
N_w = \frac{\rho^2}{1 - \rho} = \frac{0.09}{0.7} = 0.1286
$$
$$
T_w = \frac{\rho}{\mu - \lambda} = \frac{0.3}{0.7} = 0.4286
$$

---

## 2: ρ = 0.7 

 - $\lambda = 0.7$
- $\mu = 1.0$
- $\rho = \lambda / \mu = 0.7$
#### Resultados: 
$$
N_s = \frac{\rho}{1 - \rho} = \frac{0.7}{0.3} = 2.3333
$$
$$
T_s = \frac{1}{\mu - \lambda} = \frac{1}{0.3} = 3.3333
$$
$$
N_w = \frac{\rho^2}{1 - \rho} = \frac{0.49}{0.3} = 1.6333
$$
$$
T_w = \frac{\rho}{\mu - \lambda} = \frac{0.7}{0.3} = 2.3333
$$

---

## 3: ρ= 0.9 

 - $\lambda = 0.9$
- $\mu = 1.0$
- $\rho = \lambda / \mu = 0.9$
#### Resultados: 
$$
N_s = \frac{\rho}{1 - \rho} = \frac{0.9}{0.1} = 9.0
$$

$$
T_s = \frac{1}{\mu - \lambda} = \frac{1}{0.1} = 10.0
$$

$$
N_w = \frac{\rho^2}{1 - \rho} = \frac{0.81}{0.1} = 8.1
$$

$$
T_w = \frac{\rho}{\mu - \lambda} = \frac{0.9}{0.1} = 9.0
$$
## Resultados del modelo computacional (Ntelogo)
# Comparación: Resultados Teóricos vs Simulación

## Métricas Comparadas
- **Nw**: Número promedio en cola
- **Tw**: Tiempo promedio en cola  
- **Ns**: Número promedio en sistema
- **Ts**: Tiempo promedio en sistema
- **Utilización**: Porcentaje de uso del servidor

---

## Caso 1: ρ = 0.3

| Métrica | Teórico | Simulación | Diferencia | Error Relativo (%) |
|---------|---------|------------|------------|-------------------|
| **Nw** | 0.1286 | 0.129 | +0.0004 | 0.31% |
| **Tw** | 0.4286 | 0.429 | +0.0004 | 0.09% |
| **Ns** | 0.4286 | - | - | - |
| **Ts** | 1.4286 | 1.429 | +0.0004 | 0.03% |
| **Utilización** | 30.0% | 30.0% | 0.0% | 0.00% |

**Análisis**: Error mínimo (<0.5%), simulación muy precisa.

---

## Caso 2: ρ = 0.7

| Métrica | Teórico | Simulación | Diferencia | Error Relativo (%) |
|---------|---------|------------|------------|-------------------|
| **Nw** | 1.6333 | 1.626 | -0.0073 | 0.45% |
| **Tw** | 2.3333 | 2.32 | -0.0133 | 0.57% |
| **Ns** | 2.3333 | - | - | - |
| **Ts** | 3.3333 | 3.32 | -0.0133 | 0.40% |
| **Utilización** | 70.0% | 70.023% | +0.023% | 0.03% |

**Análisis**: Error muy bajo (<0.6%), simulación confiable.

---

## Caso 3: ρ = 0.9

| Métrica | Teórico | Simulación | Diferencia | Error Relativo (%) |
|---------|---------|------------|------------|-------------------|
| **Nw** | 8.1 | 7.831 | -0.269 | 3.32% |
| **Tw** | 9.0 | 8.718 | -0.282 | 3.13% |
| **Ns** | 9.0 | - | - | - |
| **Ts** | 10.0 | 9.717 | -0.283 | 2.83% |
| **Utilización** | 90.0% | 89.744% | -0.256% | 0.28% |

**Análisis**: Error moderado (2.8-3.3%), típico en alta carga por variabilidad estocástica.

---

## Resumen General

| Carga ρ | Error Promedio | Observaciones |
|---------|----------------|---------------|
| **0.3** | 0.11% | Excelente precisión |
| **0.7** | 0.36% | Muy buena aproximación |
| **0.9** | 2.39% | Error aceptable dada la alta carga |

**Conclusión**: La simulación reproduce fielmente el comportamiento teórico del modelo M/M/1, con errores que aumentan moderadamente bajo alta carga, como era de esperarse.
