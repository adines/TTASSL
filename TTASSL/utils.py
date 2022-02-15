from ripser import ripser
import numpy as np
from persim import plot_diagrams
import persim
from numpy import asarray
import random
import umap
import gudhi as gd


def analizar_punto(punto,puntos_ceros,puntos_unos,dgms_ceros,dgms_unos,distance,th,dim=0):

    dgms_ceros_mod = ripser(np.array([punto.tolist()]+puntos_ceros.tolist()))['dgms'][dim]
    dgms_unos_mod = ripser(np.array([punto.tolist()] + puntos_unos.tolist()))['dgms'][dim]

    if distance=='bottleneck':
        distance_cero = persim.bottleneck(dgms_ceros_mod, dgms_ceros, matching=False)
        distance_uno = persim.bottleneck(dgms_unos_mod, dgms_unos, matching=False)
    else:
        distance_cero = persim.wasserstein(dgms_ceros_mod, dgms_ceros, matching=False)
        distance_uno = persim.wasserstein(dgms_unos_mod, dgms_unos, matching=False)

    distancia=distance_cero+distance_uno
    if max(distance_cero/distancia,distance_uno/distancia)<th:
        clase=-1
    elif distance_cero>distance_uno:
        clase=1
    else:
        clase=0
    return clase


def separar_puntos(data,target):
    unos = np.where(target == 1)[0]
    ceros = np.where(target == 0)[0]

    datos_uno = np.array(data)[unos]
    datos_cero = np.array(data)[ceros]

    return datos_cero,datos_uno


def analizar_puntos(data, target, puntos_unlabeled, distance, th=0, reduccion=False, dim=0):
    if not comprobar_distancia(distance):
        return (data,target,np.array([]))
    (puntos_ceros, puntos_unos) = separar_puntos(data, target)
    puntos_unlabeled_umap=puntos_unlabeled
    embedding = data
    if reduccion == True:
        reducer = umap.UMAP(random_state=75)
        embedding=reducer.fit_transform(data)
        puntos_unlabeled_umap=reducer.transform(puntos_unlabeled)
    (puntos_ceros_umap, puntos_unos_umap) = separar_puntos(embedding, target)


    puntos_ceros_final = puntos_ceros.tolist()
    puntos_unos_final = puntos_unos.tolist()
    puntos_dudosos_final = []

    dgms_ceros = ripser(puntos_ceros_umap)['dgms'][dim]
    dgms_unos = ripser(puntos_unos_umap)['dgms'][dim]
    for i, punto in enumerate(puntos_unlabeled_umap):
        clase = analizar_punto(punto, puntos_ceros_umap, puntos_unos_umap, dgms_ceros, dgms_unos, distance,th, dim)
        if clase == 1:
            puntos_unos_final.append(puntos_unlabeled[i])
        elif clase == 0:
            puntos_ceros_final.append(puntos_unlabeled[i])
        else:
            puntos_dudosos_final.append(puntos_unlabeled[i])

    puntos_ceros_final=np.array(puntos_ceros_final)
    puntos_unos_final=np.array(puntos_unos_final)
    puntos_dudosos_final=np.array(puntos_dudosos_final)
    new_data=np.concatenate((puntos_ceros_final,puntos_unos_final),axis=0)
    new_target=np.concatenate((np.zeros(puntos_ceros_final.shape[0]),np.ones(puntos_unos_final.shape[0])))

    return (new_data,new_target, puntos_dudosos_final)

def obtener_radio(puntos):
    skeleton = gd.RipsComplex(points = puntos, max_edge_length = 90000000000)
    simplex_tree = skeleton.create_simplex_tree()
    filt=simplex_tree.get_filtration()
    *_, last0 = filt
    return last0[1]


def analizar_punto_gudhi(punto,puntos_ceros,puntos_unos,last0,last1,tipo):
    last_0=obtener_radio(np.array([punto.tolist()]+puntos_ceros.tolist()))
    last_1=obtener_radio(np.array([punto.tolist()]+puntos_unos.tolist()))

    if tipo==0:
        if abs(last0 - last_0) < 0.00001 and abs(last1 - last_1) > 0.00001:
            clase = 0
        elif abs(last1 - last_1) < 0.00001 and abs(last0 - last_0) > 0.00001:
            clase = 1
        else:
            clase = -1
    else:
        dif0 = abs(last0 - last_0)
        dif1 = abs(last1 - last_1)
        if dif0 == 0 and dif1 == 0:
            clase = -1
        elif dif0 < dif1:
            clase = 0
        else:
            clase = 1
    return clase


def analizar_puntos_gudhi(data, target, puntos_unlabeled, tipo, reduccion=False):
    if not comprobar_tipo(tipo):
        return (data,target,np.array([]))
    (puntos_ceros, puntos_unos) = separar_puntos(data, target)
    puntos_unlabeled_umap=puntos_unlabeled
    embedding = data
    if reduccion == True:
        reducer = umap.UMAP(random_state=75)
        embedding=reducer.fit_transform(data)
        puntos_unlabeled_umap=reducer.transform(puntos_unlabeled)
    (puntos_ceros_umap, puntos_unos_umap) = separar_puntos(embedding, target)


    puntos_ceros_final = puntos_ceros.tolist()
    puntos_unos_final = puntos_unos.tolist()
    puntos_dudosos_final = []

    last0 = obtener_radio(puntos_ceros_umap)
    last1 = obtener_radio(puntos_unos_umap)
    for i, punto in enumerate(puntos_unlabeled_umap):
        clase = analizar_punto_gudhi(punto, puntos_ceros_umap, puntos_unos_umap, last0, last1, tipo)
        if clase == 1:
            puntos_unos_final.append(puntos_unlabeled[i])
        elif clase == 0:
            puntos_ceros_final.append(puntos_unlabeled[i])
        else:
            puntos_dudosos_final.append(puntos_unlabeled[i])

    puntos_ceros_final=np.array(puntos_ceros_final)
    puntos_unos_final=np.array(puntos_unos_final)
    puntos_dudosos_final=np.array(puntos_dudosos_final)
    new_data=np.concatenate((puntos_ceros_final,puntos_unos_final),axis=0)
    new_target=np.concatenate((np.zeros(puntos_ceros_final.shape[0]),np.ones(puntos_unos_final.shape[0])))

    return (new_data,new_target, puntos_dudosos_final)

def comprobar_tipo(tipo):
    return tipo==1 or tipo==0

def comprobar_distancia(distancia):
    return distancia=='bottleneck' or distancia=='wasserstein'