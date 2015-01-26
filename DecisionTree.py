from math import log

class Node:
  """
  A simple node class to build our tree with. It has the following:
  
  children (dictionary<str,Node>): A mapping from attribute value to a child node
  attr (str): The name of the attribute this node classifies by. If this is a leaf node, then None.
  value (str): If this is a leaf node, then a final value for the label. Otherwise, None.
  """
  
  def __init__(self):
    self.children = {}
    self.attr = None
    self.value = None
    
class Tree:
  """
  A generic tree implementation with which to implement decision tree learning.
  Stores the root Node and nothing more. A nice printing method is provided, and
  the function to classify values is left to fill in.
  """
  def __init__(self, root=None):
    self.root = root

  def prettyPrint(self):
    print str(self)
    
  def preorder(self,depth,node):
    if node is None:
      return '|---'*depth+str(None)+'\n'
    if node.attr is None or node.value is not None :
      return '|---'*depth+str(node.value)+'\n'
    string = ''
    for val in node.children.keys():
      childStr = '|---'*depth
      childStr += '%s = %s'%(str(node.attr),str(val))
      string+=str(childStr)+"\n"+self.preorder(depth+1, node.children[val])
    return string    

  def count(self,node=None):
    if node is None:
      node = self.root
    if node.value is not None:
      return 1
    count = 1
    for child in node.children.values():
      if child is not None:
        count+= self.count(child)
    return count  

  def __str__(self):
    return self.preorder(0, self.root)
  
  def classify(self, classificationData):
    """
    Uses the classificatier tree with the passed in classificationData.`
    
    Args:
        classificationData (dictionary<string,string>): dictionary of attribute values
    Returns:
        str
        The classification made with the classification tree.
    """
    #YOUR CODE HERE
    if self.root.attr == None:
        return self.root.value
    subTree = Tree( self.root.children[classificationData[self.root.attr]] )
    return subTree.classify(classificationData)
  
def getPertinentExamples(examples,attrName,attrValue):
    """
    Helper function to get a subset of a set of examples for a particular assignment 
    of a single attribute. That is, this gets the list of examples that have the value 
    attrValue for the attribute with the name attrName.
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrName (str): the name of the attribute to get counts for
        attrValue (str): a value of the attribute
        className (str): the name of the class
    Returns:
        list<dictionary<str,str>>
        The new list of examples.
    """
    newExamples = []
    #YOUR CODE HERE
    for example in examples:
        if example[attrName] == attrValue:
            newExamples.append(example)
    return newExamples
  
def getClassCounts(examples,className):
    """
    Helper function to get a list of counts of different class values
    in a set of examples. That is, this returns a list where each index 
    in the list corresponds to a possible value of the class and the value
    at that index corresponds to how many times that value of the class 
    occurs.
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        className (str): the name of the class
    Returns:
        list<int>
        This is a list that for each value of the class has the count
        of that class value in the examples.
    """
    classCounts = {}
    #YOUR CODE HERE
    for example in examples:
        classValue = example[className]
        if classValue not in classCounts.keys():
            classCounts[classValue] = 0
        classCounts[classValue] += 1
    return classCounts.values()
  
def getAttributeCounts(examples,attrName,attrValues,className):
    """
    Helper function to get a list of counts of different class values
    corresponding to every possible assignment of the passed in attribute. 
	  That is, this returns a list of lists, where each index in the list 
	  corresponds to an assignment of the attribute named attrName and holds
 	  the counts of different class values for the subset of the examples
 	  that have that assignment of that attribute.
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrName (str): the name of the attribute to get counts for
        attrValues (list<str>): list of possible values for attribute
        className (str): the name of the class
    Returns:
        list<list<int>>
        This is a list that for each value of the attribute has a
        list of counts of class values.
    """
    counts=[]
    #YOUR CODE HERE
    
    for value in attrValues:
        pertinentExamples = getPertinentExamples(examples, attrName, value)
        counts.append(getClassCounts(pertinentExamples, className))
    return counts
        

def setEntropy(classCounts):
    """
    Calculates the set entropy value for the given list of class counts.
    This is called H in the book. Note that our labels are not binary,
    so the equations in the book need to be modified accordingly. Note
    that H is written in terms of B, and B is written with the assumption 
    of a binary value. B can easily be modified for a non binary class
    by writing it as a summation over a list of ratios, which is what
    you need to implement.
    
    Args:
        classCounts (list<int>): list of counts of each class value
    Returns:
        float
        The set entropy score of this list of class value counts.
    """
    #YOUR CODE HERE
    entropy = 0
    for count in classCounts:
        count = float(count)/sum(classCounts)
        entropy += -(count*log(count, 2))
    return entropy
   

def remainder(examples,attrName,attrValues,className):
    """
    Calculates the remainder value for given attribute and set of examples.
    See the book for the meaning of the remainder in the context of info 
    gain.
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrName (str): the name of the attribute to get remainder for
        attrValues (list<string>): list of possible values for attribute
        className (str): the name of the class
    Returns:
        float
        The remainder score of this value assignment of the attribute.
    """
    #YOUR CODE HERE
    classcounts = getClassCounts(examples,className)
    result = 0
    for value in attrValues:
        pertinentExamples = getPertinentExamples(examples,attrName,value)
        kclasscounts = getClassCounts(pertinentExamples, className)
        result += float(sum(kclasscounts))/sum(classcounts) * setEntropy(kclasscounts)
    return result
    
    #num += len(getPertinentExamples(examples, attrName, value)), float(len(examples)), setEntropy(getClassCounts(getPertinentExamples(examples, attrName, value), className))

        
          
