import pickle
from datetime import datetime



def checkNewSymptom(disease, symptom):
    new = True
    diseases_in = open("diseases.pickle", "rb")
    diseases = pickle.load(diseases_in)

    symptoms = []
    for symptomss in diseases[disease]:
        symptoms.append(symptomss)

    for sympt in symptoms:
        if sympt == symptom:
            new = False
    return new

def checkNewDisease(disease):
    new = True
    diseases_in = open("diseases.pickle", "rb")
    diseases = pickle.load(diseases_in)

    for diseasess in diseases:
        if diseasess == disease:
            new = False
    return new



def addSymptoms(stopKey, diseases, disease, case):
    symptoms = {}
    for symptomss in diseases[disease]:
        symptoms[symptomss] = diseases[disease][symptomss]

    symptomCount = 0
    for a in case:
        if a == ",":
            symptomCount += 1
    symptomCount += 1

    lastIndex = stopKey
    for comma in range(1, symptomCount + 1):
        if comma == 1 and symptomCount > 1:
            stopKeyComma = case.index(",")
            lastIndex = stopKeyComma
            symptom = case[stopKey + 2: stopKeyComma]
            if checkNewSymptom(disease, symptom) == True:
                symptoms[symptom] = 1
            else:
                symptoms[symptom] += 1

        elif comma > 1 and comma < symptomCount:
            newStopKeyComma = case[lastIndex + 2: len(case) - 1].index(",") + lastIndex + 2
            symptom = case[lastIndex + 2: newStopKeyComma]
            lastIndex = newStopKeyComma
            if checkNewSymptom(disease, symptom) == True:
                symptoms[symptom] = 1
            else:
                symptoms[symptom] += 1

        elif comma == symptomCount:
            finalIndex = case.index(".")
            symptom = case[lastIndex + 2: finalIndex]
            if checkNewSymptom(disease, symptom) == True:
                symptoms[symptom] = 1
            else:
                symptoms[symptom] += 1
    for symptomss in diseases[disease]:
        symptoms[symptomss] = diseases[disease][symptomss]

    symptomCount = 0
    for a in case:
        if a == ",":
            symptomCount += 1
    symptomCount += 1

    lastIndex = stopKey
    for comma in range(1, symptomCount + 1):
        if comma == 1 and symptomCount > 1:
            stopKeyComma = case.index(",")
            lastIndex = stopKeyComma
            symptom = case[stopKey + 2: stopKeyComma]
            if checkNewSymptom(disease, symptom) == True:
                symptoms[symptom] = 1
            else:
                symptoms[symptom] += 1

        elif comma > 1 and comma < symptomCount:
            newStopKeyComma = case[lastIndex + 2: len(case) - 1].index(",") + lastIndex + 2
            symptom = case[lastIndex + 2: newStopKeyComma]
            lastIndex = newStopKeyComma
            if checkNewSymptom(disease, symptom) == True:
                symptoms[symptom] = 1
            else:
                symptoms[symptom] += 1

        elif comma == symptomCount:
            finalIndex = case.index(".")
            symptom = case[lastIndex + 2: finalIndex]
            if checkNewSymptom(disease, symptom) == True:
                symptoms[symptom] = 1
            else:
                symptoms[symptom] += 1


    return symptoms





def caseSeperation(dataInput):
    casess = []
    caseCount = 0
    for p in dataInput:
        if p == ".":
            caseCount += 1
    caseCount += 1


    lastIndex = 0
    for period in range(1,caseCount):
        if period == 1 and caseCount > 1:
            stopKeyPeriod = dataInput.index(".")
            lastIndex = stopKeyPeriod
            case = dataInput[0: stopKeyPeriod+1]
            casess.append(case)

        elif period > 1 and period < caseCount:
            newStopKeyPeriod = dataInput[lastIndex + 2: len(dataInput)].index(".") + lastIndex + 2
            case = dataInput[lastIndex + 2: newStopKeyPeriod+1]
            lastIndex = newStopKeyPeriod
            casess.append(case)

    return casess

def newLog(dataInput, diseaseList):
    now = datetime.now()
    dateNtime = now.strftime("%m/%d/%Y %H:%M:%S")

    log = dateNtime + " LEARNING:" + " Input Data: " + dataInput + " Current Disease List: " +  diseaseList
    return log


def printDiseases(diseases, cases, percents, overallPercents):
    print()
    print("Diseases:")
    diseaseList = ""
    for disease in diseases:
        symptomList = ""
        symptomNumber = 0
        for symptom in diseases[disease]:
            symptomNumber += 1
            if symptomNumber < len(diseases[disease]):
                symptomList += symptom + "[" + str(diseases[disease][symptom]) + "](" + str(percents[disease][symptom]) + "%)(" + str(overallPercents[disease][symptom]) + "%), "
            else:
                symptomList += symptom + "[" + str(diseases[disease][symptom]) + "](" + str(percents[disease][symptom]) + "%)(" + str(overallPercents[disease][symptom]) + "%)."
        print(disease + "[" + str(cases[disease]) + "]: " + symptomList)
        diseaseList += disease + "[" + str(cases[disease]) + "]: " + symptomList + "\n"
    print()

    return diseaseList


