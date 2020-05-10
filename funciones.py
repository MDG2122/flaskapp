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

                    if historico[j] in codigosmateria or (len(historico[j]) == 7 and (historico[j][0] == 'B' or historico[j][0] == 'F') and (historico[j][6].isdigit())):
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

                                if historico[posiactual].isdigit() and len(historico[posiactual]) <= 2 and historico[posiactual-3]!='ELEMENTOS':
                                    if historico[posiactual]!=0:
                                        # print(historico[posiactual])
                                        nota = historico[posiactual]
                                        esnota = True
                                        x2[fila][columna] = nota
                                    else:
                                        nota = 0.01
                                        esnota = True
                                        x2[fila][columna] = nota
                                elif historico[posiactual].isdigit() and len(historico[posiactual]) <= 2 and historico[posiactual-3]=='ELEMENTOS':
                                    if historico[posiactual]!=0:
                                        # print(historico[posiactual])
                                        nota = historico[posiactual+1]
                                        esnota = True
                                        x2[fila][columna] = nota
                                    else:
                                        nota = 0.01
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
                    if historico[j] in codigosmateria or (len(historico[j]) == 7 and (historico[j][0] == 'B' or historico[j][0] == 'F') and (historico[j][6].isdigit())):
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

                                if historico[posiactual].isdigit() and len(historico[posiactual]) <= 2 and historico[posiactual-3]!='ELEMENTOS':
                                    if historico[posiactual]!=0:
                                        # print(historico[posiactual])
                                        nota = historico[posiactual]
                                        esnota = True
                                        x2[fila][columna] = nota
                                    else:
                                        nota = 0.01
                                        esnota = True
                                        x2[fila][columna] = nota
                                elif historico[posiactual].isdigit() and len(historico[posiactual]) <= 2 and historico[posiactual-3]=='ELEMENTOS':
                                    if historico[posiactual]!=0:
                                        # print(historico[posiactual])
                                        nota = historico[posiactual+1]
                                        esnota = True
                                        x2[fila][columna] = nota
                                    else:
                                        nota = 0.01
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
        listamatenonum=[10,11,59,65]
        espacio='   |   '
        if np.count_nonzero(xx[i])!=0 and np.count_nonzero(xx[i+1])!=0:
            trimestre=trimestre+1
            listaaux.append('Trimestre '+str(trimestre))
            for j in range(xx.shape[1]):
                if xx[i,j]!=0 and xx[i,j] not in listamatenonum:
                    if x2[i,j]!=0.1 and  x2[i,j]!=0.01:
                        listaaux.append(''+str(metadata.iloc[int(xx[i,j]-1)][0])+espacio*1+str(int(x2[i,j])))    
                    elif x2[i,j]==0.1:
                        listaaux.append(''+str(metadata.iloc[int(xx[i,j]-1)][0])+espacio*1+'Retirada')
                    elif x2[i,j]==0.01:
                        listaaux.append(''+str(metadata.iloc[int(xx[i,j]-1)][0])+espacio*1+'0')
                elif xx[i,j] in listamatenonum:
                    if xx[i,j]==10 or xx[i,j]==11:
                        if x2[i,j]==10:
                            listaaux.append(''+str(metadata.iloc[int(xx[i,j]-1)][0])+espacio*1+'APRO')
                        elif x2[i,j]==20:
                            listaaux.append(''+str(metadata.iloc[int(xx[i,j]-1)][0])+espacio*1+'HONO')
                        elif x2[i,j]==5:
                            listaaux.append(''+str(metadata.iloc[int(xx[i,j]-1)][0])+espacio*1+'REPR/DIFE')
                    elif xx[i,j]==65:
                        if x2[i,j]==10:
                            listaaux.append(''+str(metadata.iloc[int(xx[i,j]-1)][0])+espacio*1+'APRO')
                        elif x2[i,j]==20:
                            listaaux.append(''+str(metadata.iloc[int(xx[i,j]-1)][0])+espacio*1+'SOBR')
                        elif x2[i,j]==5:
                            listaaux.append(''+str(metadata.iloc[int(xx[i,j]-1)][0])+espacio*1+'REPR')
                        elif x2[i,j]==15:
                            listaaux.append(''+str(metadata.iloc[int(xx[i,j]-1)][0])+espacio*1+'NOT')
                    elif xx[i,j]==59:
                        contadordeveranos=0
                        for t in range(xx.shape[0]):
                            for l in range(xx.shape[1]):
                                if xx[t,l]==59:
                                    contadordeveranos=contadordeveranos+1
                        if contadordeveranos==1:
                            listaaux.append(''+str(metadata.iloc[int(xx[i,j]-1)][0])+espacio*1+'CONT')
                        else:
                            primerverano=True
                            for y in range(i+1,23):
                                for u in range(7):
                                    if xx[y,u]==59:
                                        primerverano=False
                            if primerverano is False:
                                listaaux.append(''+str(metadata.iloc[int(xx[i,j]-1)][0])+espacio*1+'CONT')
                            else:
                                if x2[i,j]==10:
                                    listaaux.append(''+str(metadata.iloc[int(xx[i,j]-1)][0])+espacio*1+'APRO')
                                elif x2[i,j]==20:
                                    listaaux.append(''+str(metadata.iloc[int(xx[i,j]-1)][0])+espacio*1+'SOBR')
                                elif x2[i,j]==5:
                                    listaaux.append(''+str(metadata.iloc[int(xx[i,j]-1)][0])+espacio*1+'REPR')
                                elif x2[i,j]==15:
                                    listaaux.append(''+str(metadata.iloc[int(xx[i,j]-1)][0])+espacio*1+'NOT')
                            

            lista.append(listaaux)
        elif np.count_nonzero(xx[i])!=0 and np.count_nonzero(xx[i+1])==0:
            listaaux.append('Trimestre a Predecir')
            for j in range(xx.shape[1]):
                if xx[i,j]!=0:
                    listaaux.append(''+str(metadata.iloc[int(xx[i,j]-1)][0])+' ')  
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
    listamatenonum=[10,11,59,65]
    for i in range(7):
        if x3[0,i]==1:
            nummaterias=i+1
    for i in range(23):
        if np.count_nonzero(xx[i])!=0 and np.count_nonzero(xx[i+1])==0:
            ultimotrim=xx[i]
    #print(ultimotrim.shape)
    #print(prediccion.shape)
    for j in range(7-nummaterias,7):
        if ultimotrim[j] not in listamatenonum:
            if prediccion[0,j]<=0.8:
                listaaux.append(''+str(metadata.iloc[int(ultimotrim[j]-1)][0])+', '+str(round(prediccion[0,j]*100,2))+'% Probabilidad de Aprobar')
            elif prediccion[0,j]>=0.8 and  prediccion[0,j]<=0.95:
                listaaux.append(''+str(metadata.iloc[int(ultimotrim[j]-1)][0])+', '+str(round(prediccion[0,j]*100,2))+'% Probabilidad de Aprobar (Muy posible aprobar con una califcacion de 12 o mas \U0001F604)')
            elif prediccion[0,j]>=0.95:
                listaaux.append(''+str(metadata.iloc[int(ultimotrim[j]-1)][0])+', '+str(round(prediccion[0,j]*100,2))+'% Probabilidad de Aprobar (Muy posible aprobar con una califcacion de 14 o mas \U0001F973)')
        else:
            listaaux.append(''+str(metadata.iloc[int(ultimotrim[j]-1)][0])+', '+str(round(prediccion[0,j]*100,2))+'% Probabilidad de Aprobar')


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

