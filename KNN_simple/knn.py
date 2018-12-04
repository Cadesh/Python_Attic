# AUTHOR: Andre Rosa
# DATE: 28 NOV 2018
# Based in the example from:
# https://www.analyticsvidhya.com/blog/2018/03/introduction-k-neighbours-algorithm-clustering/
#
# PYTHON IMPLEMENTATION OF KNN (K Nearest Neighbors)

# Importing libraries
import pandas as pd  # BSD library for data analysis istall with conda install pandas
import numpy as np
import math
import operator


#------------------------------------------------------------------------------------
# Defining a function which calculates euclidean distance between two data points
#------------------------------------------------------------------------------------
def euclideanDistance(data1, data2, length):
    distance = 0
    for x in range(length):
        distance += np.square(data1[x] - data2[x])
    return np.sqrt(distance)

#-------------------------------------------------------------------------------------
# Defining our KNN model
#-------------------------------------------------------------------------------------
def KNN(train, test, k):
 
    distances = {}
 
    length = test.shape[1]
    print ('size of train vector,', length)
    
    # Calculating euclidean distance between each row of training data and test data
    print ('Calculating Euclidean distance')
    trnLen = len(train)
    for x in range(trnLen):
  
        dist = euclideanDistance(test, train.iloc[x], length)
        print (x)

        distances[x] = dist[0]

    
    print ('distance', distances[0])
 

    # Sorting them on the basis of distance
    sorted_d = sorted(distances.items(), key=operator.itemgetter(1))

    neighbors = []
    

    # Extracting top k neighbors
    for x in range(k):
        neighbors.append(sorted_d[x][0])

    classVotes = {}
    

    # Calculating the most freq class in the neighbors
    for x in range(len(neighbors)):
        response = train.iloc[neighbors[x]][-1]
 
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1
    #### End of STEP 3.4

    #### Start of STEP 3.5
    sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True)
    return(sortedVotes[0][0], neighbors)
    #### End of STEP 3.5
#--------------------------------------------------------------------------------------


# Importing data 
train = pd.read_csv("train10.csv")

print (train)

import time
# Log the time
time_start = time.time()

test = pd.read_csv("slice_0.csv", header = None)
#print (test.head())

# Setting number of neighbors = 1
k = 1
# Running KNN model
result,neigh = KNN(train, test, k)

# Predicted class
print(result)

# Nearest neighbor
print(neigh)

# finish
time_end = time.time()
print ("Done in %d "  %(time_end-time_start) + "seconds.\n")
