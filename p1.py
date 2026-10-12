import time # Para la función time_measure. Entender código dado.
import matplotlib.pyplot as plt # Para imprimir gráficas. Entender código dado.
import random # Puede usarse random.randint(n, m) para generar listas aleatorias de enteros en las funciones dataprep.
#cambiar para probar
import numpy as np # Para la libreria numpy
N = 10
# I.A.1 Medición de tiempos de ejecución
def time_measure(f, dataprep, Nlist, Nrep=1000, Nstat=100):
    """Mide la media y varianza del tiempo de ejecución de la función f
    para cada tamaño n presente en Nlist.
    """
    res = []
    for n in Nlist:
        partial = []
        for _ in range(Nstat):
            data = dataprep(n)
            t1 = time.perf_counter()
            for _ in range(Nrep):
                f(data)
            t2 = time.perf_counter()
            t_elem = (t2 - t1) / float(Nrep)
            partial.append(t_elem)

        mean_val = sum(partial) / float(Nstat)
        var_val = sum((x - mean_val) ** 2 for x in partial) / float(Nstat)
        res.append((mean_val, var_val))
    return res

# I.A.2 Búsqueda de duplicados manteniendo orden de aparición
def find_duplicates(lst):
    """Devuelve los elementos que aparecen más de una vez en lst, 
    preservando el orden de su primera repetición y sin duplicados.
    """
    vistos = set()
    lstd = []
    for num in lst:
        if num in vistos:
            if num not in lstd:
                lstd.append(num)
        else:
            vistos.add(num)
            
    return lstd
# I.A.3 Búsqueda de par que suma target con complejidad O(n)
def has_sum_pair(par):
    """Dada una tupla (lst, target), devuelve True si existen dos elementos
    distintos en lst que sumen target; de lo contrario devuelve False.
    """
    lst, target = par
    tried = set()
    for num in lst:
        potentialTarget = target - num
        if potentialTarget in tried:
            return True
        tried.add(num)
    return False


""" Esto funciona pero es O(N²)
    while lst:
        tried = set()
        current = lst[0]
        lst = [item for item in lst if item != current]

        if target in [x + current for x in lst]:
            return True
    
    return False
"""

def dataprep_sum_pair_hit(n):
    """Genera un caso donde SÍ existe un par que suma target.
    Devuelve una tupla (lista, target)
    """
    if n < 2:
        raise ValueError("n debe ser al menos 2")

    lst = [random.randint(1, 100) for _ in range(n)]
    nums = random.sample(lst, 2)
    return (lst, nums[0]+nums[1])
    pass

def dataprep_sum_pair_miss(n):
    """Genera un caso donde NO existe ningún par (Caso peor).
    Devuelve una tupla (lista, target)
    """
    lst = [random.randint(1, 100) for _ in range(n)]
    return (lst, 201)
    pass

def dataprep_rle(n):
    """Genera una lista con rachas repetidas de dimensión n.
    Devuelve una lista.
    """
    lst = []
    types = ['A', 'B', 'C', 'D'] 
    """He puesto esto pq ni idea de que poner^"""
    
    while len(lst) < n:
        rand = random.choice(types)
        largo_racha = random.randint(1, min(10, n - len(lst))) 
        lst.extend([rand] * largo_racha)
        
    return lst
    pass

# I.B.1 RLE Naive / Ingenuo
def rle_encode_naive(lst):
    """Codificación RLE utilizando operador + concatenador de listas."""
    if not lst:
        return []
    
    num = 1
    ret = []

    for i in range(len(lst)-1):
        
        if lst[i] == lst[i+1]:
            num+=1
        else:
            ret = ret + [(lst[i], num)]
            num = 1
    ret = ret + [(lst[-1], num)]
    return ret

    pass

# I.B.2 RLE Optimized / Óptimo
def rle_encode_optimized(lst):
    """Codificación RLE optimizada usando append in-place."""
    if not lst:
        return []

    num = 1
    ret = []
    num2 = lst[0]

    for i in range(len(lst)-1):

        if lst[i+1] == num2:
            num += 1
        else:
            ret.append((num2, num))
            num2 = lst[i+1]
            num = 1
    ret.append((num2, num))
    return ret


def init_cd(n:int):
    """devuelve un array con valores -1 en las posiciones {0, 1, ..., n-1}. """
    a = [-1] * n
    if a is not np.ndarray:
        a = np.array(a)
    return a

