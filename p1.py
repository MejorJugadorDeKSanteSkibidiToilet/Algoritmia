import time # Para la función time_measure. Entender código dado.
#import matplotlib.pyplot as plt # Para imprimir gráficas. Entender código dado.
import random # Puede usarse random.randint(n, m) para generar listas aleatorias de enteros en las funciones dataprep.
#cambiar para probar
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

print(f"find duplicates: {find_duplicates( lst = [1,3,5,1,2,5,6,7])}")
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

print(f"has sum pair: {has_sum_pair(([1,1,4,5,3,1,3,5,6, 7], 5))}")

def dataprep_sum_pair_hit(n):
    """Genera un caso donde SÍ existe un par que suma target.
    Devuelve una tupla (lista, target)
    """
    lst = [random.randint(1, 100) for _ in range(n)]
    nums = random.sample(lst, 2)
    return (lst, nums[0]+nums[1])
    pass 
print(f"dataprep sum pair hit: {dataprep_sum_pair_hit(N)}")
def dataprep_sum_pair_miss(n):
    """Genera un caso donde NO existe ningún par (Caso peor).
    Devuelve una tupla (lista, target)
    """
    lst = [random.randint(1, 100) for _ in range(n)]
    rand = random.randint(1,100)
    while has_sum_pair((lst,rand)) is True:
        rand = random.randint(1,100)
    return (lst, rand)
    pass
print(f"dataprep sum pair miss: {dataprep_sum_pair_miss(N)}")
def dataprep_rle(n):
    """Genera una lista con rachas repetidas de dimensión n.
    Devuelve una lista.
    """
    lst = []
    types = ['A', 'B', 'C', 'D'] 
    """He puesto esto pq ni idea de que poner^"""
    
    while len(lst) < n:
        rand = random.choice(types)
        # Longitud de la racha (cuidando no pasarnos de n)
        largo_racha = random.randint(1, min(10, n - len(lst))) 
        lst.extend([rand] * largo_racha)
        
    return lst
    pass
print(f"dataprep_rle (Ni idea de si esto sirve): {dataprep_rle(N)}")
# I.B.1 RLE Naive / Ingenuo
def rle_encode_naive(lst):
    """Codificación RLE utilizando operador + concatenador de listas."""
    
    pass

# I.B.2 RLE Optimized / Óptimo
def rle_encode_optimized(lst):
    """Codificación RLE optimizada usando append in-place."""
    pass

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
