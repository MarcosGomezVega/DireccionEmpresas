import random
import math

def guardarNombreArchivo():
    """
    Solicita al usuario el nombre del archivo y construye la ruta completa.

    Returns:
        str: La ruta completa del archivo.
    """
    file_name = input("Introduce el nombre del archivo: ")

    file_path = f'./ProblemasFlowShopPermutacional/{file_name}'
   
    return file_path

def guardarValoresArchivo():
    """
    Lee el contenido del archivo y extrae los valores necesarios.

    Returns:
        tuple: Número de órdenes, número de máquinas y la matriz de tiempos procesada.
    """
    with open(guardarNombreArchivo(), 'r', encoding='utf-8') as file:
        content = file.read()

    lines = content.splitlines()

    first_line = lines[0].split()

    numOrdenes = int(first_line[0])
    numMaquinas = int(first_line[1])

    matriz = []

    for line in lines[1:]:
        fila = [int(x) for x in line.split()]
        matriz.append(fila)

    matrizBuena = []
    for fila in matriz:
        fila_pares = [fila[i] for i in range(len(fila)) if i % 2 != 0]
        matrizBuena.append(fila_pares)

    return numOrdenes,numMaquinas,matrizBuena

def genePermut (numOrdenes):
    """
    Genera una permutación aleatoria de las órdenes.

    Args:
        numOrdenes (int): Número de órdenes.

    Returns:
        list: Lista con una permutación aleatoria de las órdenes.
    """
    permut=[]
    listaOrdenes=[]
    
    for i in range(1,numOrdenes+1):
        listaOrdenes.append(i)

    while listaOrdenes:
        aleatorio = random.choice(listaOrdenes)
        permut.append(aleatorio)
        listaOrdenes.remove(aleatorio)
    
    return permut

def devolverMatrizF ( orden, matriz, numMaquinas ):
    """
    Calcula la matriz de tiempos de finalización (matriz F) para un orden dado de las órdenes.

    Args:
        orden (list): Lista con el orden de las órdenes.
        matriz (list): Matriz de tiempos de procesamiento.
        numMaquinas (int): Número de máquinas.

    Returns:
        list: Matriz de tiempos de finalización.
    """    
    matrizF = [[0] * len(matriz[0]) for _ in range(len(matriz))]

    for maquina in range(numMaquinas):
        for idx, pieza in enumerate(orden):
            pieza=pieza-1
            if maquina==0:
                if idx == 0:
                    matrizF[pieza][maquina] = matriz[pieza][maquina]
                else:
                    matrizF[pieza][maquina] = matrizF[orden[idx - 1]-1][maquina] + matriz[pieza][maquina]
            else:
                if idx == 0:
                    matrizF[pieza][maquina] = matrizF[pieza][maquina-1] + matriz[pieza][maquina]
                else:
                    x=matrizF[pieza][maquina-1]
                    y= matrizF[orden[idx - 1]-1][maquina]
                    matrizF[pieza][maquina] = max(x,y) + matriz[pieza][maquina]

    return matrizF
        
def busquedaAleatoria(numOrden, numIteraciones, matrizD, numMaquinas):
    """
    Realiza una búsqueda aleatoria para encontrar una solución al problema de secuenciación de órdenes.

    Args:
        numOrden (int): Número de órdenes.
        numIteraciones (int): Número de iteraciones a realizar.
        matrizD (list): Matriz de tiempos de procesamiento.
        numMaquinas (int): Número de máquinas.

    Returns:
        tuple: Matriz de tiempos de finalización de la mejor solución, el mejor valor de la función objetivo y el orden de las órdenes correspondiente.
    """
    matrizSolucion=[]
    mejorValorF=float('inf')

    for i in range(numIteraciones):
        ordenAleatorio=genePermut(numOrden)
        matrizF=devolverMatrizF(ordenAleatorio, matrizD, numMaquinas)
        maximoValorMatrizF=fMax(matrizF)
        #mediaUltimaColumna = fMed( matrizF,numOrden)
        if maximoValorMatrizF<mejorValorF:
            mejorValorF=maximoValorMatrizF
            matrizSolucion=matrizF

        
    return matrizSolucion, mejorValorF, ordenAleatorio

