import pickle
from LearningFunctions import learn
from tools import createNewPickleFile
from tools import openPickleFile
from tools import savePickleFile
import time


def sendNewData(inputData, sendData):
    print()
    if sendData == False:
        answer = "0"
        while answer != "1" and answer != "2":
            print("Teach Data?")
            print("1. Yes")
            print("2. No")
            answer = input()
        if answer == "1":
            sendData = True
        else:
            sendData = False

    if sendData == True:
        print()
        print("sending new data....")
        print()

        sendData = True

        learn(inputData)
        diseases_in = open("diseases.pickle", "rb")
        diseases = pickle.load(diseases_in)
    else:
        dataDumps_in = open("dataDumps.pickle", "rb")
        dataDumps = pickle.load(dataDumps_in)

        dataDumps = {"Lung Cancer": {"coughing": 0}}

        dataDumps_out = open("dataDumps.pickle", "wb")
        pickle.dump(dataDumps, dataDumps_out)
        dataDumps_out.close()

        originalDiseaseList_in = open("originalDiseaseList.pickle", "rb")
        originalDiseaseList = pickle.load(originalDiseaseList_in)

        originalDiseaseList = {"Lung Cancer": {"coughing": 0}}

        originalDiseaseList_out = open("originalDiseaseList.pickle", "wb")
        pickle.dump(originalDiseaseList, originalDiseaseList_out)
        originalDiseaseList_out.close()


        return "NO LOG"

def learnExtraData(diseases, disease, originalDiseaseList, dataDumps, symptom, sendData):
    print()
    if sendData == False:
        answer = "0"
        while answer != "1" and answer != "2":
            print("Teach Data?")
            print("1. Yes")
            print("2. No")
            answer = input()
        if answer == "1":
            sendData = True
        else:
            sendData = False

    if sendData == True:
        print()
        print("sending extra data....")
        print()

        sendData = True


        diseases[disease][symptom] = int((originalDiseaseList[disease][symptom] / dataDumps[disease][symptom]) * 1000)


        cases_in = open("cases.pickle", "rb")
        cases = pickle.load(cases_in)
        for disease in diseases:
            cases[disease] = 0
            for symptom in diseases[disease]:
                cases[disease] += diseases[disease][symptom]

        diseases_out = open("diseases.pickle", "wb")
        pickle.dump(diseases, diseases_out)
        diseases_out.close()

        cases_out = open("cases.pickle", "wb")
        pickle.dump(cases, cases_out)
        cases_out.close()



    else:
        dataDumps_in = open("dataDumps.pickle", "rb")
        dataDumps = pickle.load(dataDumps_in)

        dataDumps = {"Lung Cancer":{"coughing":0}}

        dataDumps_out = open("dataDumps.pickle", "wb")
        pickle.dump(dataDumps, dataDumps_out)
        dataDumps_out.close()


        originalDiseaseList_in = open("originalDiseaseList.pickle", "rb")
        originalDiseaseList = pickle.load(originalDiseaseList_in)

        originalDiseaseList = {"Lung Cancer":{"coughing":0}}

        originalDiseaseList_out = open("originalDiseaseList.pickle", "wb")
        pickle.dump(originalDiseaseList, originalDiseaseList_out)
        originalDiseaseList_out.close()

        return "NO LOG"

def findDisease(input):
    disease = ""
    lastIndex = input.index("[")
    disease = input[0:lastIndex]
    return disease

def totalCases(input):
    numOfCases = ""
    index1 = input.index("[")
    index2 = input.index("]")
    numOfCases = input[index1+1:index2]
    numOfCases = int(numOfCases)
    return numOfCases

def separateSymptoms(input):
    symptoms = []
    commaCount = 0
    hasCommas = False
    index1 = input.index(":")

    for char in input:
        if char == ",":
            hasCommas = True

    if hasCommas == True:
        index2 = input.index(",")
    else:
        index2 = input.index(".")


    for char in input:
        if char == "," or char == ".":
            commaCount += 1


    for num in range(0, commaCount):
        firstNew = True
        symptoms.append(input[index1+2:index2])
        for char in input[index2+1:len(input)]:
            if char == "," and firstNew == True or char == "." and firstNew == True :
                index1 = index2
                index2 = input[index2+1:len(input)].index(char) + len(input[0:index2+1])
                firstNew = False

    return symptoms



def formatSymptoms(roughSymptoms):
    symptoms = {}
    for symptom in roughSymptoms:
        index1 = symptom.index("(")
        index2 = symptom.index(")")
        name = symptom[0:index1]
        cases = symptom[index1+1:index2]
        symptoms[name] = cases

    return symptoms



def getKeys(dictionary):
    keys = {}
    num = 1
    for key in dictionary:
        keys[num] = key
        num += 1

    return keys



