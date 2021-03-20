#!/usr/bin/env python
#
#Author Zacharia Thottakara
#
#Program: Item Metric Evaluator
#
#Command Line Arguments:
#ARG1: Filename (optional)(default="./basket.csv")
#ARG2: AgeLimit (optional)(defautl=3)

import sys
import os

#FUNC
def trim(string):
	return string.replace("\r","").replace("\n","")
def checkFileName(filename):
	import os
	if os.path.exists(filename):
		fc = open(filename,"r")
		header = trim(fc.readline())
		fc.close()
		if header != "fruit,days,characteristic1,characteristic2":
			print("The header for the file wasn't found or was found to be incorrect.")
			print("Execution will continue on the basis of a csv file with a header and data of the type:")
			print("\tItem, Lifespan, Characteristic 1, Characteristic 2,...Characteristic X")
	else:
		print("File %s was not found" % filename)
		exit()

def loadData(filename):
	itemData={}
	totalItems=0
	itemCount=[]
	fd = open(filename,"r")
	rawData = fd.readlines()
	fd.close()
	data = [trim(rawDatum) for rawDatum in rawData]
	header = data[0]
	rest = data[1:]
	for datum in rest:
		totalItems = totalItems + 1
		row = datum.split(",")
		if row[0] in itemData.keys():
			itemData[row[0]].append({"age":row[1],"attrs":row[2:]})
		else:
			itemData[row[0]]=[{"age":row[1],"attrs":row[2:]}]
	return totalItems,itemData

def listDecrementData(counts):#reverse bubble sort
	for i in range(len(counts)):
		for j in range(len(counts)-1):
			if counts[j][1] < counts[j+1][1]:
				counts[j],counts[j+1]=counts[j+1],counts[j]
	return counts

def listItemTypes(items):
	itemCounts = [[item,len(items[item])] for item in items.keys()]
	itemCounts = listDecrementData(itemCounts)
	for itemCount in itemCounts:
		print("%s: %d"%(itemCount[0],itemCount[1]))

def listItemAttrTypes(items):
	itemAttrCount = {}
	for item in items.keys():
		for unit in items[item]:
			fullName= item + ": "+ ', '.join(sorted(unit["attrs"]))
			if fullName in itemAttrCount.keys():
				itemAttrCount[fullName] = itemAttrCount[fullName] + 1
			else:
				itemAttrCount[fullName] = 1
	itemAttrCountArry = [[specificItem,itemAttrCount[specificItem]] for specificItem in itemAttrCount.keys()]
	itemAttrCountArry = listDecrementData(itemAttrCountArry)
	for itemAttrCountArr in itemAttrCountArry:
		print("%d %s" % (itemAttrCountArr[1],itemAttrCountArr[0]))
def listOldItems(items,ageLimit):
	oldItemArry=[]
	for item in items.keys():
		oldCount=0
		for unit in items[item]:
			if int(unit["age"]) > ageLimit:
				oldCount = oldCount + 1
		if oldCount > 0:
			oldItemArry.append("%d %s" % (oldCount,item))
	print("%s and %s are over %d days old" % (', '.join(oldItemArry[:-1]),oldItemArry[-1:][0],ageLimit))
#FUNC

#MAIN
filename="./basket.csv"
ageLimit = 3
if len(sys.argv) > 3:
	print("Too many args")
elif len(sys.argv) == 3:
	filename=sys.argv[1]
	try:
		ageLimit = int(sys.argv[2])
	except:
		print("Script was called with an invalid second argument. Second argument must be the integer age limit of the items.")
		exit()
	checkFileName(filename)
elif len(sys.argv) == 2:
	filename = sys.argv[1]
	checkFileName(filename)
else:
	checkFileName(filename)

total,items = loadData(filename)
print("Total number of fruit: %d\n" % total)
print("Types of fruit: %d\n" % len(items.keys()))
print("The number of each type of fruit in descending order: ")
listItemTypes(items)
print("\nThe characteristics (size, color, shape, etc.) of each fruit by type: ")
listItemAttrTypes(items)
print("\nHave any fruit been in the basket for over %d days" % ageLimit)
listOldItems(items,ageLimit)
#MAIN
