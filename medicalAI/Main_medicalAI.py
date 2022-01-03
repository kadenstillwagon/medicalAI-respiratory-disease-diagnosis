import pickle
from LearningFunctions import learn, printDiseases, sortDiseases, addLog, percents, overallPercents
from TestingFunctions import test
from FormattingFunctions import formatData
from datetime import datetime
import getpass
import time
from tools import createNewPickleFile
from tools import openPickleFile
from tools import savePickleFile

patients = {}
diseases = {}
history = []
mainMenu = True




def adminLogin(): #MUST UNDO MUST UNDO MUST UNDO
    accessGranted = False
    username = input("Username: ")
    password = input("Password: ")

    user_in = open("user.pickle", "rb")
    user = pickle.load(user_in)

    try:
        if user[username] == password:
            accessGranted = True
    except:
        accessGranted = False

    return accessGranted


def newLog():
    history_in = open("history.pickle", "rb")
    history = pickle.load(history_in)

    now = datetime.now()
    dateNtime = now.strftime("%d/%m/%Y %H:%M:%S")

    log = dateNtime + " DISEASES RESET "

    history.append(log)

    history_out = open("history.pickle", "wb")
    pickle.dump(history, history_out)
    history_out.close()

def resetDiseases():
    newLog()
    print("Data Reset")
    print()

    diseases_in = open("diseases.pickle", "rb")
    diseases = pickle.load(diseases_in)

    diseases = {"Lung Cancer":{"coughing":0}}

    diseases_out = open("diseases.pickle", "wb")
    pickle.dump(diseases, diseases_out)
    diseases_out.close()



    cases_in = open("cases.pickle", "rb")
    cases = pickle.load(cases_in)

    cases = {"Lung Cancer": 0}

    cases_out = open("cases.pickle", "wb")
    pickle.dump(cases, cases_out)
    cases_out.close()



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


    #For Full Data Training
    trainingSymptomTotals = {"Lung Cancer": {"coughing": 0}}
    savePickleFile('trainingSymptomTotals', trainingSymptomTotals)

    trainingDiseaseTotals = {}
    savePickleFile('trainingDiseaseTotals', trainingDiseaseTotals)

    frequencyScores = {"Lung Cancer": {"coughing": 0}}
    savePickleFile('frequencyScores', frequencyScores)

    weightScores = {"Lung Cancer": {"coughing": 0}}
    savePickleFile('weightScores', weightScores)




def clearHistory():
    print("History Cleared")
    print()

    history_in = open("history.pickle", "rb")
    history = pickle.load(history_in)

    history = []

    history_out = open("history.pickle", "wb")
    pickle.dump(history, history_out)
    history_out.close()


def printHistory():
    history_in = open("history.pickle", "rb")
    history = pickle.load(history_in)
    num = 0
    print()
    print("History Log:")
    for log in history:
        if "Input Data" in history[num]:
            index1 = history[num].index("Input Data")
            index2 = history[num].index("Current Disease List")
            print(str(num + 1) + ". " + history[num][0:index1])
            print()
            print(history[num][index1:index2])
            print()
            print(history[num][index2:len(history[num])])
            print()
        elif "Test Cases" in history[num]:
            index1 = history[num].index("Test Cases")
            index2 = history[num].index("Results")
            print(str(num + 1) + ". " + history[num][0:index1])
            print()
            print(history[num][index1:index2])
            print()
            print(history[num][index2:len(history[num])])
            print()
        elif "DISEASES RESET" in history[num]:
            print(str(num + 1) + ". " + history[num])
            print()
        num += 1

def confirmation():
    if adminLogin():
        print()
        print("Are you sure?")
        print("1. Yes")
        print("2. No")
        confirmation = input()
    else:
        print()
        print("Invalid Login")
        print()
        confirmation = 2
    return confirmation

def checkDiseasesExist():
    exists = True
    diseases_in = open("diseases.pickle", "rb")
    diseases = pickle.load(diseases_in)

    if len(diseases) < 2:
        print()
        print("Must have more than one disease in database to test.")
        print()
        exists = False

    return exists



running = True
while running:
    if adminLogin() == True:
        print()
        print("Access Granted")
        print()
        while mainMenu == True:

            diseases_in = open("diseases.pickle", "rb")
            diseases = pickle.load(diseases_in)

            print("Menu:")
            print("1. Learn")
            print("2. Test")
            print("3. View Disease List")
            print("4. View History")
            print("5. Reset Diseases")
            print("6. Clear History")
            learnOtest = input()

            mainMenu = False

            while learnOtest != "1" and learnOtest != "2" and learnOtest != "3" and learnOtest != "4" and learnOtest != "5" and learnOtest != "6":
                print("Menu:")
                print("1. Learn")
                print("2. Test")
                print("3. View Disease List")
                print("4. View History")
                print("5. Reset Diseases")
                print("6. Clear History")
                learnOtest = input()

            if learnOtest == "1":

                inputData = formatData()


                diseases_in = open("diseases.pickle", "rb")
                diseases = pickle.load(diseases_in)

                cases_in = open("cases.pickle", "rb")
                cases = pickle.load(cases_in)

                if inputData == "NO LOG":
                    print()
                else:
                    Percents = percents(diseases, cases)
                    OverallPercents = overallPercents(diseases)
                    diseases = sortDiseases(diseases)
                    diseaseList = printDiseases(diseases, cases, Percents, OverallPercents)
                    addLog(inputData, diseaseList)


            elif learnOtest == "2":
                diseasesExist = checkDiseasesExist()
                if diseasesExist:
                    test()
                else:
                    print()
                    print("You must train before testing.")
                    print()

            elif learnOtest == "3":
                diseases_in = open("diseases.pickle", "rb")
                diseases = pickle.load(diseases_in)

                cases_in = open("cases.pickle", "rb")
                cases = pickle.load(cases_in)

                Percents = percents(diseases, cases)
                OverallPercents = overallPercents(diseases)
                diseases = sortDiseases(diseases)
                diseaseList = printDiseases(diseases, cases, Percents, OverallPercents)

            elif learnOtest == "4":
                printHistory()

            elif learnOtest == "5":
                confirmation = confirmation()
                if confirmation == "1":
                    resetDiseases()

            elif learnOtest == "6":
                confirmation = confirmation()
                if confirmation == "1":
                    clearHistory()

            # time.sleep(2) adds a 2 second delay to reopen menu
            mainMenu = True
    else:
        print()
        print("Access Denied")
        print()








