import sys # Use to read arguments for file location

################################################################################################
# Assignment 4                                                                                 #
# Class: CS 351                                                                                #
# Coder: Tam Nguyen                                                                            #
# Summary of assignment: "In this assignment you will be creating a bitmap index from          #
# a data file containing information about pets and whether they are adopted or not.           #
# Once you create the bitmap, it needs to be compressed using WAH with 32 and 64 Bit words."   #
# NOTICE: format of the data file must be in the following format:                             #
# Species (cat dog turtle bird), Age (0-100), Adopted? (True/False)                            #
################################################################################################

# format of the bitmap data:
# cat dog turtle bird 10's 20's 30's 40's .. 90's yes no

sorteBitmapdStr = "_bitmap_sorted" # For easy and quick edit output extension
bitMapStr = "_bitmap" # We're not going to add the extension because a function will add its own extension when done with it

##########################
#     Path Parser        #
##########################
def removeFileExt(filePath):
    try:
        name = filePath.rsplit('.')
        if (len(name) > 1 and name[len(name)-1][0] != '\\'):
            for i in range(1, len(name)-1):
                name[0] += '.'
                name[0] = name[0] + name[i]
        return name[0]
    except AttributeError:
        return ""

###########################
#        Conversion       #
##########################
def convToBitmap(dbTuple):
    data = dbTuple.split(',')
    bitmap = ""

    # Determine animal
    if (data[0].lower() == "cat"):
        bitmap = "1000"
    elif (data[0].lower() == "dog"):
        bitmap = "0100"
    elif (data[0].lower() == "turtle"):
        bitmap = "0010"
    elif (data[0].lower() == "bird"):
        bitmap = "0001"
    
    # Determine
    age = ""
    tmpMax =int(data[1]) # Determine where to set 1. It will give us a decimal
    for i in range(1,101, 10):
        if (tmpMax < i+10 and tmpMax >= i):
            age += '1'
        else:
            age += '0'
    bitmap += age # Concat those two

    if (data[2].lower() == "false"):
        bitmap += "01"
    else:
        bitmap += "10"

    return bitmap+'\n'
###########################
#        Compression     #
##########################
def WAHCompression (bits, bitmapFile, originalDataName): 
    lines = []
    try:
        outputFile = open(originalDataName+"_compressed_"+str(bits)+".txt", 'w')
    except FileNotFoundError:
        print("Compression ERROR: Can't create new compression file")
        return
    try:
        with open(bitmapFile) as f:
            for line in f:
                lines.append(line.rstrip())
    except FileNotFoundError:
        print("Compression ERROR: Can't locate bitmap file")
        return

    if not lines:
        print('Error occur: Unable to read bitmap file...')

    cols = []
    for col in list(zip(*lines))[::-1]: # get each column of the file and rotate it to  be rows
        cols.append(''.join(col)) # after it get all of bits in a column, combine all of it to a long string and add it to our cols array 

    runsOf1 = "".rjust(bits-1, '1') # Our runs of 1
    runsOf0 = "".rjust(bits-1, '0')

    for row in reversed(cols): # the last operation add our first column to the last spot in the array, so now we have to flip it
        word = ''
        bitCount = 0
        runCount = [0,'0'] # [run count, what was the last run]
        for i in row:
            if bitCount < bits-1: # Making our word
                word = word + i
                bitCount += 1
            else: # At 31st bit
                if (word == runsOf0): # Check to see if it's a run of 0
                    if (word[2] == runCount[1]): # If this is the same run as last one
                        runCount[0] += 1 # Increment that value
                    else :
                        checkIfNewRun(runCount, outputFile, word, 1, bits) # The title explains it...
                elif (word == runsOf1): # Do the same but for runs of 1
                    if (word[2] == runCount[1]):
                        runCount[0] += 1
                    else :
                        checkIfNewRun(runCount, outputFile, word, 1, bits)
                else: # If this is a literal
                    checkIfNewRun(runCount, outputFile, word, 0, bits) # We gonna check if we just break from a run
                    outputFile.write('0'+word) # Save our literal
                word = ""+i # Reset out literal
                bitCount = 1 # Reset out counter
        if bitCount > 0: # If there were any bits left
            checkIfNewRun(runCount, outputFile, word, 0, bits) # We gonna check if we just break from a run
            outputFile.write('0'+word) # Save the remaining as literal with no padding.
        outputFile.write('\n')
    outputFile.close()

