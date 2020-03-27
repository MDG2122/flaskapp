import re
#import tika
#from tika import parser
import pandas as pd
import numpy as np



def buscar3(historico, codigosmateria, metadata, codigosynbombres):
    xx = np.zeros((23, 7))
    x2 = np.zeros((23, 7))
    historico = historico
    metadata = metadata
    codigosynbombres = codigosynbombres
    codigosmateria = codigosmateria
    posicionperiodoactual = -1
    posicionperiodosiguiente = -1
    encontrado = False
    esnota = False
    utlimoperiodo = -1
    llevarcuenta = -1
    fila = -1
    columna = -1

    for i in range(len(historico)):
        if historico[i] == 'Período' and historico[i+1] != 'N':
            utlimoperiodo = i

    for i in range(len(historico)):
        posicionperiodoactual = -1
        posicionperiodosiguiente = -1
        contadorvecesmismoperiodo = 1
        # llevarcuenta=-1
        if historico[i] == 'Período' and historico[i+1] != 'N' and historico[i+1] != llevarcuenta:
            posicionperiodoactual = i
            encontrado = False
            estoyen = i
            llevarcuenta = historico[i+1]
            fila = fila+1
            columna = -1

            # llevarcuenta=historico[i+1]
            # print(str(historico[i-1])+' '+str(historico[i])+' '+str(historico[i+1]))#imprimir
            if posicionperiodoactual != utlimoperiodo:
                while(encontrado == False and estoyen < len(historico)):
                    # estoyen=i
                    if historico[estoyen] == 'Período' and historico[estoyen+1] != historico[i+1]:
                        # print(historico[estoyen+1])
                        # print(historico[i+1])
                        posicionperiodosiguiente = estoyen
                        encontrado = True
                    '''
          elif historico[estoyen]=='Período' and historico[estoyen+1]==historico[i+1]:
            contadorvecesmismoperiodo=contadorvecesmismoperiodo+1
            ...
          '''
                    estoyen = estoyen+1
                # print(posicionperiodoactual)
                # print(posicionperiodosiguiente)
                for j in range(posicionperiodoactual, posicionperiodosiguiente, 1):

                    if historico[j] in codigosmateria or (len(historico[j]) == 7 and (historico[j][0] == 'B' or historico[j][0] == 'F')):
                        columna = columna+1
                        if historico[j] in codigosmateria:
                            # print(historico[j])
                            materia = historico[j]
                            esnota = False
                            posiactual = j

                        else:
                            # print(historico[j])
                            materia = 'Electiva'
                            esnota = False
                            posiactual = j

                        for l in range(len(codigosynbombres)):
                            if materia == codigosynbombres[l][0] and materia != 'Electiva':
                                nombredemat = codigosynbombres[l][1]
                            elif materia == 'Electiva':
                                nombredemat = 'Electiva'
                        # print(nombredemat)

                        for y in range(len(metadata)):
                            if nombredemat == metadata.iloc[y][0]:
                                xx[fila][columna] = (y + 1)
                                #xx[fila][columna] = y+1
                        # columna=columna+1
                        # print(columna)

                        while(esnota == False and posiactual < len(historico)):
                            # posiactual=j
                            if (historico[posiactual].isdigit() and len(historico[posiactual]) <= 2) or (historico[posiactual] == 'SOB' or historico[posiactual] == 'SOBR' or
                                                                                                         historico[posiactual] == 'APRO' or historico[posiactual] == 'CONT' or
                                                                                                         historico[posiactual] == 'REPR' or historico[posiactual] == 'NOT'):

                                if historico[posiactual].isdigit() and len(historico[posiactual]) <= 2:
                                    # print(historico[posiactual])
                                    nota = historico[posiactual]
                                    esnota = True
                                    x2[fila][columna] = nota

                                    #print(str(materia)+' '+str(nota))
                                elif historico[posiactual] == 'SOB' or historico[posiactual] == 'SOBR' or historico[posiactual] == 'APRO' or historico[posiactual] == 'CONT' or historico[posiactual] == 'REPR' or historico[posiactual] == 'NOT':
                                    nota = historico[posiactual]
                                    esnota = True
                                    if nota == 'SOB' or nota == 'SOBR':
                                        x2[fila][columna] = 20

                                    elif nota == 'CONT' or nota == 'APRO':
                                        x2[fila][columna] = 10

                                    elif nota == 'NOT':
                                        x2[fila][columna] = 15

                                    elif nota == 'REPR':
                                        x2[fila][columna] = 5

                                    # columna=columna+1

                                    #print(str(materia)+' '+str(nota))
                            posiactual = posiactual+1
                            # columna=columna+1

            elif posicionperiodoactual == utlimoperiodo:
                posicionperiodosiguiente = len(historico)
                # print(posicionperiodoactual)
                # print(posicionperiodosiguiente)
                for j in range(posicionperiodoactual, posicionperiodosiguiente, 1):
                    if historico[j] in codigosmateria or (len(historico[j]) == 7 and (historico[j][0] == 'B' or historico[j][0] == 'F')):
                        columna = columna+1
                        if historico[j] in codigosmateria:
                            # print(historico[j])
                            materia = historico[j]
                            esnota = False
                            posiactual = j

                        else:
                            # print(historico[j])
                            materia = 'Electiva'
                            esnota = False
                            posiactual = j

                        for l in range(len(codigosynbombres)):
                            if materia == codigosynbombres[l][0] and materia != 'Electiva':
                                nombredemat = codigosynbombres[l][1]
                            elif materia == 'Electiva':
                                nombredemat = 'Electiva'

                        for y in range(len(metadata)):
                            if nombredemat == metadata.iloc[y][0]:
                                xx[fila][columna] = (y + 1)
                                #xx[fila][columna] = y+2
                        # columna=columna+1

                        while(esnota == False and posiactual < len(historico)):
                            # posiactual=j
                            if (historico[posiactual].isdigit() and len(historico[posiactual]) <= 2) or (historico[posiactual] == 'SOB' or historico[posiactual] == 'SOBR' or
                                                                                                         historico[posiactual] == 'APRO' or historico[posiactual] == 'CONT' or
                                                                                                         historico[posiactual] == 'REPR' or historico[posiactual] == 'NOT'):

                                if historico[posiactual].isdigit() and len(historico[posiactual]) <= 2:
                                    # print(historico[posiactual])
                                    nota = historico[posiactual]
                                    esnota = True
                                    x2[fila][columna] = nota

                                    # print(str(materia)+' '+str(nota))#imprimir
                                elif historico[posiactual] == 'SOB' or historico[posiactual] == 'SOBR' or historico[posiactual] == 'APRO' or historico[posiactual] == 'CONT' or historico[posiactual] == 'REPR' or historico[posiactual] == 'NOT':
                                    nota = historico[posiactual]
                                    esnota = True
                                    if nota == 'SOB' or nota == 'SOBR':
                                        x2[fila][columna] = 20

                                    elif nota == 'CONT' or nota == 'APRO':
                                        x2[fila][columna] = 10

                                    elif nota == 'NOT':
                                        x2[fila][columna] = 15

                                    elif nota == 'REPR':
                                        x2[fila][columna] = 5

                                    # columna=columna+1

                                    # print(str(materia)+' '+str(nota))#imprimir
                            posiactual = posiactual+1

    return xx, x2