def primerMejor(ordenBueno, matrizFBuena,solucionFinal):
    """
    Realiza una búsqueda local para encontrar una mejor solución al problema de secuenciación de órdenes.

    Args:
        ordenBueno (list): Lista con el orden actual de las órdenes.
        matrizFBuena (list): Matriz de tiempos de finalización actual.
        solucionFinal (float): Valor de la función objetivo de la solución actual.

    Returns:
        tuple: El mejor orden de las órdenes, la mejor matriz de tiempos de finalización y el mejor valor de la función objetivo.
    """
    for i in range(len(ordenBueno)):
        for j in range(i+1,len(ordenBueno)):
            ordenPrimos=ordenBueno.copy()
            ordenPrimos[i],ordenPrimos[j]=ordenPrimos[j],ordenPrimos[i]
            matrizFPrimo=devolverMatrizF(ordenPrimos, matrizD, numMaquinas)
            maximoPrimo=fMax(matrizFPrimo)
            if solucionFinal > maximoPrimo:
                ordenBueno=ordenPrimos
                matrizFBuena=matrizFPrimo
                solucionFinal=maximoPrimo
                return ordenBueno, matrizFBuena, solucionFinal
            
    return ordenBueno, matrizFBuena, solucionFinal

def busquedaLocal(numOrdenes, matrizD, numMaquinas):
    """
    Realiza una búsqueda local para encontrar una mejor solución al problema de secuenciación de órdenes.

    Args:
        numOrdenes (int): Número de órdenes.
        matrizD (list): Matriz de tiempos de procesamiento.
        numMaquinas (int): Número de máquinas.

    Returns:
        tuple: La mejor matriz de tiempos de finalización, el mejor valor de la función objetivo y el mejor orden de las órdenes.
    """
    solucionFinal=float('inf')
    ordenBueno=genePermut(numOrdenes)
    matrizFBuena=devolverMatrizF(ordenBueno, matrizD, numMaquinas)
    solucionFinal=fMax(matrizFBuena)  
 
    
    while True:
        ordenBueno, matrizFBuena, solucionPrimo=primerMejor(ordenBueno, matrizFBuena,solucionFinal)
        if solucionFinal == solucionPrimo:
            return matrizFBuena, solucionFinal, ordenBueno
        else:
            solucionFinal=solucionPrimo
    
def recocidoSimulado(numOrdenes, matrizD, numMaquinas):
    """
    Realiza una búsqueda de solución utilizando el algoritmo de recocido simulado.

    Args:
        numOrdenes (int): Número de órdenes.
        matrizD (list): Matriz de tiempos de procesamiento.
        numMaquinas (int): Número de máquinas.

    Returns:
        tuple: La mejor matriz de tiempos de finalización, el mejor valor de la función objetivo y el mejor orden de las órdenes.
    """    
    ordenInicial = genePermut(numOrdenes)
    matrizFBuena = devolverMatrizF(ordenInicial, matrizD, numMaquinas)
    solucionActual = fMax(matrizFBuena)
    mejorSolucion = solucionActual
    mejorOrden = ordenInicial
    T = solucionActual*0.35  # Temperatura inicial
    T_min = 0.01  # Temperatura mínima
    alpha = 0.9  # Factor de enfriamiento
    L = 100  # Número de iteraciones en cada temperatura

    while T > T_min:
        for _ in range(L):
            # Generar una nueva solución vecina
            nuevaOrden = ordenInicial[:]
            i, j = random.sample(range(numOrdenes), 2)
            nuevaOrden[i], nuevaOrden[j] = nuevaOrden[j], nuevaOrden[i]
            
            # Calcular la nueva matriz y el valor de la función objetivo
            matrizFVecina = devolverMatrizF(nuevaOrden, matrizD, numMaquinas)
            solucionVecina = fMax(matrizFVecina)
            
            # Calcular la diferencia de costo
            delta_E = solucionVecina - solucionActual
            
            # Aceptar la nueva solución
            if delta_E < 0 or random.uniform(0, 1) < math.exp(-delta_E / T):
                ordenInicial = nuevaOrden
                solucionActual = solucionVecina
                matrizFBuena = matrizFVecina
                if solucionVecina < mejorSolucion:
                    mejorSolucion = solucionVecina
                    mejorOrden = nuevaOrden
        
        # Enfriar la temperatura
        T *= alpha

    return matrizFBuena, mejorSolucion, mejorOrden