def buscarprelaciones(xx,x2,materia,materiasqueprelan):
    prelaciones=False
    for i in range(materiasqueprelan.shape[0]):
        for j in range(xx.shape[0]):
            for k in range(xx.shape[1]):
                if xx[j,k]==materiasqueprelan[i] and  x2[j,k]>=10:
                    materiasqueprelan[i]=0
    if np.count_nonzero(materiasqueprelan==0)==materiasqueprelan.shape[0]:
        prelaciones=True
    return prelaciones

def contarcreditos(xx,x2):
    creditos=0
    for i in range(xx.shape[0]):
        for j in range(xx.shape[1]):
            if xx[i,j]!=0 and xx[i,j]!=59 and x2[i,j]>=10:
                creditos=creditos+3
    return creditos

def contarcreditosBP(xx,x2):
    creditos=0
    listaBP=np.array([56,12,45,44,3,20,46,37,21,5,18,47,22,48,2,54,64,13,49,36,16])
    for i in range(xx.shape[0]):
        for j in range(xx.shape[1]):
            if xx[i,j]!=0 and xx[i,j]!=59 and x2[i,j]>=10 and xx[i,j] in listaBP:
                creditos=creditos+3
    return creditos

def prelaciones(xx,x2,materias):
    materias=materias
    materias = materias.split(",")
    materias=np.asarray(materias)
    error=False
    creditos=contarcreditos(xx,x2)
    creditosBP=contarcreditosBP(xx,x2)
    for i in range(materias.shape[0]):
        if  int(materias[i])!=0:
            if int(materias[i])==42:
                prela=np.array([43])
                boolea = buscarprelaciones(xx,x2,materias[i],prela)
                if boolea == False:
                    error=True
            if int(materias[i])==8:
                prela=np.array([40])
                boolea = buscarprelaciones(xx,x2,materias[i],prela)
                if boolea == False:
                    error=True
            if int(materias[i])==66:
                prela=np.array([67])
                boolea = buscarprelaciones(xx,x2,materias[i],prela)
                if boolea == False:
                    error=True
            if int(materias[i])==4:
                prela=np.array([7])
                boolea = buscarprelaciones(xx,x2,materias[i],prela)
                if boolea == False:
                    error=True
            if int(materias[i])==45 or int(materias[i])==12 or int(materias[i])==56:
                prela=np.array([42])
                boolea = buscarprelaciones(xx,x2,materias[i],prela)
                if boolea == False:
                    error=True
            if int(materias[i])==35:
                prela=np.array([66])
                boolea = buscarprelaciones(xx,x2,materias[i],prela)
                if boolea == False:
                    error=True
            if int(materias[i])==46 or int(materias[i])==44:
                prela=np.array([45])
                boolea = buscarprelaciones(xx,x2,materias[i],prela)
                if boolea == False:
                    error=True
            if int(materias[i])==37:
                prela=np.array([56])
                boolea = buscarprelaciones(xx,x2,materias[i],prela)
                if boolea == False:
                    error=True
            if int(materias[i])==20:
                prela=np.array([35,45])
                boolea = buscarprelaciones(xx,x2,materias[i],prela)
                if boolea == False:
                    error=True
            if int(materias[i])==47:
                prela=np.array([46])
                boolea = buscarprelaciones(xx,x2,materias[i],prela)
                if boolea == False:
                    error=True
            if int(materias[i])==3:
                prela=np.array([45])
                boolea = buscarprelaciones(xx,x2,materias[i],prela)
                if boolea == False:
                    error=True
            if int(materias[i])==21:
                prela=np.array([20,46])
                boolea = buscarprelaciones(xx,x2,materias[i],prela)
                if boolea == False:
                    error=True
            if int(materias[i])==22:
                prela=np.array([21])
                boolea = buscarprelaciones(xx,x2,materias[i],prela)
                if boolea == False:
                    error=True
            if int(materias[i])==47:
                prela=np.array([46])
                boolea = buscarprelaciones(xx,x2,materias[i],prela)
                if boolea == False:
                    error=True
            if int(materias[i])==2:
                prela=np.array([44,47])
                boolea = buscarprelaciones(xx,x2,materias[i],prela)
                if boolea == False:
                    error=True
            if int(materias[i])==18 or int(materias[i])==5:
                prela=np.array([3])
                boolea = buscarprelaciones(xx,x2,materias[i],prela)
                if boolea == False:
                    error=True
            if int(materias[i])==23:
                prela=np.array([22])
                boolea = buscarprelaciones(xx,x2,materias[i],prela)
                if boolea == False:
                    error=True
            if int(materias[i])==13:
                prela=np.array([48])
                boolea = buscarprelaciones(xx,x2,materias[i],prela)
                if boolea == False:
                    error=True
            if int(materias[i])==62 or int(materias[i])==6:
                prela=np.array([18])
                boolea = buscarprelaciones(xx,x2,materias[i],prela)
                if boolea == False:
                    error=True
            if int(materias[i])==54:
                prela=np.array([5])
                boolea = buscarprelaciones(xx,x2,materias[i],prela)
                if boolea == False:
                    error=True
            if int(materias[i])==36:
                prela=np.array([22])
                boolea = buscarprelaciones(xx,x2,materias[i],prela)
                if boolea == False:
                    error=True
            if int(materias[i])==49:
                prela=np.array([48])
                boolea = buscarprelaciones(xx,x2,materias[i],prela)
                if boolea == False:
                    error=True
            if int(materias[i])==52:
                prela=np.array([13])
                boolea = buscarprelaciones(xx,x2,materias[i],prela)
                if boolea == False:
                    error=True
            if int(materias[i])==64:
                prela=np.array([54])
                boolea = buscarprelaciones(xx,x2,materias[i],prela)
                if boolea == False:
                    error=True
            if int(materias[i])==63:
                prela=np.array([21])
                boolea = buscarprelaciones(xx,x2,materias[i],prela)
                if boolea == False:
                    error=True
            if int(materias[i])==33:
                prela=np.array([7])
                boolea = buscarprelaciones(xx,x2,materias[i],prela)
                if boolea == False or creditos<105 :
                    error=True
            if int(materias[i])==53:
                prela=np.array([52])
                boolea = buscarprelaciones(xx,x2,materias[i],prela)
                if boolea == False:
                    error=True
            if int(materias[i])==25:
                prela=np.array([6,62])
                boolea = buscarprelaciones(xx,x2,materias[i],prela)
                if boolea == False:
                    error=True
            if int(materias[i])==1:
                prela=np.array([6,62])
                boolea = buscarprelaciones(xx,x2,materias[i],prela)
                if boolea == False:
                    error=True
            if int(materias[i])==16:
                prela=np.array([47])
                boolea = buscarprelaciones(xx,x2,materias[i],prela)
                if boolea == False:
                    error=True
            if int(materias[i])==58:
                prela=np.array([63])
                boolea = buscarprelaciones(xx,x2,materias[i],prela)
                if boolea == False:
                    error=True
            if int(materias[i])==59:
                prela=np.array([57])
                prela2=np.array([41])
                boolea = buscarprelaciones(xx,x2,materias[i],prela)
                boolea2 = buscarprelaciones(xx,x2,materias[i],prela2)
                if boolea == False and boolea2 == False:
                    error=True
            if int(materias[i])==57 or int(materias[i])==41:
                if creditos<75:
                    error=True
            if int(materias[i])==65 or int(materias[i])==26 or int(materias[i])==27 or int(materias[i])==55:
                if creditos<120:
                    error=True
            if int(materias[i])==24:
                prela=np.array([52])
                boolea = buscarprelaciones(xx,x2,materias[i],prela)
                if boolea == False and creditosBP<57:
                    error=True
            if int(materias[i])==50:
                prela=np.array([53])
                boolea = buscarprelaciones(xx,x2,materias[i],prela)
                if boolea == False and creditosBP<57:
                    error=True
            if int(materias[i])==60:
                prela=np.array([16])
                boolea = buscarprelaciones(xx,x2,materias[i],prela)
                if boolea == False and creditosBP<57:
                    error=True
            if int(materias[i])==51:
                prela=np.array([16])
                boolea = buscarprelaciones(xx,x2,materias[i],prela)
                if boolea == False and creditosBP<57:
                    error=True
            if int(materias[i])==23:
                prela=np.array([62])
                boolea = buscarprelaciones(xx,x2,materias[i],prela)
                if boolea == False and creditosBP<57:
                    error=True
            if int(materias[i])==10 or int(materias[i])==11 :
                prela=np.array([62])
                boolea = buscarprelaciones(xx,x2,materias[i],prela)
                if boolea == False and creditosBP<57:
                    error=True
            
            
            
    return error
    