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
        if np.count_nonzero(xxord[j]) > 0:
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
                auxiliar = x3ord[j, posiciondelmin]
                x3ord[j, posiciondelmin] = x3ord[j, numrecorrido]
                x3ord[j, numrecorrido] = auxiliar
                numrecorrido = numrecorrido+1
                '''
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
                if j == 22:
                    print('wtf')
                    print(ultimafila)
                    print(i)
                auxiliar = x3ord[j, posiciondelmin]
                x3ord[j, posiciondelmin] = x3ord[j, numrecorrido]
                x3ord[j, numrecorrido] = auxiliar
                numrecorrido = numrecorrido+1
                # auxiliar=yord[i,posiciondelmin]
                # yord[i,posiciondelmin]=yord[i,numrecorrido]
                # yord[i,numrecorrido]=auxiliar
                numrecorrido = numrecorrido+1'''

    return xxord, x3ord  # ,yord

def imprimirtrimestres(xx,metadata,x2):
    xx=xx
    lista=[]
    metadata=metadata
    trimestre=0

    for i in range(xx.shape[0]):
        listaaux=[]
        if np.count_nonzero(xx[i])!=0 and np.count_nonzero(xx[i+1])!=0:
            trimestre=trimestre+1
            listaaux.append('Trimestre: '+str(trimestre))
            for j in range(xx.shape[1]):
                if xx[i,j]!=0:
                    if x2[i,j]!=0.1:
                        listaaux.append('materia: '+str(metadata.iloc[int(xx[i,j]-1)][0])+' nota: '+str(x2[i,j]))    
                    elif x2[i,j]==0.1:
                        listaaux.append('materia: '+str(metadata.iloc[int(xx[i,j]-1)][0])+' nota: Retirada')

            lista.append(listaaux)
        elif np.count_nonzero(xx[i])!=0 and np.count_nonzero(xx[i+1])==0:
            listaaux.append('Trimestre a predecir:')
            for j in range(xx.shape[1]):
                if xx[i,j]!=0:
                    listaaux.append('materia: '+str(metadata.iloc[int(xx[i,j]-1)][0])+' ')  
            lista.append(listaaux)
    
    return lista

def obtenernummat(xx):
    xx=xx
    ultimapos=-1
    x3=np.zeros((1,7))
    for i in range(xx.shape[0]):
        if np.count_nonzero(xx[i])!=0:
            ultimapos=i
    nummat=np.count_nonzero(xx[ultimapos])
    x3[0,nummat-1]=1
    return x3

def incluirpred(x1,pred):
    x1=x1
    pred = pred.split(",")
    pred=np.asarray(pred)
    ultimtrim=0

    for i in range(x1.shape[0]):
        if np.count_nonzero(x1[i])!=0:
            ultimtrim=i
    x1[ultimtrim+1]=pred
    return x1

def incluirreti(x1,x2,retiradas):
    x1=x1
    x2=x2
    retiradas = retiradas.split(",")
    retiradas=np.asarray(retiradas)
    for i in range(retiradas.shape[0]):
        if i%2==0 or i==0 and i<=retiradas.shape[0]-1:
            if int(retiradas[i+1])!=0:
                cuenta=np.count_nonzero(x1[int(retiradas[i])-1])
                cuenta=6-cuenta
                x1[int(retiradas[i])-1,cuenta]=int(retiradas[i+1])
                x2[int(retiradas[i])-1,cuenta]=0.1


    return x1,x2
    


def darprediccion(xx,metadata,x3,prediccion):
    xx=xx
    x3=x3
    metadata=metadata
    prediccion=prediccion
    listaaux=[]
    prediccion
    for i in range(7):
        if x3[0,i]==1:
            nummaterias=i+1
    for i in range(23):
        if np.count_nonzero(xx[i])!=0 and np.count_nonzero(xx[i+1])==0:
            ultimotrim=xx[i]
    #print(ultimotrim.shape)
    #print(prediccion.shape)
    for j in range(7-nummaterias,7):
        listaaux.append('materia: '+str(metadata.iloc[int(ultimotrim[j]-1)][0])+' proababilidad de nota mayor a 12: '+str(prediccion[0,j]))



    return listaaux

