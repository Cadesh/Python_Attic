
import csv

#----------------------------------------------------------------------------------------
# CLASS CTRLCSV
#----------------------------------------------------------------------------------------
class ctrlCSV:

    #----------------------------------------------------------------------------
    # INIT LOAD THE CSV FILE
    # Class constructor
    #----------------------------------------------------------------------------
    def __init__ (self, fileName):

        self.row = []   #attribute shared to all instances (static)
        with open(fileName) as csvfile:

            reader = csv.DictReader(csvfile)
            for r in reader:
                self.row.append(r)

        # deletes the two first lines because they are just labels
        del self.row[0]
    #----------------------------------------------------------------------------

    #----------------------------------------------------------------------------
    # SAVE A LIST PASSED AS PARAMETER TO A CSV FILE
    # Each process saves a temporary csv file
    #----------------------------------------------------------------------------
    def saveCSV (self, pList, idx):
        fileName = 'out_' + str(idx) + '.out'
        with open(fileName, 'w') as outCSV:
            wr = csv.writer(outCSV, quoting=csv.QUOTE_ALL)
            for row in pList:
                wr.writerow(row)
    #----------------------------------------------------------------------------

    #----------------------------------------------------------------------------
    # RETURNS THE NUMBER OF ROWS IN THE DATA MEMBER LIST
    #----------------------------------------------------------------------------
    def countRow(self):
        return len(self.row)
    #----------------------------------------------------------------------------

    #----------------------------------------------------------------------------
    # RETURNS A LIST CONTAINING ONLY A SLICE OF THE CURRETN LIST
    # PARAMETERS - index begin, index end, of the slice to be returned 
    #----------------------------------------------------------------------------
    def getSlice (self, idBegin, idEnd):
        return self.row[idBegin: idEnd]
    #----------------------------------------------------------------------------

    #----------------------------------------------------------------------------
    # RETURN THE DATA MEMBER LIST
    #----------------------------------------------------------------------------
    def getList (self):
        return self.row
    #----------------------------------------------------------------------------

    #----------------------------------------------------------------------------
    # MERGE ALL OUTPUT FILES
    # Each process creates a csv file that now will be merged in a single file
    #----------------------------------------------------------------------------
    def mergeCSV(self, slices):
        # merge in one file and delete the rest
        import os
        # careful, "a" means 'add'. If there is a file with the same name it will concatenate data
        fout=open("output_KNN.csv","a")
        for num in range(slices):
            fileName = "out_" + str(num) + ".out"
            fin=open(fileName)
            for line in fin:
                fout.write(line)  
            fin.close()
            os.remove(fileName) 
        fout.close()
    #-----------------------------------------------------------------------------

#----------------------------------------------------------------------------------------

