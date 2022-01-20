from TTASSL.utils import *

def homological_annotation(data, target, puntos_unlabeled, distance, th=0, reduccion=False, dim=0):
    return analizar_puntos(data, target, puntos_unlabeled, distance, th, reduccion, dim)


def connectivity_annotation(data, target, puntos_unlabeled, tipo, reduccion=False):
    return analizar_puntos_gudhi(data, target, puntos_unlabeled, tipo, reduccion)