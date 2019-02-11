# AUTHOR: Andre Rosa
# DATE: 09 FEB 2019
# OBJECTIVE: A generic calculator for Precision and Recall
# The program work with two csv files that contain a videoName as first column and 
# a list of booleans for the rest of columns. 

# to run the code: python CalcPR.py groundTruthFile.csv Estimate.csv [list of categories]
# if no list of categories the code will consider all categories

import csv
import os  # for the runtime exit
import sys # for arguments input
from Categories import NewCat

#-------------------------------------------------------------------
# CLASS LINE HOLDS EACH VIDEO NAME AND RELATED CATEGORIES
# this class represents each line from the csv file, the first field is the name of the video 
# while the categories is a list of booleans 0,1
#-------------------------------------------------------------------
class Line:

    NR_CATEGORIES = 0 #static variable to hold the number of categories

    def __init__(self, name, categories):
        self.name = name
        self.categories = categories
        
        Line.NR_CATEGORIES = len(categories)
    
    def isCategory (self, catIndex):  # Return true if video belongs to category
        ''' Return the boolean value for the category '''

        return bool(self.categories[catIndex])

    def getVidName (self):
        return self.name

    def getCategories (self):
        return self.categories

    def getNumberofCategories (self):
        ''' Return the number of categories in a line '''
        return len(self.categories)
#-------------------------------------------------------------------

#-------------------------------------------------------------------
# USED TO SHOW COLOR IN TERMINAL
#-------------------------------------------------------------------
class sysColor:
    Red = '\033[91m'
    Green = '\033[92m'
    Blue = '\033[94m'
    Cyan = '\033[96m'
    White = '\033[97m'
    Yellow = '\033[93m'
    Magenta = '\033[95m'
    Default = '\033[99m'
#-------------------------------------------------------------------

#-------------------------------------------------------------------
# READ A CSV FILE AND SAVES IN A LIST DATA STRUCTURE
#-------------------------------------------------------------------
def readCSVFile (fileName):
    ''' Read the csv file and saves in a list structure '''

    lList = []
    lBolCat = [] # a list of booleans for categories 

    # read the file and fill the video list
    with open(fileName) as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
                line_count += 1

                vidName = row[0]  # save video name (position [0] in the row)
                for i in range (1, len(row)):
                    lBolCat.append(int(row[i]) ) # append the boolean to the list

                lLine = Line (vidName, lBolCat[:]) # create a line object, use the [:] to pass the variable by value
                lList.append(lLine) # append the line object to the list of videos
                lBolCat.clear() # clear the list

        print(f'Processed from {fileName} ' + sysColor.Green + str(line_count) + sysColor.White + ' lines.')
        return lList
#-------------------------------------------------------------------

#-------------------------------------------------------------------
# CHECK IF THE STRUCTURE (ROWS AND COLUMNS) ARE THE SAME ON BOTH FILES
#-------------------------------------------------------------------
def checkStructure (testVid, catVid):
    ''' Check if two csv files have the same number of columns and rows ''' 
    isOK = False
    tRow = len(testVid) # number of rows
    cRow = len(catVid)

    if ((tRow > 0) and (tRow == cRow)): # if they have the same number of rows
        if (testVid[0].getNumberofCategories() == catVid[0].getNumberofCategories()):
            isOK = True
    
    return isOK
#-------------------------------------------------------------------

#-------------------------------------------------------------------
# CHECK IF THE ARGUMENTS ARE OK
#-------------------------------------------------------------------
def checkArguments(args):
    ''' Check the validity of the arguments passed. '''

    if (len(args) == 1 ): # number of arguments is ok?
        print(sysColor.Red + 'ATTENTION:' + sysColor.White + ' Invalid number of arguments, type "CalcPR --help" for help.')
        return False

    if (args[1] == '--help'): # calls help
        print(sysColor.Green + 'Use the following arguments:\n' +  
                  sysColor.Green + '1' + sysColor.White + ' - csv file with ground truth.\n' + 
                  sysColor.Green + '2' + sysColor.White + ' - csv file with estimation to be evaluated.\n' + 
                  sysColor.Green + '3' + sysColor.White + '... - name of categories to test (separated by spaces).\n' +
                  sysColor.Yellow + 'If no category is selected the program runs all categories' + sysColor.White )
        return False

    suffix = '.csv'
    if (not( (args[1].endswith(suffix) == True) and (args[2].endswith(suffix) == True) )): # check if the files are csv files
        print (sysColor.Red + 'ATTENTION:' + sysColor.White + ' First and second arguments must be .csv files')
        return False

    return True
#-------------------------------------------------------------------

#-------------------------------------------------------------------
#
#-------------------------------------------------------------------
def getCategoriesToRun(args):

    from Categories import NewCat
    bolCats = []

    for i in range (0,Line.NR_CATEGORIES): # fill the categories list with falses
        bolCats.append (False)

    #get the categories passed as paremeters in terminal
    cats = args[3:] # the arguments 3 and onwards are the categories
    
    if (len(cats) >= 1 ): 
        print ('Categories selected: ' + sysColor.Blue + str(cats) + sysColor.White)
        for cat in cats:
            # 1. check if category name exist in  list and get the index
            for i in range (0, len(NewCat) ):
                if (cat == NewCat[i]):
                    bolCats[i] = True

    else: # no category selected do all categories
        print ('All categories selected')
        for i in range (0,Line.NR_CATEGORIES): # fill the categories list iwth falses
            bolCats[i] = True
    
    return bolCats
#-------------------------------------------------------------------

#-------------------------------------------------------------------
# CLEAR THE TERMINAL SCREEN
# platform.system() identifies the OS 'Linux', 'Windows' or 'Darwin'(for MacOS)
#-------------------------------------------------------------------
def clearTerminal():
    import platform
    if ( platform.system() == 'Windows'): os.system('cls')
    else: os.system('clear')
