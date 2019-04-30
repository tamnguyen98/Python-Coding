import pymysql
import csv
import json
import sys
import warnings


schemaName = "cs351" # Database name
queriesSQLFile = './Queries.sql' # File to the queries code
tableSQLFile = './CreatingTable.sql' # File to the table creation code
csvDb = './tmdb_5000_movies.csv' # File to the database

uniqueList = set() # Our list to prevent dupes of sub tables (Generes,etc.). Using list since it's quicker than list when our db is big
createTableSQL = [] # List of commands to create tables
queriesOption = [] # List of querries commands

# -------------------------- Get SQL Code From File -------------------------- #

def readSQLfile(src, fileName):
	try:
		createTableSql = open(fileName, "r")
	except IOError:
		print("Error: Opening file")
		quit()

	onCodeChunk = False
	code2exec = ""
	for line in createTableSql:
		line = line.rstrip().replace('\t', ' ')
		if (line) and not onCodeChunk:
			onCodeChunk = True
			code2exec = line
			if (';' in line):
				src.append(code2exec)
				onCodeChunk = False
		elif onCodeChunk:
			code2exec += ' ' + line
			if ";" in line:
				src.append(code2exec)
				onCodeChunk = False
	createTableSql.close()

# ------------------------------ Create Db Table ----------------------------- #

def createTable():
	if not createTableSQL:
		readSQLfile(createTableSQL, tableSQLFile)
		createTable()
	for cmd in createTableSQL:
		try:
			cur.execute(cmd)
		except pymysql.MySQLError as e:
			print("Error {0}: {1}".format(e.args[0], e))
	conn.commit()
# ---------------------- Insert Tuples Into Movies Table --------------------- #

def insertToTable():
	with open(csvDb, encoding="utf8") as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 1
		for row in csv_reader: # Each tuple, Row is an array/list so you gotta access it like [i]
			if line_count == 1: # we dont care about this
				line_count += 1 #it's only contain attribute name
			else:
				'''
				index 1,4,9,10,14 are new tables
				Genres = 1
				keywords = 4
				productionCo = 9
				productionCountry = 10
				languages = 14
				'''
				
				insertCode = "INSERT IGNORE INTO movies (budget, homepage, id, orig_language, title, overview, popularity, release_date, revenue, runtime, movieStatus, tagline, vote_avg, vote_count) VALUES"
				insertCode += " ({0}, \'{1}\', {2}, \'{3}\', \'{4}\', \'{5}\', {6}, \'{7}\', {8}, {9}, \'{10}\', \'{11}\', {12}, {13});".format(row[0], row[2], row[3], row[5], row[6].replace('\'','\\\''), row[7].replace('\'','\\\''), row[8], row[11], row[12], row[13] if row[13] else 0, row[15], row[16].replace('\'','\\\''), row[18], row[19])	

				cur.execute(insertCode) # Executing the sql code
				# Follow are non Atomic attributes, so we have to do extra work to get them into 2NF #
				insertToRelationTable( "genresRelation", row[1], row[3], False) # pass the non atomic attributes to be parsed
				insertToRelationTable( "keywordsRelation", row[4], row[3], False)
				insertToRelationTable( "productionCoRelation", row[9], row[3], False)
				insertToRelationTable( "productionCountryRelation", row[10], row[3], True)
				insertToRelationTable( "languagesRelation", row[14], row[3], True)
				line_count += 1
		conn.commit() # Commit the changes

# --------- Insert Tuples Into Relation Table --------- #

def insertToRelationTable(newTableName, tupleJson, movieId, isCountry):
	tupleJson = json.loads(tupleJson) # Break up the attribute to accessible objs
	if not tupleJson or not movieId: # If attribute is empty or missing movieId
		return
	for obj in tupleJson:
		if obj:
			keyName = list(obj.keys()) # This let use the the key name, since the db have iso_x
			tmpTuple = (obj[keyName[0]], obj[keyName[1]]) # convert it to a python's tuple
			if tmpTuple not in uniqueList: # check to see if it's not a dupe
				insertToSubTable( newTableName, obj, keyName, isCountry)
				uniqueList.add(tmpTuple)
			if isCountry and obj[keyName[0]]: # Make sure we're dealing with the iso_x
				insertCode = "INSERT INTO %s (movieId, abbrev) VALUES (%s, \'%s\');" % (newTableName, movieId, obj[keyName[0]]) # We're using keyname because the key switches if you look at the csv
			elif not isCountry and obj["id"]: # Since other element uses the same id/name key name
				insertCode = "INSERT INTO %s (movieId, itemID) VALUES (%s, %s);" % (newTableName, movieId, obj["id"])	# not all genres relation are geting added	
			try:
				cur.execute(insertCode)
			except pymysql.MySQLError as e:
				print("Error {0}: {1}".format(e.args[0], e))

# -------------- Insert Tuples Into Genre, Keywords, etc. Table -------------- #

def insertToSubTable(newTableName, tupleObj, keys, isCountry): #To insert into the genre, keyword, etc. table
	newTableName = newTableName.replace("Relation", "")
	if (isCountry):
		insertCode = "INSERT IGNORE INTO %s (sName, lName) VALUES (\'%s\', \'%s\');" % (newTableName, tupleObj[keys[0]], tupleObj[keys[1]].replace('\'', '\\\'')) #ignore key will prevent dupes
	else:
		insertCode = "INSERT IGNORE INTO %s (id, info) VALUES (%s, \'%s\');" % (newTableName, tupleObj["id"], tupleObj["name"].replace('\'', '\\\''))

	cur.execute(insertCode) # Don't need to catch exceptions since we have IGNORE into our code


# ------------------------------ Queries Option ------------------------------ #

def qOptions(opt):
	if not queriesOption: # Check to see if we have our commands available
		readSQLfile(queriesOption, queriesSQLFile)
	if opt > len(queriesOption): # Make sure the user input is in range
		print("Error: Can't find command %d, double check %s" % (opt, queriesSQLFile))
	
	if opt == 0: # Do all
		for cmd in queriesOption:
			execQuer(cmd)
			print('')
	else:
		execQuer(queriesOption[opt-1])
	conn.commit()
	
def execQuer (cmd):
	try:
		cur.execute(cmd)
		tuples = cur.fetchall()
		if cur.rowcount > 0:
			for t in tuples:
				print(t)
	except pymysql.MySQLError as e:
		print("Error {0}: {1}".format(e.args[0], e))

# ----------------------------------- Main ----------------------------------- #

conn = pymysql.connect(host='localhost', port=3306, user=sys.argv[1], passwd=sys.argv[2], db = schemaName)
cur = conn.cursor()

createTable()
insertToTable()

argc = len(sys.argv)
if not (argc <= 4 and argc >= 3): # check to see if user give 2-3 args
	print("Erorr: Invalid execution, please see README.")
	quit()

if argc == 4:
	qopt = int(sys.argv[3])
else:
	qopt = 0
qOptions(qopt)
conn.close() 
cur.close()