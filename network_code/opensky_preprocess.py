
from bs4 import BeautifulSoup
import requests
from numpy.lib.utils import source
import numpy as np
from numpy.lib.function_base import disp, percentile
import os
import pandas as pd
from scipy.spatial.distance import cdist
import test

#############################################################
def getAirports2():
    # get table from the webpage(wiki)
    url = 'https://www.latlong.net/category/states-236-14.html'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    # already get the table's class
    table = soup.find('table')
    dfs = pd.read_html(str(table).replace("2;", "2"))
    return transferToDict2(dfs[0])

def transferToDict2(data):
    # replace all missing value into nan
    states = {}
    for index, row in data.iterrows():
        states[row[0].split(',')[0]] = [row[1], row[2]]
    return states
# only need the flight that happend inside of US, so get the airports abbr from website 
def getAirports():
    # get table from the webpage(wiki)
    url = 'https://en.wikipedia.org/wiki/List_of_airports_in_the_United_States'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    # already get the table's class
    table = soup.find('table', {'class': 'wikitable'})
    dfs = pd.read_html(str(table).replace("2;", "2"))
    return transferToDict(dfs[0])

#############################################################
# transfer all abbervation to States 
def transferToDict(data):
    # replace all missing value into nan
    data.replace(to_replace=r'^\s*$',value=np.nan,inplace=True)
    airports = {}
    cur = ''
    states = list(getAirports2().keys())
    for _, row in data.iterrows():
        # represnet the state if other values is nan
        if (pd.isna(row['ICAO'])):
            cur = row['City'].lower().capitalize()
        else:
            if cur not in states:
                continue
            airports[row['ICAO']] = cur
    return airports

#############################################################
# get data from the file
def readFile():
    filepath = 'network_code'
    filepath = os.path.join(filepath, 'Data_opensky')
    filepath = os.path.join(filepath, 'opensky_cleanData.csv')
    # origin, destination, date
    data = pd.read_csv(filepath) 
    return data

#############################################################
# used to preprocess the data, transfer the data from airports to index, and sotre the corresponding date
# will take a pretty long time 
def network_Matrix(): 
    # the loaction of corresponding file 
    path = 'network_code'
    path = os.path.join(path, "Data_opensky")
    weight_path = os.path.join(path, "network_matrix.npy")
    states_path = os.path.join(path, "states.npy")
    if os.path.exists(weight_path) and os.path.exists(states_path):
        return np.load(weight_path), np.load(states_path)
    else:
        airports = getAirports()
        states = list(set(airports.values()))

        data = readFile()
        data_drop = data.drop(data[(data['origin'].isin(airports.keys())) & (data['destination'].isin(airports.keys()))].index)
        data = pd.merge(left=data, right=data_drop, how='left', indicator=True)
        data_new = data.loc[data._merge == 'left_only', :].drop(columns='_merge')

        # get all states, construct a matrix to represent the network first
        network_matrix = np.zeros([len(states),len(states)])
        index = 0
        for row in data_new.itertuples(index=True, name='Pandas'):
            source = states.index(airports.get(row[1]))
            target = states.index(airports.get(row[2]))
            network_matrix[source][target] = network_matrix[source][target] + 1
            # since this will take a pretty long time, add a print line to notice the percentage
            if index >= 7821721:
                print('?')
            print(str(index) + "/" + str(len(data_new)))
            index = index + 1
        # for index, row in data_new.iterrows():
        #     source = states.index(airports.get(row[0]))
        #     target = states.index(airports.get(row[1]))
        #     network_matrix[source][target] = network_matrix[source][target] + 1
        #     # since this will take a pretty long time, add a print line to notice the percentage
        #     if index >= 7821721:
        #         print('?')
        #     print(str(index) + "/" + str(len(data_new)))

        np.save(weight_path, network_matrix)
        np.save(states_path, states)
        
        return network_matrix, states

# transfer the matrix into graph required format
def network():
    matrix, states = network_Matrix()
    source = []
    target = []
    weight = []
    source_index = []
    target_index = []
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if not matrix[i][j] == 0:
                source.append(states[i])
                source_index.append(i)
                target.append(states[j])
                target_index.append(j)
                weight.append(matrix[i][j])
    return source, target, weight, source_index, target_index