def union(rep_1, rep_2, p_cd):
    """devuelve el representante del conjunto obtenido como la unión por rangos de los representados por los índices
    rep_1, rep_2 en el CD almacenado en el array p_cd."""
    if rep_1 == rep_2:
        return rep_1
    
    if p_cd[rep_1] > p_cd[rep_2]:
        temp = rep_1
        rep_1 = rep_2
        rep_2 = temp
    if p_cd[rep_1] == p_cd[rep_2]:
        p_cd[rep_1] -= 1

    p_cd[rep_2] = rep_1
    return rep_1

def find(ind, p_cd):
    """devuelve el representante del índice ind en el CD almacenado en p_cd realizando compresión de caminos."""
    if p_cd[ind] < 0:
        return ind
    p_cd[ind] = find(p_cd[ind], p_cd)
    return p_cd[ind]

def cd_2_dict(p_cd):
    """reciba un CD en el array p_cd y devuelva un diccionario cuyas claves sean los representantes de los
subconjuntos del CD y donde el valor de la clave u del dict sea una lista con los miembros del subconjunto
representado por u , incluyendo, por supuesto el propio u ."""
    output = {}
    for i in range(len(p_cd)):
        rep = find(i, p_cd)
        if rep not in output:
            output[rep] = []
        output[rep].append(i)
    return output

def ccs(n, l):
    """nos devuelva las componentes conexas de un tal grafo. Para ello la función inicializará un CD vacío, examinará las ramas del grafo contenidas en la lista l y si los dos nodos de la rama pertenecen a subconjuntos distintos, unirá estos. Cuando se procesen todas las ramas la función convertirá la tabla que contenga el CD en un dict y devolverá éste"""
    p_cd = init_cd(n)
    for edge in l:
        u, v = edge
        rep_u = find(u, p_cd)
        rep_v = find(v, p_cd)
        if rep_u != rep_v:
            union(rep_u, rep_v, p_cd)
    return cd_2_dict(p_cd)
#probar apartado 1
print(f"find duplicates: {find_duplicates( lst = [1,3,5,1,2,5,6,7])}")
print(f"has sum pair: {has_sum_pair(([1,1,4,5,3,1,3,5,6, 7], 5))}")
print(f"dataprep sum pair hit: {dataprep_sum_pair_hit(N)}")
print(f"dataprep sum pair miss: {dataprep_sum_pair_miss(N)}")
a = dataprep_rle(N)
print(f"dataprep_rle: {a}")
print(f"rle_encode_naive: {rle_encode_naive(a)}")
p_cd = init_cd(7)

#Probar apartado 2
print(f"init_cd: {init_cd(5)}")
p_cd = init_cd(5)
union(find(0, p_cd), find(1, p_cd), p_cd)
print(f"find: {find(0, p_cd)}")
print(f"union: {cd_2_dict(p_cd)}")
print(f"cd_2_dict: {cd_2_dict(p_cd)}")

print(f"ccs: {ccs(5, [(0,1), (1,2), (3,4)])}")

# Función auxiliar para generar una gráfica de una serie de datos.
def plot_single_curve(
    x,
    y,
    title="Gráfica de Datos",
    xlabel="Eje X",
    ylabel="Eje Y",
    label=None,
    style="o-",
    color="b",
    grid=True,
    filename=None,
    figsize=(8, 5),
):
    """Genera y muestra/guarda una gráfica limpia para una única serie de datos."""
    plt.figure(figsize=figsize)  # Crea la figura con el tamaño indicado

    # Dibuja la curva
    plt.plot(x, y, style, color=color, label=label)

    # Personalización básica de ejes y título
    plt.title(title)  # Asigna el título
    plt.xlabel(xlabel)  # Etiqueta X
    plt.ylabel(ylabel)  # Etiqueta Y

    if grid:
        plt.grid(True, linestyle="--", alpha=0.6)

    if label:
        plt.legend(
            loc="best"
        )  # Muestra la leyenda si se definió una etiqueta

    plt.tight_layout()

    # Guarda la gráfica en un fichero si se especifica un nombre
    if filename:
        plt.savefig(
            filename, format=filename.split(".")[-1], dpi=300
        )  #

    plt.show()  # Muestra la figura