def sentenceFormatting():
    print()
    print("Format: ")
    print("Disease[total#ofcases]: symptom1(#ofcaseswithsymptom), symptom2(#ofcaseswithsymptom).")
    print()
    dataInput = input("Input: ")

    disease = findDisease(dataInput)
    numOfCases = totalCases(dataInput)
    roughSymptoms = separateSymptoms(dataInput)
    symptoms = formatSymptoms(roughSymptoms)

    return disease, numOfCases, symptoms


def seperateDiseases(dataInput):
    sentences = []
    startIndex = 0
    endIndex = -1
    for character in dataInput:
        endIndex += 1
        if character == '.':
            sentences.append(dataInput[startIndex:endIndex+1])
            startIndex = endIndex + 2

    return sentences



def formattedPrint():
    symptomTotals = openPickleFile('trainingSymptomTotals')
    diseaseTotals = openPickleFile('trainingDiseaseTotals')
    frequencyScores = openPickleFile('frequencyScores')
    weightScores = openPickleFile('weightScores')

    DISEASES = []
    for disease in diseaseTotals:
        formattedString = ''
        formattedString += disease + '[' + str(diseaseTotals[disease]) + ']: '
        count = 0
        for symptom in symptomTotals[disease]:
            count += 1
            formattedString += symptom + '[' + str(symptomTotals[disease][symptom]) + ']'
            formattedString += '(' + str(weightScores[disease][symptom]) + ')'
            formattedString += '(' + str(frequencyScores[disease][symptom]) + ')'
            if count == len(symptomTotals[disease]):
                formattedString += '. '
            else:
                formattedString += ', '

        DISEASES.append(formattedString)

    print('Diseases Data:')
    COUNT = 0
    for disease in DISEASES:
        COUNT += 1
        print(f'{COUNT}. {disease}')
        print()
    print()
    print()
    print()

    # print('Diseases Data:')
    # for disease in DISEASES:
    #     print(disease)
    # print()



def updateFrequencyScores(disease):
    symptomTotals = openPickleFile('trainingSymptomTotals')[disease]
    diseaseTotals = openPickleFile('trainingDiseaseTotals')[disease]
    frequencyScores = openPickleFile('frequencyScores')

    try:
        SCORES = frequencyScores[disease]
    except:
        SCORES = {}
    for symptom in symptomTotals:
        SCORES[symptom] = round(((symptomTotals[symptom] / diseaseTotals) * 100), 2)

    frequencyScores[disease] = SCORES
    savePickleFile('frequencyScores', frequencyScores)


def updateWeightScores(disease):
    symptomTotals = openPickleFile('trainingSymptomTotals')[disease]
    diseaseTotals = openPickleFile('trainingDiseaseTotals')[disease]
    weightScores = openPickleFile('weightScores')
    symptomTotalCount = 0

    for symptom in symptomTotals:
        symptomTotalCount += symptomTotals[symptom]

    try:
        SCORES = weightScores[disease]
    except:
        SCORES = {}
    for symptom in symptomTotals:
        SCORES[symptom] = round(((symptomTotals[symptom] / symptomTotalCount) * 100), 2)

    weightScores[disease] = SCORES
    savePickleFile('weightScores', weightScores)

    
def updateTotals(disease, symptoms, symptomNames, numOfCases):
    trainingSymptomTotals = openPickleFile('trainingSymptomTotals')
    try:
        SYMPTOMS = trainingSymptomTotals[disease]
    except:
        SYMPTOMS = {}
    for symptom in symptomNames:
        Symptom = symptomNames[symptom]
        try:
            SYMPTOMS[Symptom] += int(symptoms[Symptom])
            trainingSymptomTotals[disease] = SYMPTOMS
            savePickleFile('trainingSymptomTotals', trainingSymptomTotals)
        except:
            SYMPTOMS[Symptom] = int(symptoms[Symptom])
            trainingSymptomTotals[disease] = SYMPTOMS
            savePickleFile('trainingSymptomTotals', trainingSymptomTotals)

    trainingDiseaseTotals = openPickleFile('trainingDiseaseTotals')
    try:
        trainingDiseaseTotals[disease] += numOfCases
    except:
        trainingDiseaseTotals[disease] = numOfCases

    savePickleFile('trainingDiseaseTotals', trainingDiseaseTotals)