def darprediccion2(xx,metadata,x3,prediccion):
    xx=xx
    x3=x3
    metadata=metadata
    prediccion=prediccion
    listaaux=[]
    prediccion
    for i in range(7):
        if x3[0,i]==1:
            nummaterias=i+1
    for i in range(23):
        if np.count_nonzero(xx[i])!=0 and np.count_nonzero(xx[i+1])==0:
            ultimotrim=xx[i]
    #print(ultimotrim.shape)
    #print(prediccion.shape)
    for j in range(7-nummaterias,7):
        listaaux.append('materia: '+str(metadata.iloc[int(ultimotrim[j]-1)][0])+' proababilidad de nota mayor a 10: '+str(prediccion[0,j]))



    return listaaux

def validar1(xx,pred,x2):
    xx=xx
    pred=pred
    x2=x2
    pred = pred.split(",")
    pred=np.asarray(pred)
    todaspasadas=True
    for i in range(pred.shape[0]):
        if int(pred[i])!=0:
            for t in range(xx.shape[0]):
                for y in range(xx.shape[1]):
                    if xx[t,y]==int(pred[i]) and x2[t,y]>=10 and int(pred[i])!=19 and int(pred[i])!=59:
                        todaspasadas=False
    return todaspasadas

def validar2(pred):
    pred=pred
    pred = pred.split(",")
    pred=np.asarray(pred)
    matrepe=False
    for i in range(pred.shape[0]):
        if int(pred[i])!=0:
            for j in range(pred.shape[0]):
                if int(pred[j])==int(pred[i]) and i!=j and int(pred[i])!=19:
                    matrepe=True
    return matrepe

def validar3(x1,retiradas):
    x1=x1
    retiradas = retiradas.split(",")
    retiradas=np.asarray(retiradas)
    error=False
    for i in range(retiradas.shape[0]):
        if i%2==0 or i==0 and i<=retiradas.shape[0]-1:
            if int(retiradas[i+1])!=0:
                cuenta=np.count_nonzero(x1[int(retiradas[i])-1])
                if cuenta<7:    
                    cuenta=6-cuenta
                    x1[int(retiradas[i])-1,cuenta]=int(retiradas[i+1])
                elif cuenta==7:
                    error=True
    return error


def validar4(retiradas):
    retiradas = retiradas.split(",")
    retiradas=np.asarray(retiradas)
    error=False
    for i in range(retiradas.shape[0]):
        if i%2==0 or i==0 and i<=retiradas.shape[0]-1:
            if int(retiradas[i+1])!=0:
                for k in range(retiradas.shape[0]):
                    if k%2!=0 or k!=0 and k<=retiradas.shape[0]-1 and int(retiradas[k])!=0:
                        if k!=i+1 and retiradas[k-1]==retiradas[i] and int(retiradas[k])!=19 and retiradas[k]==retiradas[i+1]:
                            error=True

    return error

def validar5(x1,retiradas,x2):
    x1=x1
    retiradas=retiradas
    x2=x2
    retiradas = retiradas.split(",")
    retiradas=np.asarray(retiradas)
    error=False
    for i in range(retiradas.shape[0]):
        if i%2==0 or i==0 and i<=retiradas.shape[0]-1:
            if int(retiradas[i+1])!=0 and int(retiradas[i+1])!=19 and int(retiradas[i+1])!=59:
                for p in range(x1.shape[0]):
                    for t in range(x1.shape[1]):
                        if x1[p,t]==int(retiradas[i+1]) and x2[p,t]>=10 and p<int(retiradas[i])-1:
                            error=True
    return error

def ulttrim(xx):
    ultitrim=0
    for i in range(xx.shape[0]):
        if np.count_nonzero(xx[i])!=0:
            ultitrim=i
    print(ultitrim)
    return ultitrim