def infoGain(examples,attrName,attrValues,className):
    """
    Calculates the info gain value for given attribute and set of examples.
    See the book for the equation - it's a combination of setEntropy and
    remainder (setEntropy replaces B as it is used in the book).
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrName (str): the name of the attribute to get remainder for
        attrValues (list<string>): list of possible values for attribute
        className (str): the name of the class
    Returns:
        float
        The gain score of this value assignment of the attribute.
    """
    #YOUR CODE HERE
    classcounts = getClassCounts(examples,className)
    #print setEntropy(classcounts), remainder(examples,attrName,attrValues,className)
    return setEntropy(classcounts) - remainder(examples,attrName,attrValues,className)
  
def giniIndex(classCounts):
    """
    Calculates the gini value for the given list of class counts.
    See equation in instructions.
    
    Args:
        classCounts (list<int>): list of counts of each class value
    Returns:
        float
        The gini score of this list of class value counts.
    """
    #YOUR CODE HERE
    result = 1
    for count in classCounts:
        result -= (float(count)/sum(classCounts)) ** 2
    return result
  
def giniGain(examples,attrName,attrValues,className):
    """
    Return the inverse of the giniD function described in the instructions.
    The inverse is returned so as to have the highest value correspond 
    to the highest information gain as in entropyGain. If the sum is 0,
    return sys.maxint.
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrName (str): the name of the attribute to get counts for
        attrValues (list<string>): list of possible values for attribute
        className (str): the name of the class
    Returns:
        float
        The summed gini index score of this list of class value counts.
    """
    #YOUR CODE HERE
    gain = 0
    for value in attrValues:
        pertinentExamples = getPertinentExamples(examples,attrName,value)
        classcounts = getClassCounts(pertinentExamples, className)
        gain += float(len(pertinentExamples))/len(examples) * giniIndex(classcounts)
    if gain == 0:
        import sys
        return sys.maxint
    return 1.0/gain
        
        
    
def makeTree(examples, attrValues,className,setScoreFunc,gainFunc):
    """
    Creates the classification tree for the given examples.
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrValues (dictionary<string,list<string>>): list of possible values for attribute
        className (str): the name of the class
        classScoreFunc (func): the function to score classes (ie setEntropy or giniIndex)
        gainFunc (func): the function to score gain of attributes (ie infoGain or giniGain)
    Returns:
        Tree
        The classification tree for this set of examples
    """
    remainingAttributes=attrValues.keys()
    return Tree(makeSubtrees(remainingAttributes,examples,attrValues,className,setScoreFunc,gainFunc))
    
def makeSubtrees(remainingAttributes,examples,attributeValues,className,setScoreFunc,gainFunc):
    """
    Creates a classification tree Node and all its children.
    
    Args:
        remainingAttributes (list<string>): the names of attributes still not used
        examples (list<dictionary<str,str>>): list of examples
        attrValues (dictionary<string,list<string>>): list of possible values for attribute
        className (str): the name of the class
        setScoreFunc (func): the function to score classes (ie classEntropy or gini)
        gainFunc (func): the function to score gain of attributes (ie entropyGain or giniGain)
    Returns:
        Node
        The classification tree node optimal for the remaining set of attributes.
    """
    #YOUR CODE HERE
    
    
    #print "woop woop"
    if len(remainingAttributes) == 0:
        root = Node()
        classvalues = []
        classcounts = []
        for example in examples:
            if example[className] in classvalues:
                classcounts[classvalues.index(example[className])] += 1
            else:
                classvalues.append(example[className])
                classcounts.append(1)
        modeindex = classcounts.index(max(classcounts))
        root.value = classvalues[modeindex]
        #print "class values", classvalues, "class counts", classcounts, "root.value", root.value
        return root
        
    allSame = True
    firstValue = examples[0][className]
    for example in examples[1:]:
        if example[className] != firstValue:
            allSame = False
    if allSame:
        root = Node()
        root.value = firstValue
        #print "all same hit, value:", firstValue
        return root
        
    best = remainingAttributes[0]
    for attribute in remainingAttributes:
        if gainFunc(examples, attribute, attributeValues[attribute], className) > gainFunc(examples, best, attributeValues[best], className):
            best = attribute
            
    #print remainingAttributes, "removing", best
    #remainingAttributes.remove(best)
    #print remainingAttributes
    newRemainingAttributes = list(remainingAttributes)
    newRemainingAttributes.remove(best)
    
    root = Node()
    root.attr = best
    for value in attributeValues[best]:
        pertinentExamples = getPertinentExamples(examples, best, value)
        if len(pertinentExamples) == 0:
            child = Node()
            root.children[value] = child
            #print "no pertinent examples case hit"
        else:
            root.children[value] = makeSubtrees(newRemainingAttributes, pertinentExamples, attributeValues, className, setScoreFunc, gainFunc)
    return root


