#File:        Clustering.py
#Author:      Brendan Waters
#Email:       b101@umbc.edu
#Description:
#  This program will complete k-means clustering on a given
# set of 2D points and print the result graphically to the user with clusters
# marked in different colors and cluster centers marked with stars. 
# Usage: python Clustering.py numberOfClusters file.txt

import sys
import random
import math
import matplotlib.pyplot as plt

KMEANS_ITERATIONS = 50

#reads 2D coordinates from a text file
#returns list of 2-tuple coordinates
def parseFile(filename):

    points = []

    #loop thru lines in file, adding each point to points
    with open(filename, "r") as inputFile:
        for line in inputFile:
            data = line.split()
            point = (float(data[0]), float(data[1]))
            points.append(point)

    return points

#places original cluster points
#returns list of 2-tuple cluster point coordinates
def placeClusterPoints(k, data):

    #first loop thru data to find range of values
    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0
    for coord in data:
        if(coord[0] < min_x):
            min_x = coord[0]
        if(coord[0] > max_x):
            max_x = coord[0]
        if(coord[1] < min_y):
            min_y = coord[1]
        if(coord[1] > max_y):
            max_y = coord[1]

    #now generate random cluster points in that range
    clusterPoints = []
    for i in range(0, k):
        x = random.uniform(min_x, max_x)
        y = random.uniform(min_y, max_y)
        clusterPoints.append((x, y))

    return clusterPoints

#plots points graphically in a new window to show user
def plotPoints(mapping):

    #loop thru cluster points in the dictionary
    cluster_x = []
    cluster_y = []
    for key in mapping:
        cluster_x.append(key[0])
        cluster_y.append(key[1])
        
        #loop thru the mapped data points
        data_x = []
        data_y = []
        for coord in mapping[key]:
            data_x.append(coord[0])
            data_y.append(coord[1])
        
        #now draw it with a random color
        rgb = (random.random(), random.random(), random.random())
        plt.plot(data_x, data_y, marker="o", color=rgb, linestyle='None')
            

    plt.plot(cluster_x, cluster_y, 'k*', markersize=15)
    plt.show()

#get distance between two coordinates
def dist(a, b):
    
    return math.sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2)

#does one iteration of k-means clustering
#returns dictionary of cluster points with mapped data points
def kmeans(dataPoints, clusterPoints):

    #create dictionary of cluster points to keep track of mapped dataPoints
    mapping = {}

    for i in range(0, KMEANS_ITERATIONS):
    
        #reset dictionary
        mapping.clear()
        for clusterPoint in clusterPoints:
            mapping[clusterPoint] = []
    
        #loop thru data points
        for coord in dataPoints:

            #find closest cluster point
            closestCluster = clusterPoints[0]
            closestDistance = dist(coord, closestCluster)
            for clusterPoint in clusterPoints:
                distance = dist(coord, clusterPoint)
                if distance < closestDistance:
                    closestCluster = clusterPoint
                    closestDistance = distance
                    
            #add this coord to the cluster point its closest to
            mapping[closestCluster].append(coord)

        #now reposition the cluster points
        for i in range(0, len(clusterPoints)):
            x_total = 0
            y_total = 0
            count = 0
            for coord in mapping[clusterPoints[i]]:
                x_total += coord[0]
                y_total += coord[1]
                count += 1
            if count > 0:
                x_new = x_total / count
                y_new = y_total / count
                clusterPoints[i] = (x_new, y_new)

    return mapping

#main logic of program
def main():

    if(len(sys.argv) != 3):
        print("usage: python Clustering.py numberOfClusters file.txt")
        exit()

    k = int(sys.argv[1])
    filename = sys.argv[2]

    #seed random for later use
    random.seed()

    data = parseFile(filename)

    clusterPoints = placeClusterPoints(k, data)

    mapping = kmeans(data, clusterPoints)
    
    plotPoints(mapping)

if __name__ == "__main__": main()
