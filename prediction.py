# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 00:04:55 2024

@author: ataru
"""

import os
import pandas as pd
import pickle

base_dir = os.path.dirname(os.path.abspath(__file__))  # Gets the directory of the current script

# Load your models and dataset using relative paths
diabetes_model = pickle.load(open(os.path.join(base_dir, 'saved models', 'diabetes_model.sav'), 'rb'))
heart_disease_model = pickle.load(open(os.path.join(base_dir, 'saved models', 'heart_disease_model.sav'), 'rb'))
parkinsons_model = pickle.load(open(os.path.join(base_dir, 'saved models', 'parkinsons_model.sav'), 'rb'))
df_severity = pd.read_csv(os.path.join(base_dir, 'dataset', 'Symptom-severity.csv'))
GBC_model = pickle.load(open(os.path.join(base_dir, 'saved models', 'symptoms models', 'GBC.sav'), 'rb'))
hyper_tuned_svc = pickle.load(open(os.path.join(base_dir, 'saved models', 'symptoms models', 'hypertuned.sav'), 'rb'))
model_SVM_init = pickle.load(open(os.path.join(base_dir, 'saved models', 'symptoms models', 'svm.sav'), 'rb'))
