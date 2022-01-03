import pickle
from datetime import datetime


def addSymptoms(stopKey, caseName, case):
    symptoms = []

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
            symptoms.append(symptom)

        elif comma > 1 and comma < symptomCount:
            newStopKeyComma = case[lastIndex + 2: len(case) - 1].index(",") + lastIndex + 2
            symptom = case[lastIndex + 2: newStopKeyComma]
            lastIndex = newStopKeyComma
            symptoms.append(symptom)

        elif comma == symptomCount:
            finalIndex = case.index(".")
            symptom = case[lastIndex + 2: finalIndex]
            symptoms.append(symptom)

    return symptoms


def caseSeperation(dataInput):
    cases = []
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
            cases.append(case)

        elif period > 1 and period < caseCount:
            newStopKeyPeriod = dataInput[lastIndex + 2: len(dataInput)].index(".") + lastIndex + 2
            case = dataInput[lastIndex + 2: newStopKeyPeriod+1]
            lastIndex = newStopKeyPeriod
            cases.append(case)

    return cases


def assignScores(symptoms, diseases):
    scores = {}
    nonMatches = {}
    for disease in diseases:
        diseaseScore = 0
        nonMatches[disease] = 0
        for symptom in symptoms:
            beforeTest = diseaseScore
            for ssymptom in diseases[disease]:
                if symptom == ssymptom:
                    diseaseScore += diseases[disease][ssymptom]
            if beforeTest == diseaseScore:
                nonMatches[disease] += 1
        scores[disease] = diseaseScore

    return scores, nonMatches

def assignPercents(scores, nonMatches, diseases):
    percents = {}
    for disease in diseases:
        totalScore = 0
        for symptom in diseases[disease]:
            totalScore += diseases[disease][symptom]
        percent = (scores[disease] / totalScore) * 100
        percent = percent - (nonMatches[disease] * 7)
        percents[disease] = percent

    return percents


def highestPercent(percents, caseName):
    predictions = ""
    secondPredictions = []
    highestPercent = 0

    print()
    print(str(caseName) + ": ")
    prediction = "Invalid Test: Symptoms not Found"
    for disease in percents:
        print(disease + ": " + str(round(percents[disease], 1)) + "%")
        if percents[disease] > highestPercent:
            highestPercent = percents[disease]
            prediction = disease
    for disease in percents:
        if disease != prediction:
            if (percents[prediction] - percents[disease]) < 7:
                secondPredictions.append(disease)
    highS = {}
    realSecondPredictions = []
    for entity in range(0, len(secondPredictions)):
        highestSecond = 0
        for disease in secondPredictions:
            if percents[disease] > highestSecond:
                highS = disease
                highestSecond = percents[disease]
        secondPredictions.pop(secondPredictions.index(highS))
        realSecondPredictions.append(highS)


    predictions = prediction
    print()


    return predictions, realSecondPredictions



def newLog(testCases, results):
    now = datetime.now()
    dateNtime = now.strftime("%d/%m/%Y %H:%M:%S")

    log = dateNtime + " TESTING:" + " Test Cases: " + testCases + " Results: " + results
    return log


def printPredictions(predictions, secondPredictions, percents, diseases):
    results = ""
    predictionNumber = 0
    invalid = False
    print()
    print("Predictions:")
    for caseName in predictions:
        invalid = False
        predNper = ""
        predictionNumber += 1

        prediction = predictions[caseName]
        if prediction == "Invalid Test: Symptoms not Found":
            invalid = True
            print()
            print(prediction)
            print()
        else:
            totalScore = 0
            for symptom in diseases[prediction]:
                totalScore += diseases[prediction][symptom]
            percentage = round(percents[caseName][prediction], 1)
            predNper += str(prediction) + "(" + str(percentage) + "%). "

            if len(secondPredictions[caseName]) > 0:
                number = 0
                predNper += "Second Guess(es): "
                for secondPrediction in secondPredictions[caseName]:
                    number += 1
                    totalScore = 0
                    for symptom in diseases[secondPrediction]:
                        totalScore += diseases[secondPrediction][symptom]
                    Percentage = round(percents[caseName][secondPrediction], 1)
                    if number == len(secondPredictions[caseName]):
                        predNper += str(secondPrediction) + "(" + str(Percentage) + "%). "
                    else:
                        predNper += str(secondPrediction) + "(" + str(Percentage) + "%), "



        if invalid == False:
            print(str(predictionNumber) + ". " + caseName + ": " + predNper)
            results += caseName + ": " + predNper
        else:
            results += caseName + ": INVALID."
    print()



    return results



def addLog(results, testCases):
    history_in = open("history.pickle", "rb")
    history = pickle.load(history_in)

    log = newLog(testCases, results)
    history.append(log)

    history_out = open("history.pickle", "wb")
    pickle.dump(history, history_out)
    history_out.close()



def test():
    diseases_in = open("diseases.pickle", "rb")
    diseases = pickle.load(diseases_in)

    startTime = 0
    endTime = 0
    predictions = {}
    secondPredictions = {}
    scores = {}
    percents = {}
    nonMatches = {}

    verified = False

    while verified == False:
        testCases = input("Enter Cases to Test: ")

        if "," in testCases and "." in testCases and ":" in testCases:

            startTimeRough = datetime.today()
            startTime = startTimeRough.second
            startTime += (startTimeRough.microsecond / 1000000)

            verified = True
            cases = caseSeperation(testCases)

            for case in cases:
                diseases_in = open("diseases.pickle", "rb")
                diseases = pickle.load(diseases_in)
                stopKey = case.index(":")
                caseName = case[0:stopKey]
                symptoms = addSymptoms(stopKey, caseName, case)
                scores[caseName], nonMatches[caseName] = assignScores(symptoms, diseases)
                percents[caseName] = assignPercents(scores[caseName], nonMatches[caseName], diseases)
                predictions[caseName], secondPredictions[caseName] = highestPercent(percents[caseName], caseName)

            results = printPredictions(predictions, secondPredictions, percents, diseases)

            endTimeRough = datetime.today()
            endTime = endTimeRough.second
            endTime += (endTimeRough.microsecond / 1000000)
            totalTime = endTime - startTime
            print("Time: " + str(totalTime))
            print()

            results += " Time: " + str(totalTime)

            addLog(results, testCases)

        else:
            verified = False
            print()
            print("Reformat data input to: Case1: symptom1, symptom2, symptom3. Case2: symptom1, symptom2, symptom3.")
            print()

