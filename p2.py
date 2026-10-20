"""
Práctica 2: Algoritmos codiciosos.
Algoritmia y Estructuras de Datos Avanzadas.
Curso 2026-27.
"""

from typing import List, Tuple, Dict, Optional
import random

# =============================================================================
# I. Problema del cambio de monedas
# =============================================================================

def greedy_change(coins: List[int], amount: int) -> Tuple[List[int], int]:
    """
    Estrategia codiciosa para el problema del cambio de monedas.
    Selecciona en cada paso la moneda de mayor valor que no supere la cantidad restante.
    """
    sorted_coins = sorted(coins, reverse=True)
    selected = []
    remainder = amount
    
    for coin in sorted_coins:
        while remainder >= coin:
            remainder -= coin
            selected.append(coin)
            
    return selected, remainder

def optimal_change(coins: List[int], amount: int) -> Optional[List[int]]:
    """
    Solución óptima mediante programación dinámica para el problema del cambio de monedas.
    Determina el menor número de monedas necesario para obtener la cantidad objetivo.
    """
    if amount == 0:
        return []
    
    dp = [float('inf')] * (amount + 1)
    parent_coin = [0] * (amount + 1)
    dp[0] = 0
    
    for a in range(1, amount + 1):
        for coin in coins:
            if a >= coin and dp[a - coin] + 1 < dp[a]:
                dp[a] = dp[a - coin] + 1
                parent_coin[a] = coin
                
    if dp[amount] == float('inf'):
        return None
    
    current_amount = amount
    result = []
    while current_amount > 0:
        c = parent_coin[current_amount]
        result.append(c)
        current_amount -= c
        
    return result

def compare_change(coins: List[int], max_amount: int) -> Dict[str, List[int]]:
    """
    Evalúa todas las cantidades entre 1 y max_amount, clasifica cada cantidad en
    'optimal', 'suboptimal', 'greedy_failed' o 'impossible'.
    """
    result = {
        "optimal": [],
        "suboptimal": [],
        "greedy_failed": [],
        "impossible": []
    }
    
    for a in range(1, max_amount + 1):
        g_selected, g_rem = greedy_change(coins, a)
        opt_selected = optimal_change(coins, a)
        
        if opt_selected is None:
            result["impossible"].append(a)
        else:
            if g_rem == 0:
                if len(g_selected) == len(opt_selected):
                    result["optimal"].append(a)
                else:
                    result["suboptimal"].append(a)
            else:
                result["greedy_failed"].append(a)
                
    return result

# =============================================================================
# II. Selección de actividades
# =============================================================================

def activity_selection(activities: List[Tuple[str, int, int]]) -> List[Tuple[str, int, int]]:
    """
    Selecciona el máximo número posible de actividades compatibles.
    Ordena por tiempo de finalización ascendente, y en caso de empate por inicio e identificador.
    """
    sorted_activities = sorted(activities, key=lambda x: (x[2], x[1], x[0]))
    
    selected = []
    last_end = -1
    
    for act in sorted_activities:
        identifier, start, end = act
        if start >= last_end:
            selected.append(act)
            last_end = end
            
    return selected

def generate_activities(n: int, seed: int = 42) -> List[Tuple[str, int, int]]:
    """
    Genera n actividades aleatorias reproducibles.
    start en [0, 10000], duration en [1, 100], end = start + duration.
    """
    random.seed(seed)
    activities = []
    for i in range(n):
        start = random.randint(0, 10000)
        duration = random.randint(1, 100)
        end = start + duration
        identifier = f"A{i}"
        activities.append((identifier, start, end))
    return activities

# =============================================================================
# III. Planificación de tareas con fechas límite
# =============================================================================

def job_scheduling(jobs: List[Tuple[str, int, int]]) -> Tuple[List[Optional[Tuple[str, int, int]]], int]:
    """
    Planificación de tareas de duración unitaria con fecha límite (deadline).
    Devuelve la secuencia de tareas asignadas (con None para intervalos vacíos) y el beneficio total.
    """
    if not jobs:
        return [], 0
    
    sorted_jobs = sorted(jobs, key=lambda x: (-x[1], x[2], x[0]))
    
    max_deadline = max(job[2] for job in sorted_jobs)
    schedule: List[Optional[Tuple[str, int, int]]] = [None] * max_deadline
    total_profit = 0
    
    for job in sorted_jobs:
        _, profit, deadline = job
        slot = min(deadline, max_deadline) - 1
        while slot >= 0:
            if schedule[slot] is None:
                schedule[slot] = job
                total_profit += profit
                break
            slot -= 1
            
    return schedule, total_profit

def generate_jobs(n: int, seed: int = 42) -> List[Tuple[str, int, int]]:
    """
    Genera n tareas aleatorias con fecha límite reproducibles.
    profit en [1, 1000], deadline en [1, max(1, n // 10)].
    """
    random.seed(seed)
    jobs = []
    max_d = max(1, n // 10)
    for i in range(n):
        profit = random.randint(1, 1000)
        deadline = random.randint(1, max_d)
        identifier = f"J{i}"
        jobs.append((identifier, profit, deadline))
    return jobs