def addLog(dataInput, diseaseList):
    history_in = open("history.pickle", "rb")
    history = pickle.load(history_in)

    log = newLog(dataInput, diseaseList)
    history.append(log)

    history_out = open("history.pickle", "wb")
    pickle.dump(history, history_out)
    history_out.close()


def sortDiseases(diseases):
    sortedDiseases = {}

    for disease in diseases:
        symptoms = {}
        for symptomss in diseases[disease]:
            if diseases[disease][symptomss] > 0:
                maxNum = 0
                toAdd = ""
                for symptom in diseases[disease]:
                    if symptom not in symptoms:
                        if diseases[disease][symptom] > maxNum:
                            maxNum = diseases[disease][symptom]
                            toAdd = symptom
                symptoms[toAdd] = diseases[disease][toAdd]
        sortedDiseases[disease] = symptoms

    return sortedDiseases




def percents(diseases, cases):
    Percents = {}
    percents_in = open("percents.pickle", "rb")
    percentss = pickle.load(percents_in)


    for disease in diseases:
        diseasePercents = {}
        for symptom in diseases[disease]:
            diseasePercents[symptom] = round(((diseases[disease][symptom] / cases[disease]) * 100), 1)
        Percents[disease] = diseasePercents

    percentss = Percents

    percents_out = open("percents.pickle", "wb")
    pickle.dump(percentss, percents_out)
    percents_out.close()

    return Percents


def overallPercents(diseases):
    OverallPercents = {}
    overallPercents_in = open("overallPercents.pickle", "rb")
    overallPercentss = pickle.load(overallPercents_in)


    for disease in diseases:
        diseaseOverallPercents = {}
        for symptom in diseases[disease]:
            diseaseOverallPercents[symptom] = diseases[disease][symptom] / 10
        OverallPercents[disease] = diseaseOverallPercents

    overallPercentss = OverallPercents

    overallPercents_out = open("overallPercents.pickle", "wb")
    pickle.dump(overallPercentss, overallPercents_out)
    overallPercents_out.close()


    return OverallPercents


def learn(dataInput):
    diseases_in = open("diseases.pickle", "rb")
    diseases = pickle.load(diseases_in)

    cases_in = open("cases.pickle", "rb")
    cases = pickle.load(cases_in)

    verified = False

    while verified == False:
        if len(dataInput) < 1:
            dataInput += input("Enter new data to Teach: ")

        if "." in dataInput and ":" in dataInput:
            verified = True

            casess = caseSeperation(dataInput)
            for case in casess:
                diseases_in = open("diseases.pickle", "rb")
                diseases = pickle.load(diseases_in)
                stopKey = case.index(":")
                disease = case[0:stopKey]



                symptoms = {}
                try:
                    for symptomss in diseases[disease]:
                        symptoms[symptomss] = diseases[disease][symptomss]
                    diseases[disease] = symptoms
                except:
                    diseases[disease] = symptoms
                diseases_out = open("diseases.pickle", "wb")
                pickle.dump(diseases, diseases_out)
                diseases_out.close()


            for case in casess:
                diseases_in = open("diseases.pickle", "rb")
                diseases = pickle.load(diseases_in)
                stopKey = case.index(":")
                disease = case[0:stopKey]
                symptoms = addSymptoms(stopKey, diseases, disease, case)
                diseases[disease] = symptoms
                diseases_out = open("diseases.pickle", "wb")
                pickle.dump(diseases, diseases_out)
                diseases_out.close()

            diseases = sortDiseases(diseases)

            cases_in = open("cases.pickle", "rb")
            cases = pickle.load(cases_in)
            for disease in diseases:
                cases[disease] = 0
                for symptom in diseases[disease]:
                    cases[disease] += diseases[disease][symptom]


            Percents = percents(diseases, cases)
            OverallPercents = overallPercents(diseases)
            diseaseList = printDiseases(diseases, cases, Percents, OverallPercents)
            addLog(dataInput, diseaseList)


            diseases_out = open("diseases.pickle", "wb")
            pickle.dump(diseases, diseases_out)
            diseases_out.close()

            cases_out = open("cases.pickle", "wb")
            pickle.dump(cases, cases_out)
            cases_out.close()

        else:
            verified = False
            print()
            print("Reformat data input to: Disease1: symptom1, symptom2, symptom3. Disease2: symptom1, symptom2, symptom3.")
            print()







