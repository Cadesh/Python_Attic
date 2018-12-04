#-----------------------------------------------------------------------------
# AUTHOR: Andre Rosa
# DATE: 04DEC2018
# OBJECTIVE: This program calculates the k nearest neighbor (KNN) 
# ----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# PARAMETERS:
# 1 - name of the file with the training data 
# 2 - name of the file with the test data
# 3 - number of closest neighbors, K factor
# 4 - number of threads to use
# EXAMPLE OF USE: python knn.py train.csv test.csv 1 12 
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# OUTPUT:
# The output is a csv file named output_KNN.csv that contains:
# 1 - the test data 1st field
# 2 - the closest neighbor taken from the training data
# 3 - the distance between the two files
#-----------------------------------------------------------------------------

from multiprocessing import Process, Queue
from myCSV import ctrlCSV
import numpy as np

#------------------------------------------------------------------------------
# EUCLIDEAN DISTANCE BETWEEN TWO POINTS IN N DIMENSIONS
#------------------------------------------------------------------------------
def EuclideanDist(testLn, trainLn):
    distance = 0 
    for x in range(1, len(trainLn)):
        distance += np.square(float(testLn[x]) - float(trainLn[x]))
    
    return distance # not calculating the square root because we do not need the values but only the closest video 
    #return np.sqrt(distance)
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# KNN - RECEIVES ONE ROW FROM THE TEST SET AND CALCULATES THE DISTANCE FOR EACH ROW IN TRAINING SET
#------------------------------------------------------------------------------
def KNN (testLn, train, K):

    values = []
    valList = train.getList()
    # calculates the distance for each row in the training set
    for any in valList:
        trainLn = list(any.values())
        vidName = trainLn[0]
        dist = EuclideanDist(testLn, trainLn)
        locObj = (testLn[0], vidName, dist)
        values.append(locObj)

    # sort the results
    from operator import itemgetter
    values.sort(key=itemgetter(2))  # order by distance, index 2

    # get the first K neighbors
    valuesK = values [0:K]
    #print (valuesK)

    return valuesK  # return the pair of closest data and the distance between them
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# WORKER - THIS IS THE FUNCTION THAT WILL RUN IN PARALEL
# for more info on paralellization check: https://pymotw.com/2/multiprocessing/basics.html
#------------------------------------------------------------------------------
def worker (chunk, train, K, idx):

    print ('Starting worker ' + str(idx))
    Klist = []

    for i in range(len(chunk)):
        row = list(chunk[i].values()) #gets the value of the ordered dict in a list
        #print ('hello ' + str(idx) + ' ' + str(row[0]))
        # now calculates the closest neighbor
        getK = KNN (row, train, K)
        #save the closest ones
        Klist = Klist + getK
        #print (Klist)

    ##finally the worker save the list in a csv file
    train.saveCSV(Klist, idx)
#------------------------------------------------------------------------------       

#------------------------------------------------------------------------------
# RUN - THE METHOD THAT INITIATE THE PARALLEL PROCESSING
#------------------------------------------------------------------------------
def run (test, train, K, nrSlices):

    rows = test.countRow()
    size = (int(rows / nrSlices)) #max size of each slice
    rest = rows % nrSlices       

    chunks = []   # object that will hold each slice
    
    # divide the Test data to create slices for paralellization
    idBeg = 0
    idEnd = size
    for x in range (nrSlices):
        if rest > 0:  # distribute the 'rest' more evenly
            pEnd = idEnd + 1
            rest -= 1
        else:
            pEnd = idEnd
        sliceObj = test.getSlice(idBeg, pEnd)
        print ('Chunk ' + str(x) + ' size: ' + str(len(sliceObj)) )
        chunks.append(sliceObj)
        idBeg = pEnd
        idEnd = pEnd + size
    
    #create processes (threads), one for each slice
    jobs = []
    index = 0
    for chunk in chunks:
        p = Process(target = worker, args = (chunk, train, K, index))
        jobs.append(p)
        p.start()
        index += 1

    #waits all processes to terminate
    for p in jobs:
        p.join()
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# MAIN
#-------------------------------------------------------------------------------
if __name__== "__main__":

    import sys
    # read the training set
    train = ctrlCSV(sys.argv[1])
    # read the testing set
    test = ctrlCSV(sys.argv[2])
    #defines the K factor for the KNN
    K = int(sys.argv[3])
    #defines the number of slices for multiprocessing
    nrSlices = int(sys.argv[4])

    # time to check performance
    import time
    time_start = time.time()

    # run the code!
    run (test, train, K, nrSlices)

    # gets all csv output files and merge in just one file
    test.mergeCSV(nrSlices) 

    # finish
    time_end = time.time()
    print ("Done in %d "  %(time_end-time_start) + "seconds.\n")
#-------------------------------------------------------------------------------