def checkIfNewRun(runCount, outputFile, word, resetTo, bits):
    if runCount[0] > 0: # Check to see if the we were working on run that had multiple consecutive occurance
        if (bits == 64):
            outputFile.write('1'+runCount[1]+'{0:062b}'.format(runCount[0])) # Compress it if it there was
        else:
            outputFile.write('1'+runCount[1]+'{0:030b}'.format(runCount[0])) # Compress it if it there was
        #outputFile.write('1'+runCount[1]+'{0:030b}'.format(runCount[0])) # Compress it if it there was
    runCount[0] = resetTo # reset our counter/flag
    runCount[1] = word[2] # Mark the start of new run

################################################
#               Main                           #
################################################

argc = len(sys.argv)
nosort = False
##### Check Arguments for flag and compression value #####
if argc == 4:
    if sys.argv[1] == "-nosort":
        nosort = True
    else:
        print("Error: Unrecognize flag...\n\tDid you mean to type: py Main.py -nosort <path/file> <32/64 (optional)>")
        sys.exit(-1)
elif argc == 1 or argc > 3:
    print("Error: Invalid arguments. To run try:")
    print("\tpy Main.py <path/Datafile.type> <32/64 (bit compression)>")
    sys.exit(0)
if argc == 2:
    bitsCompression = 0
else:
    if (not nosort and sys.argv[1] == "-nosort"):
        nosort = True
        bitsCompression = 0
    else:
        try:
            if nosort:
                bitsCompression = int(sys.argv[3])
            else:
                bitsCompression = int(sys.argv[2])
        except ValueError:
            print("Error: Invalid 2nd arguments. To run try:")
            print("\tpy Main.py <path/file.type> 32")
            sys.exit(-1)

if bitsCompression != 32 and bitsCompression != 64 and bitsCompression != 0: # Only allow 32/64
    print("Please enter either 32/64 bit compression or none (for both).")
    sys.exit(-1)    

if not nosort:
    dataFileName = sys.argv[1]
else:
    dataFileName = sys.argv[2]    
try:
    dataFile = open(dataFileName, "r")
except FileNotFoundError:
    print("Conversion ERROR: Can't locate data file.")
    sys.exit(-1)

appendDataName = str(removeFileExt(dataFileName)) # the string of the file without the extention that is appendable

##### Converting the original data file to bitmap value #####
bitmapFilename = appendDataName+bitMapStr+'.txt'
outputFile = open(bitmapFilename, "w")
toBeSortedData = [] # Assignment instructs us to sort the data too.
for dbTuple in dataFile:
    bitval = convToBitmap(dbTuple.rstrip())
    outputFile.write(bitval)
    toBeSortedData.append(dbTuple)

dataFile.close()
outputFile.close()

##### Check to see if user want to make sort the data file #####
if not nosort:
    toBeSortedData.sort()
    sortedFileName = appendDataName+sorteBitmapdStr+'.txt'
    sortedOutputFile = open(sortedFileName, "w")
    for dbTuple in toBeSortedData: # Store all of them to a text file.
        sortedOutputFile.write(convToBitmap(dbTuple.rstrip()))
    sortedOutputFile.close()

##### Start compressing the bitmaps #####
if (bitsCompression == 0):
    WAHCompression(32,bitmapFilename, appendDataName)
    WAHCompression(64,bitmapFilename, appendDataName)
    if not nosort:
        WAHCompression(32,sortedFileName, appendDataName+sorteBitmapdStr)
        WAHCompression(64,sortedFileName, appendDataName+sorteBitmapdStr)
else:
    WAHCompression(bitsCompression,bitmapFilename, appendDataName)
    if not nosort:
        WAHCompression(bitsCompression,sortedFileName, appendDataName+sorteBitmapdStr)