def fullDataFormatting():
    print()
    print("Format: ")
    print("Disease1[total#ofcases]: symptom1(#ofcaseswithsymptom), symptom2(#ofcaseswithsymptom). Disease2[total#ofcases]: symptom1(#ofcaseswithsymptom), symptom2(#ofcaseswithsymptom).")
    print()

    dataInput = input("Input: ")

    answer = "0"
    while answer != "1" and answer != "2":
        print("Would you like to train the program?")
        print("1. Yes")
        print("2. No")
        answer = input()
    if answer == "1":

        sentences = seperateDiseases(dataInput)
        data = {}
        for sentence in sentences:
            disease = findDisease(sentence)
            numOfCases = totalCases(sentence)
            roughSymptoms = separateSymptoms(sentence)
            symptoms = formatSymptoms(roughSymptoms)
            symptomNames = getKeys(symptoms)
            updateTotals(disease, symptoms, symptomNames, numOfCases)
            updateFrequencyScores(disease)
            updateWeightScores(disease)
            formattedPrint()
            time.sleep(0.1)
    else:
        print()









def formatData():
    ans = "4"
    fullData = False
    APPROVED = False
    while ans != "1" and ans != "2" and ans != "3" and APPROVED == False:
        print("1. Manual Input")
        print("2. Rapid Input")
        print("3. Full Data Input")
        ans = input()
        if ans == "2":
            print()
            print("Rapid Input")
            print()
            diseaseR, numOfCasesR, symptomsR = sentenceFormatting()
            symptomNamesR = getKeys(symptomsR)
            rapid = True
            fullData = False
            APPROVED = True
        elif ans == "1":
            print()
            print("Manual Input")
            print()
            rapid = False
            fullData = False
            APPROVED = True
        elif ans == '3':
            print()
            print("Full Data Input")
            print()
            rapid = False
            fullData = True
            diseases = openPickleFile('diseases')
            if diseases == {"Lung Cancer":{"coughing":0}}:
                fullDataFormatting()
                APPROVED = True
            else:
                APPROVED = False
            break

    data = []
    individualData = {}

    print()
    approved = False
    while approved == False:
        if rapid:
            disease = diseaseR
        else:
            disease = input("Disease: ")
        try:
            disease = int(disease)
            print()
            print("ERROR: Input must be a string.")
            print()
        except:
            if len(disease) > 0:
                approved = True
            else:
                print()
                print("ERROR: Input must be greater than 0 characters long.")
                print()


    totalCases = "one"
    while type(totalCases) == str or totalCases < 1:
        if rapid:
            totalCases = numOfCasesR
        else:
            totalCases = input("Number of Cases: ")
        try:
            totalCases = int(totalCases)
            if totalCases < 1:
                print()
                print("ERROR: Input must be greater than 0.")
                print()
        except:
            print()
            print("ERROR: Input must be an integer greater than 0.")
            print()

    totalSymptoms = "one"
    while type(totalSymptoms) == str or totalSymptoms < 1:
        if rapid:
            totalSymptoms = len(symptomsR)
        else:
            totalSymptoms = input("Number of Symptoms: ")
        try:
            totalSymptoms = int(totalSymptoms)
            if totalSymptoms < 1:
                print()
                print("ERROR: Input must be greater than 0.")
                print()
        except:
            print()
            print("ERROR: Input must be an integer greater than 0.")
            print()

    symptoms = {}
    dumps = {}
    originalDiseaseList = {}
    dataDumps = {}


    dataDumps_in = open("dataDumps.pickle", "rb")
    dataDumps = pickle.load(dataDumps_in)

    originalDiseaseList_in = open("originalDiseaseList.pickle", "rb")
    originalDiseaseList = pickle.load(originalDiseaseList_in)


    for numm in range(0, 1000):
        data.append(disease + ": ")

    for num in range(1, totalSymptoms + 1):

        approved = False
        while approved == False:
            if rapid:
                symptom = symptomNamesR[num]
            else:
                symptom = input("Symptom " + str(num) + ": ")
            try:
                symptom = int(symptom)
                print()
                print("ERROR: Input must be a string.")
                print()
            except:
                if len(symptom) > 0:
                    approved = True
                else:
                    print()
                    print("ERROR: Input must be greater than 0 characters long.")
                    print()

        symptomCases = "one"
        while type(symptomCases) == str or symptomCases < 1:
            if rapid:
                symptomCases = symptomsR[symptom]
            else:
                symptomCases = input("Number of Cases with " + symptom + ": ")
            try:
                symptomCases = int(symptomCases)
                if symptomCases < 1:
                    print()
                    print("ERROR: Input must be greater than 0.")
                    print()
                if symptomCases > totalCases:
                    symptomCases = 0
                    print()
                    print("ERROR: Cases with this symptom must be less than the total number of cases.")
                    print()
            except:
                print()
                print("ERROR: Input must be an integer greater than 0.")
                print()

        SymptomCases = int((symptomCases/totalCases) * 1000)
        print(symptom + ":" + str(SymptomCases))

        symptoms[symptom] = symptomCases
        dumps[symptom] = totalCases

        for number in range(0, SymptomCases):
            if num == totalSymptoms:
                data[number] += symptom + ". "
            else:
                data[number] += symptom + ", "

        goToexcept = {}
        GOTOEXCEPT = {}

        try:
            if originalDiseaseList[disease][symptom] > 0:
                originalDiseaseList[disease][symptom] = originalDiseaseList[disease][symptom]
                originalDiseaseList[disease][symptom] += symptomCases
                dataDumps[disease][symptom] = dataDumps[disease][symptom]
                dataDumps[disease][symptom] += totalCases
            else:
                print(goToexcept[GOTOEXCEPT][44])

        except:
            symptomData = {}
            for number in range(1, SymptomCases + 1):
                symptomData[number] = disease + ": "
                symptomData[number] += symptom + ". "
            individualData[symptom] = symptomData


    allFailed = True
    goToexcept = {}
    GOTOEXCEPT = {}

    for symptom in symptoms:
        try:
            if originalDiseaseList[disease][symptom] > 0:
                allFailed = False
            else:
                print(goToexcept[GOTOEXCEPT][44])
        except:
            print()
    if allFailed == True:
        originalDiseaseList[disease] = symptoms
        dataDumps[disease] = dumps
    else:
        for symptom in symptoms:
            try:
                if originalDiseaseList[disease][symptom] > 0:
                    print()
                else:
                    print()
            except:
                originalDiseaseList[disease][symptom] = symptoms[symptom]
                dataDumps[disease][symptom] = dumps[symptom]


    newData = []
    for numberr in range(0, 1000):
        if len(data[numberr]) > 7: #This prevents the data that doesn't have symptoms from being counted(good and bad) total symptoms = total cases of most common symptom
            if data[numberr][len(data[numberr]) - 2] == ",":
                data[numberr] = data[numberr][0: len(data[numberr]) - 2] + ". "
            newData.append(data[numberr])


    formattedData = ""
    for case in newData:
        formattedData += case


    individualFormatedData = {}
    for symptom in individualData:
        individualFormatedData[symptom] = ""
        for number in individualData[symptom]:
            individualFormatedData[symptom] += individualData[symptom][number]
        individualFormatedData[symptom] = individualFormatedData[symptom][0:len(individualFormatedData[symptom])-2]


    # print(originalDiseaseList[disease])
    # print(dataDumps[disease])

    goToexcept = {}
    GOTOEXCEPT = {}

    diseases_in = open("diseases.pickle", "rb")
    diseases = pickle.load(diseases_in)

    rapidInput = "Copy: "+ disease + "[" + str(totalCases) + "]: "
    for symptom in symptoms:
        rapidInput += symptom + "(" + str(symptoms[symptom]) + "), "
    rapidInput = rapidInput[0:len(rapidInput)-2]
    rapidInput += "."
    print(rapidInput)





    alreadyLearnedNew = False
    numOfSymptoms = len(symptoms)
    symptomNumber = 0
    sendData = False
    for symptom in symptoms:

        diseases_in = open("diseases.pickle", "rb")
        diseases = pickle.load(diseases_in)

        if symptomNumber >= 1:
            sendData = True
        symptomNumber += 1
        try:
            if diseases[disease][symptom] > 0:
                learnExtraData(diseases, disease, originalDiseaseList, dataDumps, symptom, sendData)

                diseases_out = open('disease.picke','wb')
                pickle.dump(diseases, diseases_out)
                diseases_out.close()
            else:
                print(goToexcept[GOTOEXCEPT][44])



            if symptomNumber == numOfSymptoms:
                return formattedData

        except:
            dataInput = individualFormatedData[symptom]
            sendNewData(dataInput, sendData)
            diseases_in = open("diseases.pickle", "rb")
            diseases = pickle.load(diseases_in)

            originalDiseaseList_out = open("originalDiseaseList.pickle", "wb")
            pickle.dump(originalDiseaseList, originalDiseaseList_out)
            originalDiseaseList_out.close()

            dataDumps_out = open("dataDumps.pickle", "wb")
            pickle.dump(dataDumps, dataDumps_out)
            dataDumps_out.close()

            diseases_out = open("diseases.pickle", "wb")
            pickle.dump(diseases, diseases_out)
            diseases_out.close()

            if symptomNumber == numOfSymptoms:
                return "NO LOG"


# trainingSymptomTotals = {"Lung Cancer": {"coughing": 0}}
# savePickleFile('trainingSymptomTotals', trainingSymptomTotals)
# trainingDiseaseTotals = {}
# savePickleFile('trainingDiseaseTotals', trainingDiseaseTotals)
# frequencyScores = {"Lung Cancer": {"coughing": 0}}
# savePickleFile('frequencyScores', frequencyScores)
# weightScores = {"Lung Cancer": {"coughing": 0}}
# savePickleFile('weightScores', weightScores)
# fullDataFormatting()