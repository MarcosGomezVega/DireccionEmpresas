import random
import math

def guardarNombreArchivo():
    
    file_name = input("Introduce el nombre del archivo: ")

    file_path = f'C:/Users/marco/OneDrive - Universidad de Burgos/Escritorio/Empresas/Practicas/PracticaPrgramacion/ProblemasFlowShopPermutacional/{file_name}'
    #file_path = f'C:/Users/pablo/Desktop/Estudios/Universidad/4º/1 cuatri/Org y Gest Empresas/Practica/ProblemasFlowShopPermutacional/{file_name}'
    #file_path = f'C:/Users/marco/OneDrive - Universidad de Burgos/Escritorio/Empresas/Practicas/ProblemasFlowShopPermutacional/ejem_clase1.txt'

    return file_path

def guardarValoresArchivo():
    
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
    matrizSolucion=[]
    mejorValorF=float('inf')

    for i in range(numIteraciones):
        ordenAleatorio=genePermut(numOrden)
        matrizF=devolverMatrizF(ordenAleatorio, matrizD, numMaquinas)
        maximoValorMatrizF=fMax(matrizF)
        mediaUltimaColumna = fMed( matrizF,numOrden)
        if maximoValorMatrizF<mejorValorF:
            mejorValorF=maximoValorMatrizF
            matrizSolucion=matrizF

        
    return matrizSolucion, mejorValorF, ordenAleatorio

def primerMejor(ordenBueno, matrizFBuena,solucionFinal):

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
    tamPoblacion=50
    probMutacion=1
    probCruzamiento=10
    poblacionConFmax=[]
    mejorSolucionFmax=float('inf')
    solucionFmax=mejorSolucionFmax

    #Generar poblacion inicial
    poblacion = [genePermut(numOrdenes) for _ in range(tamPoblacion)]
    for orden in poblacion:
            matrizF = devolverMatrizF(orden, matrizD, numMaquinas)
            poblacionConFmax.append((orden, fMax(matrizF)))
    #Ordenar la poblacion por el valor de la funcion objetivo
    poblacionConFmax.sort(key=lambda x: x[1])
    mejorSolucionFmax=poblacionConFmax[0][1]



    while solucionFmax > mejorSolucionFmax:
        #Calcular el valor de la funcion objetivo para cada individuo
        for orden in poblacion:
            matrizF = devolverMatrizF(orden, matrizD, numMaquinas)
            poblacionConFmax.append((orden, fMax(matrizF)))
        #Ordenar la poblacion por el valor de la funcion objetivo
        poblacionConFmax.sort(key=lambda x: x[1])
        #Seleccionar los individuos de la poblacion
        poblacionSelecionada = seleccionTorneoAleatorio(poblacionConFmax)
        #Cruzamiento
        poblacionHijos=[]
        for _ in range((tamPoblacion//2)):
            padre1=random.choice(poblacionSelecionada)
            padre2=random.choice(poblacionSelecionada)
            if random.randint(0,100) < probCruzamiento:
                hijo1, hijo2 = cruzamientoPMX(padre1[0], padre2[0])
                poblacionHijos.append(hijo1)
                poblacionHijos.append(hijo2)
            else:
                poblacionHijos.append(padre1[0])
                poblacionHijos.append(padre2[0])
        #Mutacion
        poblacionMutada=[0 for _ in range(tamPoblacion)]
        for i in range(tamPoblacion):
            if random.randint(0,100) < probMutacion:
                poblacionMutada[i] = mutacion(poblacionHijos[i])
            else:
                poblacionMutada[i] = poblacionHijos[i]
            
        #MIRAR SI ESTA BIEN HECHO !!!!!!!!!

        mejorPoblacionInicial=poblacionConFmax[0]

        #Actualizar la poblacion
        for i in range(len(poblacionMutada)):
            poblacion[i] = poblacionMutada[i]
        #Actualizar la mejor poblacion
        poblacion.append(mejorPoblacionInicial)

        #Actualizar el mejor valor de la funcion objetivo
        mejorSolucionFmax = mejorPoblacionInicial[1]

        
        for orden in poblacion:
            matrizF = devolverMatrizF(orden, matrizD, numMaquinas)
            poblacionConFmax.append((orden, fMax(matrizF)))
         #Ordenar la poblacion por el valor de la funcion objetivo
        poblacionConFmax.sort(key=lambda x: x[1])
        solucionFmax=poblacionConFmax[0][1]

    pass

def mutacion(orden):
    i, j = random.sample(range(len(orden)), 2)
    orden[i], orden[j] = orden[j], orden[i]

    return orden
    
def cruzamientoPMX(p1, p2):

    
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

    diferencia = puntoCorte2 - puntoCorte
    listaPuntoCorteHijo1 = [0 for _ in range(diferencia)]
    listaPuntoCorteHijo2 = [0 for _ in range(diferencia)]
    for i in range(puntoCorte, puntoCorte2):
        listaPuntoCorteHijo1[i-puntoCorte] = p2[i]
        listaPuntoCorteHijo2[i-puntoCorte] = p1[i]
    for i in range(len(p1)):
        if puntoCorte <= i < puntoCorte2:
            hijo1[i] = listaPuntoCorteHijo1[i-puntoCorte]
            hijo2[i] = listaPuntoCorteHijo2[i-puntoCorte]
        else:
           
            if p1[i] in listaPuntoCorteHijo1:
                indice=listaPuntoCorteHijo1.index(p1[i])
                hijo1[i]=listaPuntoCorteHijo2[indice]
            else:
                hijo1[i]=p1[i]
            if p2[i] in listaPuntoCorteHijo2:
                indice=listaPuntoCorteHijo2.index(p2[i])
                hijo2[i]=listaPuntoCorteHijo1[indice]
            else:
                hijo2[i]=p2[i]
                
            

    return hijo1, hijo2
    
def seleccionTorneoAleatorio(poblacion):
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

    maximo=max(row[-1] for row in matriz)

    return maximo

def fMed(matriz, numOrden):

    promedio = sum(row[-1] for row in matriz) / numOrden

    return promedio

def menuDeModo():

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
