import random

def guardarNombreArchivo():
    
    file_name = input("Introduce el nombre del archivo: ")
    file_path = f'C:/Users/marco/OneDrive - Universidad de Burgos/Escritorio/Empresas/Practicas/ProblemasFlowShopPermutacional/{file_name}'
    #file_path = f'C:/Users/pablo/Desktop/Estudios/Universidad/4º/1 cuatri/Org y Gest Empresas/Practica/ProblemasFlowShopPermutacional/{file_name}'


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
    matrizJ = [[0] * len(matriz[0]) for _ in range(len(matriz))]
    tiempoActual=0

    for maquina in range(numMaquinas):
        tiempoActual=0
        for pieza in orden:
            tiempoPiezMaquina = matriz[pieza-1][maquina]
            tiempoActual += tiempoPiezMaquina
            tiempoFinal=tiempoActual
            if maquina>0:
                tiempoFinal= max(tiempoActual,matrizJ[pieza-1][maquina-1])+tiempoPiezMaquina

            matrizJ[pieza-1][maquina]=tiempoFinal

    return matrizJ
        
def busquedaAleatoria(numOrden, numIteraciones, matrizD, numMaquinas):
    matrizSolucion=[]
    mejorValorF=float('inf')

    for i in range(numIteraciones):
        ordenAleatorio=genePermut(numOrden)
        matrizF=devolverMatrizF(ordenAleatorio, matrizD, numMaquinas)
        print("matriz "+str(i))
        for fila in matrizF:
            print(fila)
        matrizFAplanada = [elemento for fila in matrizF for elemento in fila]
        maximoValorMatrizF=max(matrizFAplanada)
        if maximoValorMatrizF<mejorValorF:
            mejorValorF=maximoValorMatrizF
            matrizSolucion=matrizF

        
    return matrizSolucion, mejorValorF


def menuDeModo():

    print("--== Menu de Modos de Ejecucion ==--"
            "    (elige el numero del modo)"
            "1) Modo Aleatorio"
            "2)...")

    op= input("Modo seleccionado: ")

    match op:
        case "1":
            numeroDeIteraciones= input("Introduce el numero de iteraciones: ")
            solucion,mejorValorF=busquedaAleatoria(numOrdenes, int(numeroDeIteraciones), matrizD, numMaquinas)

    #case "2"...:

    return solucion,mejorValorF

    

#----------------------------#
#                            #
#        MAIN PROGRAM        #
#                            #
#----------------------------#

numOrdenes,numMaquinas,matrizD=guardarValoresArchivo()
orden=genePermut(numOrdenes)

print ("Matriz D")
for fila in matrizD:
    print(fila)
    
matrizF=devolverMatrizF(orden,matrizD, numMaquinas)

print ("Orden")
print(orden)

print ("Matriz J")
for fila in matrizF:
    print(fila)

solucion, mejorValorF = menuDeModo()

print ("SOLUCION")
for fila in solucion: 
    print(fila)
print(mejorValorF)