#-------------------------------------------------------------------

#-------------------------------------------------------------------
def execute ():

    clearTerminal()

    # 0. Test the arguments
    if (checkArguments(sys.argv) == False):
        os._exit(1)

    # 1. read the GROUND TRUTH csv
    #print ('1. Load file with ground truth.')
    testVid = readCSVFile (sys.argv[1]) # ("TestBOOLEANGroundTruth.csv") 

    # 2. Read the ESTIMATED CATEGORIES csv
    #print ('2. Load file with estimated categories.')
    cateVid = readCSVFile (sys.argv[2]) # ("TestBOOLEANUnWeightVote.csv")

    # 3. Test if structure (number of columns and rows) of both files are the same
    #print ('3. Checking if both files have the same number of categories.')
    if ( checkStructure (testVid, cateVid) == False):
        print (sysColor.Red + 'ATTENTION:' + sysColor.White + ' Files do not have the same number of columns and rows!' )
        os._exit(1)

    # 4. Get list of categories to test, the return is a list of booleans with the categories to calculate
    #print ('4. Get category list.')
    print (sysColor.Red + "number of categories " + str(Line.NR_CATEGORIES) + sysColor.White)
    categoryToRun = getCategoriesToRun (sys.argv)
    
    RE_List = [] #relevant result list
    TP_List = [] #true positive list
    FP_List = [] #false positive list
    precision = [] #to store the results of the precision
    recall = [] #to store the result of the racll calculation
    fScore = [] #to store the F1 Score
    catNames = [] #saves the names of the selected categories for 

    # 5. For each Category
    for index in range (0,Line.NR_CATEGORIES): # loop the number of categories
        
        if (categoryToRun[index] == True): # if the category was selected then calculate

            currentCat = NewCat[index]
            catNames.append(currentCat) # save the category name for later use

            # 5.0 loop to find the number of relevant occurences for each category
            #----------------------------------------------------------------
            relevantElements = 0 
            #loop to sum all relevant elements
            for vid in testVid:
                if (vid.isCategory(index) == True):  
                    relevantElements += 1
            print(f'Relevant elements found for category {currentCat} -> {relevantElements} ')
            RE_List.append(relevantElements * 1.0) #multiplying by 1.0 to save a float value for later calculations     
            #----------------------------------------------------------------

	        #5.1. loop to find the true positives - category exist in both vote and test
            #----------------------------------------------------------------
            truePositives = 0 
            #loop to sum all relevant elements
            for i in range (0, len(cateVid) ):
                if ((testVid[i].isCategory(index)==True) and (cateVid[i].isCategory(index)==True)):
                    truePositives += 1
            print(f'True Positives found for category {currentCat} -> {truePositives} ')
            TP_List.append(truePositives * 1.0) #multiplying by 1.0 to save the float value
            #----------------------------------------------------------------   

	        #5.2 loop to find the false positives - category exist in vote but not in test
            #----------------------------------------------------------------
            #loop to find the false positives - category exist in vote but not in test
            falsePositives = 0 
            #loop to sum all relevant elements
            for i in range (0, len(cateVid) ):
                if ((testVid[i].isCategory(index)== False) and (cateVid[i].isCategory(index) == True)):
                    falsePositives += 1
            print(f'False Positives found for category {currentCat} -> {falsePositives} ')
            FP_List.append(falsePositives * 1.0) #multiplying by 1.0 to save the float value
        #----------------------------------------------------------------

	#6. Calculates precision and recall for each category
    for i in range(len(FP_List)):
        if (TP_List[i] != 0):
            precision.append(100.0 * TP_List[i] / (TP_List[i] + FP_List[i])) 
            recall.append(100.0 * TP_List[i] / RE_List[i])
        else:
            precision.append(0.0)
            recall.append(0.0)

    #7. Calculate the fScore
    for i in range(len(FP_List)):
        if (TP_List[i] != 0):
            fScore.append( 2 * (precision[i] * recall[i]) / (precision[i] + recall[i]) )
        else:
            fScore.append (0.0)

    for i in range(len(precision)):
        print (f'Category: {catNames[i]} - precision: {precision[i]} - recall: {recall[i]} ')

	#8. save output to file
    #--------------------------------------
    catNames.insert(0, "CATEGORIES")
    precision.insert(0, "precision")
    recall.insert(0, "recall")
    fScore.insert(0, "f_score")
    myData = [catNames, precision, recall, fScore]  
    myFile = open('PR_output.csv', 'w')  
    with myFile:  
        writer = csv.writer(myFile)
        writer.writerows(myData)
    catNames.pop(0)
    precision.pop(0)
    recall.pop(0)
    fScore.pop(0)
    #--------------------------------------

    #saves the report in another file
    catNames.insert(0, "CATEGORIES")
    RE_List.insert(0, 'relevant')
    TP_List.insert(0, 'true_positives')
    FP_List.insert(0, 'false_positives')
    myData = [catNames, RE_List, TP_List, FP_List]  
    myFile = open('report.csv', 'w')  
    with myFile:  
        writer = csv.writer(myFile)
        writer.writerows(myData)
    catNames.pop(0)
    RE_List.pop(0)
    TP_List.pop(0)
    FP_List.pop(0)

    #now saves precision and recall in a csv file (A NEW FORMAT TO GENERATE A DIAGRAM EASIER)
    # Save in the csv file
    text_file = open("outputForGraph.csv", "w")
    for i in range(len(precision)):
        text_file.write(catNames[i] + ',' + str(precision[i]/100) + ','+ str(recall[i]/100) + ',' + str(fScore[i]/100) + '\n')
    text_file.close()

def main ():
    execute()

main()
