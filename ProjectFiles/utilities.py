# Import external packages

from multiprocessing.connection import wait
import pandas as pd
from datetime import datetime
import numpy as np
import re
import os

# Universal Methods

def get_Path(extension):

    '''
    Finds and returns file paths based on the input file extension
	    Arguments:
		    extension: file extension of the desired files (e.g. '.csv', '.txt')
	    Returns:
		    path_container: array of file paths 
    '''

    path_container = []
    folder_current = os.path.dirname(__file__) 
    folder_input_data = os.path.join(folder_current, "input_data")
    for file in os.listdir(folder_input_data):
        
        if file.endswith("." + extension):
            file_name = os.path.join(folder_input_data, file)
            path_container.append(file_name)
            
    return path_container

# Classes 

class Subject(): #erstellt Klasse "Subject"
    def __init__(self, file_name): # über Konstruktor "__init__" wird die Klasse instantiiert 
        # Klasse hat das Attribut: "file_name" (gilt als Variable für einen Dateipfad)
 
        ### Aufgabe 1: Interpolation ###

        __f = open(file_name) # open öffnet die Datei "file_name"
        self.subject_data = pd.read_csv(__f) #pd.read liest die Daten der Datei 
        self.subject_data = self.subject_data.interpolate(method='quadratic', axis=0) #interpolate (hier knackpunkt) erstellt Datenpunkte zwischen den Daten aus "__f"
        #interpolate(method='linear', axis=0) stellt eine lineare verbindung her 
        #__splited_id = re.findall(r'\d+',file_name)      
        self.subject_id = file_name.split(".csv")[0][-1]
        self.names = self.subject_data.columns.values.tolist()
        self.time = self.subject_data["Time (s)"]
        self.spO2 = self.subject_data["SpO2 (%)"]
        self.temp = self.subject_data["Temp (C)"]
        self.blood_flow = self.subject_data["Blood Flow (ml/s)"]
        print('Subject ' + self.subject_id + ' initialized')
        
### Aufgabe 2: Datenverarbeitung ###

def calculate_CMA(df,n):
    pass
    

def calculate_SMA(df,n):
    pass
