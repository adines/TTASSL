# Towards a Topological Approach for Semi-SupervisedLearning

Nowadays, Machine Learning and Deep Learning methods have become the 
state-of-the-art approach to solve data classification tasks. 
In order to use those methods, it is necessary to acquire and label a 
considerable amount of data; however, this is not straightforward in some 
fields, since data annotation is time consuming and might require expert 
knowledge. This challenge can be tackled by means of semi-supervised 
learning methods that take advantage of both labelled and unlabelled data. 
In this work, we present new semi-supervised learning methods based on 
techniques from Topological Data Analysis (TDA), a field that is gaining 
importance for analysing large amounts of data with high variety and 
dimensionality. In particular, we have created two semi-supervised 
learning methods following two different topological approaches. 
In the former, we have used a homological approach that consists in 
studying the persistence diagrams associated with the data using the 
Bottleneck and Wasserstein distances. In the latter, we have taken 
into account the connectivity of the data. In addition, we have 
carried out a thorough analysis of the developed methods using 3 
synthetic datasets, 5 structured datasets, and 2 datasets of images. 
The results show that the semi-supervised methods developed in this work 
outperform both the results obtained with models trained with only manually 
labelled data, and those obtained with classical semi-supervised learning 
methods, reaching improvements of up to a 16\%.

## Installation

TTASSL is available in PyPi for Python 3.6. To use it, you have to install 
Python 3.6 and pip.

```
pip install TTASSL
``` 

## Methods

We have two available methods, one that use homological properties of the data,
and other that use the connectivity properties. That methods are:

```
homological_annotation(data, target, puntos_unlabeled, distance, th=0, reduccion=False, dim=0)


connectivity_annotation(data, target, puntos_unlabeled, tipo, reduccion=False)
``` 

## Expermients

We have carried out a set of experiments with the different methods that can be found 
in the [experiments](https://github.com/adines/TTASSL/tree/main/Experiments) section.