import json
import csv
import sys
from sets import Set
global emp_data
global AuthorNames
global association
global output_matrix

#proc : To get the full name of author from the json format
def getFullAuthorName(author):
    name = author["ForeName"] + ' ' + author["LastName"]
    return name
  
#proc : To get the list of all the Authors (unique entries), and associate these with an id
def getAuthors():
    AuthList = []
    for i in range(0,len(emp_data)):
        aList = emp_data[i]['AuthorList']['Author']
        for j in range(0,len(aList)):
            AuthList.append(getFullAuthorName(aList[j]))
    AuthNames = list(Set(AuthList))
    AuthNames.sort()
    for i in range(0, len(AuthNames)):
        association[AuthNames[i]] = i+1
    return AuthNames

#proc : Initialize Output Matrix, Set First row and column as Author Names	
def initializeMatrix(AuthorNames):
    for i in range(0,len(association)+1):
        output_matrix.append([0] * (len(association)+1))
	output_matrix[0][0]= ""
    for i in range(0,len(association)):
        output_matrix[0][i+1] = AuthorNames[i]
        output_matrix[i+1][0] = AuthorNames[i]

#proc : Print the Output Matrix		
def printMatrix():
    for i in range(0,len(output_matrix)):
        print "\n"
        for j in range(0,len(output_matrix)):
            print str(output_matrix[i][j])+"\t",
		
#proc : Get the count of Author-CoAuthor association and update the matrix
def getAuthorCoauthorData():
    for i in range(0,len(emp_data)):
        aList  =  emp_data[i]['AuthorList']['Author']
        AuthorIds = []	
        for j in range(0,len(aList)):
            auth_name = getFullAuthorName(aList[j])
            AuthorIds.append(association[auth_name])
        for k in AuthorIds:
            for m in AuthorIds:
                output_matrix[k][m] = output_matrix[k][m] + 1

#proc : main proc to call all other procs
def main():
    AuthorNames = getAuthors()
    initializeMatrix(AuthorNames)
    getAuthorCoauthorData()
    printMatrix() 
    
if __name__ == '__main__':
    #check if valid arguments (json input file) are passed
    if len(sys.argv) > 1: 
        #load the json file to a variable	
        json_data = json.load(open(sys.argv[1],'r'))
        emp_data = json_data['MedlineCitationSet']['Article']
    else:
        print "Too few arguments.. Please add the required arguments and try again"
    association = {}
    output_matrix = []
    AuthorNames = []		
    main()
