import numpy

def minDistance(targetString, sourceString):
    """
    Takes in Strings and return Minimum Distance Matrix and Minimum Distance
    """
    targetLength = len(targetString)
    sourceLength = len(sourceString)

    distance = numpy.zeros((targetLength+1,sourceLength+1))
    distance[0][0] = 0
    
    for i in range(targetLength,-1,-1):
      distance[i][0] = targetLength - i
    
    for j in range(0,sourceLength+1,1) :
      distance[targetLength][j] = j

    for i in range(targetLength,0,-1):
      for j in range(0,sourceLength,1):

        leftDistance = distance[i-1][j] + 1 
        upDistance = distance [i][j+1] + 1

        if (targetString[targetLength - i] == sourceString[j]): 
          diagDistance = distance [i][j] 
          
          distance[i-1][j+1] = min(leftDistance,upDistance,diagDistance)

        else:
          diagDistance = distance[i][j] + 2 
          distance[i-1][j+1] = min(leftDistance,upDistance,diagDistance)

    # print(distance)
    # print(distance[0][sourceLength])
    return (distance,distance[0][sourceLength])

def backTrace(distanceMatrix,targetString,sourceString):
  rowSize = len(distanceMatrix) 
  colSize = len(distanceMatrix[0])
  backTraceArray =[]
  backTraceStep=[]

  i = 0
  j = colSize-1
  rotateBoolean = True
  while True:
    testDistance = distanceMatrix[i][j]
    diagDistance = distanceMatrix[i+1][j-1]
    leftDistance = distanceMatrix[i][j-1]
    downDistance = distanceMatrix[i+1][j]
    tempArray = backTraceArray
    backTraceArray = [testDistance] + tempArray

    tempArray = backTraceStep
    if ((targetString[rowSize-i-2] == sourceString[j-1])):
      i+=1
      j-=1
      backTraceStep = ["Maintain"] + tempArray
    elif((testDistance==(diagDistance+2))):
      i+=1
      j-=1
      backTraceStep = ["Sub"] + tempArray
    elif((testDistance==(leftDistance+1)) & (testDistance==(downDistance+1))):
      if(rotateBoolean):
        rotateBoolean = False
        backTraceStep = ["Del"] + tempArray
        i+=1
      else:
        rotateBoolean = True
        backTraceStep = ["Ins"] + tempArray
        j-=1
    elif(testDistance==(leftDistance+1)):
      j-=1
      backTraceStep = ["Ins"] + tempArray
    else:
      backTraceStep = ["Del"] + tempArray
      i+=1
    
    if((i>(len(targetString)-1))|(j<0)):
      print("BackTraceArray:",backTraceArray)
      print("BackTraceStep:",backTraceStep)
      return backTraceArray