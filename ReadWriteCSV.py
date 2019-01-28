

# 1. Read the CLEAN Votes, sjut load the names of videos
CLEAN = [] # list of test videos
    # 1. Load the list of videos
f1 = open('CLEAN_WeightedVotes.csv', 'r')
for line in f1:
    tmp = line.split(',')[0].replace('"','')
    if (tmp[-3:] == 'mp4'): # deletes the .mp4 from the back of the name
        tmp = tmp[:-4]
    CLEAN.append(tmp)
f1.close()    
print ("Number of CLEAN lines:" + str(len(CLEAN) ) )

# 2. Read the unclean votes
UNCLEAN = [] # list of test videoss
f2 = open('KNN10_voting.csv', 'r')
for line in f2:
    tmp = line.replace('"','')
    tmp = tmp.rstrip('\n') #eliminate the /n from the back of the string
    words = tmp.split(",")
    if (words[0][-3:] == 'mp4'): # deletes the .mp4 from the back of the name
        words[0] = words[0][:-4]
    UNCLEAN.append(words)
f2.close()    
print ("Number of UNCLEAN lines:" + str(len(UNCLEAN) ) ) 

# 3. Filter the  to get only the videos present in CLEAN
NEW = []
for cl in CLEAN:
    for un in UNCLEAN:
        if (cl == un[0]):
            NEW.append (un)

print ("Number of NEW lines:" + str(len(NEW) ) + " (must be the same of CLEAN)" ) 

# 4. Save the new CLEAN_UnweightedVotes 
csvLn = []
for ln in NEW:
    strTemp = ''
    for val in ln: 
        strTemp += val + ','
    strTemp [:-1] # deletes the last comma from the end of the line
    strTemp += '\n' # adds the break line
    csvLn.append(strTemp)

# 5. Save the file
f = open ('CLEAN_UnweightedVotes.csv', 'w')
for any in csvLn:
    f.write(any)
f.close()