def genetico(numOrdenes, matrizD, numMaquinas):
    """
    Realiza una búsqueda de solución utilizando el algoritmo genético.

    Args:
        numOrdenes (int): Número de órdenes.
        matrizD (list): Matriz de tiempos de procesamiento.
        numMaquinas (int): Número de máquinas.

    Returns:
        tuple: La mejor matriz de tiempos de finalización, el mejor valor de la función objetivo y el mejor orden de las órdenes.
    """    
    tamPoblacion=1000
    probMutacion=1
    probCruzamiento=0.8
    poblacionConFmax=[]
    numMaxGeneraciones=100
    generacion=0

    #Generar poblacion inicial
    poblacion = [genePermut(numOrdenes) for _ in range(tamPoblacion)]
    for orden in poblacion:
            matrizF = devolverMatrizF(orden, matrizD, numMaquinas)
            poblacionConFmax.append((orden, fMax(matrizF)))
    #Ordenar la poblacion por el valor de la funcion objetivo
    poblacionConFmax.sort(key=lambda x: x[1])


    while generacion<numMaxGeneraciones:
        if generacion !=0:
            #Calcular el valor de la funcion objetivo para cada individuo
            for i in range(len(poblacion)):
                matrizF = devolverMatrizF(poblacion[i], matrizD, numMaquinas)
                poblacionConFmax[i]=(poblacion[i], fMax(matrizF))
            #Ordenar la poblacion por el valor de la funcion objetivo
            poblacionConFmax.sort(key=lambda x: x[1])

        #Seleccionar los individuos de la poblacion
        poblacionSelecionada = seleccionTorneoAleatorio(poblacionConFmax)
        
        #Cruzamiento por PMX
        poblacionHijos=[]
        tamanoPoblacionCruce = int(tamPoblacion * probCruzamiento)
        if tamanoPoblacionCruce % 2 != 0:
            tamanoPoblacionCruce+=1
        
        #Cruzamos el 80% de la poblacion
        for i in range(tamanoPoblacionCruce//2):
            padre1=poblacionSelecionada[i]
            i+=1
            padre2=poblacionSelecionada[i]
            
            hijo1, hijo2 = cruzamientoPMX(padre1[0], padre2[0])
            poblacionHijos.append(hijo1)
            poblacionHijos.append(hijo2)
            i+=1
            
        #Mete en hijos el 20% que no se cruza
        for i in range(tamanoPoblacionCruce,tamPoblacion):
            poblacionHijos.append(poblacionSelecionada[i][0])
            
        #Mutacion
        poblacionMutada=[0 for _ in range(tamPoblacion)]
        for i in range(tamPoblacion):
            if random.randint(0,100) < probMutacion:
                poblacionMutada[i] = mutacion(poblacionHijos[i])
            else:
                poblacionMutada[i] = poblacionHijos[i]
            
        mejorPoblacionInicial=poblacionConFmax[0][0]

        #Actualizar la poblacion
        for i in range(len(poblacionMutada)):
            poblacion[i] = poblacionMutada[i]
        

        #Actualizar la mejor poblacion
        if len(poblacion) != tamPoblacion+1:
            poblacion.append(mejorPoblacionInicial)
            poblacionConFmax.append(0)
        elif len(poblacion) == tamPoblacion+1:
            poblacion[tamPoblacion] = mejorPoblacionInicial

        generacion+=1

    solucionOrden=poblacionConFmax[0][0]
    solucionMatrizF=devolverMatrizF(solucionOrden, matrizD, numMaquinas)
    mejorValorF=fMax(solucionMatrizF)

    return solucionMatrizF, mejorValorF, solucionOrden
        
def mutacion(orden):
    """
    Realiza una mutación en el orden de las órdenes.

    Args:
        orden (list): Lista con el orden de las órdenes.

    Returns:
        list: Lista con el orden de las órdenes mutado.
    """
    i=random.randint(0,len(orden)-1)
    j=random.randint(0,len(orden)-1)
    orden[i], orden[j] = orden[j], orden[i]

    return orden
    
def cruzamientoPMX(p1, p2):

    """
    Realiza el cruzamiento PMX (Partially Mapped Crossover) entre dos padres.

    Args:
        p1 (list): Primer padre.
        p2 (list): Segundo padre.

    Returns:
        tuple: Dos listas que representan los hijos generados por el cruzamiento PMX.
    """    
    hijo1 = p1[:]
    hijo2 = p2[:]
    puntoCorte = random.randint(0, len(p1) - 1)
    puntoCorte2 = random.randint(0, len(p2) - 1)

  
    
    if puntoCorte == puntoCorte2:
        if puntoCorte2 == len(p2) - 1:
            puntoCorte2 -= 1
        else:
            puntoCorte2+=1

    if puntoCorte > puntoCorte2:
        puntoEsxtra=puntoCorte2
        puntoCorte2=puntoCorte
        puntoCorte=puntoEsxtra

    #creamos las listas de los puntos de corte
    diferencia = puntoCorte2 - puntoCorte
    listaPuntoCorteHijo1 = [0 for _ in range(diferencia)]
    listaPuntoCorteHijo2 = [0 for _ in range(diferencia)]
    for i in range(puntoCorte, puntoCorte2):
        listaPuntoCorteHijo1[i-puntoCorte] = p2[i]
        listaPuntoCorteHijo2[i-puntoCorte] = p1[i]

    #Creamos la mutacion
    for i in range(len(p1)):
        #miramos si estamos dentro de los puntos de corte
        if puntoCorte <= i < puntoCorte2:
            hijo1[i] = listaPuntoCorteHijo1[i-puntoCorte]
            hijo2[i] = listaPuntoCorteHijo2[i-puntoCorte]
        else:
            #miramos si el valor de p1 esta en la lista de los puntos de corte
            if p1[i] in listaPuntoCorteHijo1:
                indice=listaPuntoCorteHijo1.index(p1[i])
                valorCambiar=listaPuntoCorteHijo2[indice]

                while valorCambiar in listaPuntoCorteHijo1:
                    indice=listaPuntoCorteHijo1.index(valorCambiar)
                    valorCambiar=listaPuntoCorteHijo2[indice]

                hijo1[i]=valorCambiar
            else:
                hijo1[i]=p1[i]
            #miramos si el valor de p2 esta en la lista de los puntos de corte
            if p2[i] in listaPuntoCorteHijo2:
                indice=listaPuntoCorteHijo2.index(p2[i])
                valorCambiar=listaPuntoCorteHijo1[indice]

                while valorCambiar in listaPuntoCorteHijo2:
                    indice=listaPuntoCorteHijo2.index(valorCambiar)
                    valorCambiar=listaPuntoCorteHijo1[indice]

                hijo2[i]=valorCambiar
            else:
                hijo2[i]=p2[i]
                
            

    return hijo1, hijo2
    
def seleccionTorneoAleatorio(poblacion):
    """
    Realiza la selección de individuos mediante el método de torneo aleatorio.

    Args:
        poblacion (list): Lista de individuos con sus valores de función objetivo.

    Returns:
        list: Lista de individuos seleccionados.
    """
    tamPoblacion = len(poblacion)
    seleccionados=[[0]  for _ in range(tamPoblacion)]
    
    for i in range(tamPoblacion):
        selecionado1=random.randint(0, tamPoblacion - 1)
        selecionado2=random.randint(0, tamPoblacion - 1)
        

        if poblacion[selecionado1][1] < poblacion[selecionado2][1]:
            seleccionados[i]=poblacion[selecionado1]
        else:
            seleccionados[i]=poblacion[selecionado2]

    return seleccionados

def fMax(matriz):
    """
    Calcula el valor máximo de la última columna de la matriz.

    Args:
        matriz (list): Matriz de tiempos de finalización.

    Returns:
        int: El valor máximo de la última columna de la matriz.
    """
    maximo=max(row[-1] for row in matriz)

    return maximo

def fMed(matriz, numOrden):
    """
    Calcula el valor promedio de la última columna de la matriz.

    Args:
        matriz (list): Matriz de tiempos de finalización.
        numOrden (int): Número de órdenes.

    Returns:
        float: El valor promedio de la última columna de la matriz.
    """
    promedio = sum(row[-1] for row in matriz) / numOrden

    return promedio

def menuDeModo():
    """
    Muestra el menú de modos de ejecución y solicita al usuario que seleccione uno.

    Returns:
        tuple: La mejor matriz de tiempos de finalización, el mejor valor de la función objetivo y el mejor orden de las órdenes.
    """
    print("--== Menu de Modos de Ejecucion ==-- \n"
            "    (elige el numero del modo)\n"
            "1) Modo Aleatorio\n"
            "2) Modo Busqueda Local - Primer Mejor\n"
            "3) Modo Recocido Simulado\n"
            "4) Modo Algoritmo Genetico\n")

    op= input("Modo seleccionado: ")

    match op:
        case "1":
            numeroDeIteraciones= input("Introduce el numero de iteraciones: ")
            solucion,mejorValorF, ordenFinal=busquedaAleatoria(numOrdenes, int(numeroDeIteraciones), matrizD, numMaquinas)
        case "2":
            solucion,mejorValorF,ordenFinal=busquedaLocal(numOrdenes,matrizD, numMaquinas)
        case "3":
            solucion,mejorValorF,ordenFinal=recocidoSimulado(numOrdenes,matrizD, numMaquinas)
        case "4":
            solucion,mejorValorF,ordenFinal=genetico(numOrdenes,matrizD, numMaquinas)

    return solucion,mejorValorF, ordenFinal

    

#----------------------------#
#                            #
#        MAIN PROGRAM        #
#                            #
#----------------------------#


numOrdenes,numMaquinas,matrizD=guardarValoresArchivo()
orden=genePermut(numOrdenes)
solucion, mejorValorF, ordenFinal = menuDeModo()

print ("\nSOLUCION: ")
for fila in solucion: 
    print(fila)
print("\nMejor Valor: "+str(mejorValorF))
print ("\nOrden Final: "+ str(ordenFinal))