def cambiarformato(x2):
    x2 = x2
    for i in range(x2.shape[0]):
        for j in range(x2.shape[1]):
            if x2[i, j] < 10 and x2[i, j] != 0:
                x2[i, j] = 0.01
            elif x2[i, j] >= 10:
                x2[i, j] = 1
    return x2


def ordenarmenoramayor(arreglo1, arreglo2):
    xxord = arreglo1
    x3ord = arreglo2
    # yord=arreglo3

    for j in range(23):
        if np.count_nonzero(xxord[j]) > 0:
            ultimafila = j

    for j in range(23):
        if j != ultimafila and j != 22 and np.count_nonzero(xxord[j]) > 0:
            numrecorrido = 0
            while(numrecorrido < 7):
                minimo = 100
                posiciondelmin = -1
                for k in range(numrecorrido, 7):
                    if xxord[j, k] < minimo:
                        minimo = xxord[j, k]
                        posiciondelmin = k
                xxord[j, posiciondelmin] = xxord[j, numrecorrido]
                xxord[j, numrecorrido] = minimo
                if j == 22:
                    print('wtf')
                    print(ultimafila)
                    print(i)
                auxiliar = x3ord[j, posiciondelmin]
                x3ord[j, posiciondelmin] = x3ord[j, numrecorrido]
                x3ord[j, numrecorrido] = auxiliar
                numrecorrido = numrecorrido+1
        elif j == ultimafila:
            numrecorrido = 0
            while(numrecorrido < 7):
                minimo = 100
                posiciondelmin = -1
                for k in range(numrecorrido, 7):
                    if xxord[j, k] < minimo:
                        minimo = xxord[j, k]
                        posiciondelmin = k
                xxord[j, posiciondelmin] = xxord[j, numrecorrido]
                xxord[j, numrecorrido] = minimo
                # auxiliar=yord[i,posiciondelmin]
                # yord[i,posiciondelmin]=yord[i,numrecorrido]
                # yord[i,numrecorrido]=auxiliar
                numrecorrido = numrecorrido+1

    return xxord, x3ord  # ,yord

def imprimirtrimestres(xx,metadata,x2):
    xx=xx
    lista=[]
    metadata=metadata
    trimestre=0

    for i in range(xx.shape[0]):
        listaaux=[]
        if np.count_nonzero(xx[i])!=0:
            if np.count_nonzero(xx[i+1])!=0:
                trimestre=trimestre+1
                listaaux.append('Trimestre: '+str(trimestre))
                for j in range(xx.shape[1]):
                    if xx[i,j]!=0:
                        listaaux.append('materia: '+str(metadata.iloc[int(xx[i,j]-1)][0])+' nota: '+str(x2[i,j]))
            else:
                listaaux.append('Trimestre a predecir')
                for j in range(xx.shape[1]):
                    if xx[i,j]!=0:
                        listaaux.append('materia: '+str(metadata.iloc[int(xx[i,j]-1)][0]))
            lista.append(listaaux)
    
    return lista




        
