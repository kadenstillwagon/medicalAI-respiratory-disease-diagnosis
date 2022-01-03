# import pickle
# import requests
# from bs4 import BeautifulSoup
# from datetime import datetime
# import time
# from twilio.rest import Client
# import threading
# from concurrent.futures import ThreadPoolExecutor
# import atexit
# import os
#
# WORDS = []
# DICTIONARY = {}
#
# def createNewPickleFile(name, type):
#     pickle_in = open(f'{name}.pickle', 'wb')
#
#     variable = type
#
#     pickle_out = open(f'{name}.pickle', 'wb')
#     pickle.dump(variable, pickle_out)
#     pickle_out.close()
#
#
# def openPickleFile(name):
#     pickle_in = open(f'{name}.pickle', 'rb')
#     variable = pickle.load(pickle_in)
#
#     return variable
#
#
# def savePickleFile(name, variable):
#     pickle_out = open(f'{name}.pickle', 'wb')
#     pickle.dump(variable, pickle_out)
#     pickle_out.close()
#
#
# def sendNotification(notification):
#     account_sid = 'ACf21fe25e0f83d65a47daf9f8f1ad4528'
#     auth_token = '0fd10b6cf80c8571d3e5905f60872a1c'
#     client = Client(account_sid, auth_token)
#
#     message = client.messages.create(
#         messaging_service_sid='MG6c403876d90069344c8316564d9bfeaa',
#         body=notification,
#         to='+14804936650'
#     )
#
#     print(notification)
#
#
# def newDictionaryWords(url):
#
#     Exists = True
#     count = 0
#     wordsToAdd = []
#
#     while Exists == True:
#         count += 1
#         if count < 11:
#             url = url[0:-1]
#         else:
#             url = url[0:-2]
#         url += str(count)
#         print(url)
#
#         try:
#             page = requests.get(url).text
#         except:
#             try:
#                 sendNotification("Page Overwhelmed: Resetting in 60")
#                 time.sleep(60)
#                 page = requests.get(url).text
#             except:
#                 sendNotification("Page Very Overwhelmed: Resetting in another 120")
#                 time.sleep(120)
#                 page = requests.get(url).text
#
#         soup = BeautifulSoup(page, 'html.parser')
#
#         exists = soup.find(class_="contentCard")
#         try:
#             if len(exists.text) > 0:
#                 print('Reset')
#             Exists = False
#             break
#
#         except:
#             list = soup.find(class_="css-fq2xu3 e1j8zk4s0")
#             for word in list:
#                 word = word.text
#                 if '|' in word:
#                     index = int(word.index("|"))
#                     word = word[0: index - 1]
#                 # print(word)
#
#                 DICTIONARY = openPickleFile('dictionary')
#                 if word not in DICTIONARY:
#                     wordsToAdd.append(word)
#
#
#     return wordsToAdd
#
#
# def newWordThreads(letters):
#     codes = []
#     for letter in letters:
#         code = f'https://www.dictionary.com/list/{letter}/1'
#         codes.append(code)
#
#     with ThreadPoolExecutor() as executor:
#         results = executor.map(newDictionaryWords, codes)
#
#     count = 0
#     for result in results:
#         added = 0
#         for word in result:
#             newWords = openPickleFile('newWords')
#             if word not in newWords:
#                 newWords.append(word)
#                 savePickleFile('newWords', newWords)
#                 added += 1
#         print(f'{letters[count].upper()}: {added} Words Added')
#         count += 1
#
#
#     newWords = openPickleFile('newWords')
#     print(f'New Words: {len(newWords)}')
#
#     sendNotification('Reset')
#
#
# newWordThreads(['a', 'b'])



