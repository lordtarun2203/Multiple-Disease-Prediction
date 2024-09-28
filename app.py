# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 23:56:04 2024
@author: ataru
"""

import streamlit as st
import pandas as pd
from prediction import diabetes_model, heart_disease_model, parkinsons_model, df_severity, GBC_model, hyper_tuned_svc, model_SVM_init
from streamlit_option_menu import option_menu
from database import add_user, login_user, check_user_exists, update_diagnosis, get_user_diagnoses
import hashlib  # For password hashing


# Load the credentials from the JSON file
# Load the credentials and diagnosis history from the JSON file
# Hash the password using SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Check Password Functionality
def check_password():
    #"""Returns True if the user has entered the correct password."""
    if st.session_state.get("password_correct"):
        return True

    st.write("Already have an account? Log in below or sign up if you're new:")

    # Radio buttons for sign up / sign in
    option = st.radio("Choose an option:", ["Sign In", "Sign Up"])

    # Sign Up Functionality
    def sign_up():
        """Sign up a new user and save their credentials to the SQLite database."""
        username = st.session_state["username"]
        password = st.session_state["password"]

        # Check if the username already exists
        if check_user_exists(username):
            st.error("Username already exists! Please try a different one.")
        else:
            # Hash the password before saving
            hashed_password = hash_password(password)
            add_user(username, hashed_password)
            st.success("Sign Up successful! You can now log in.")

    # Sign In Functionality
    def sign_in():
        """Check if the entered username and password are correct."""
        username = st.session_state["username"]
        password = st.session_state["password"]

        # Hash the entered password for comparison
        hashed_password = hash_password(password)

        # Validate the username and password
        if login_user(username, hashed_password):
            st.session_state["password_correct"] = True
            st.session_state["current_user"] = username
            del st.session_state["password"]  # Don't store the password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # Create a login form
    def login_form():
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")

            if option == "Sign In":
                st.form_submit_button("Log in", on_click=sign_in)
            elif option == "Sign Up":
                st.form_submit_button("Sign Up", on_click=sign_up)

    # Show the login form
    login_form()

    # Show error if the password is incorrect
    if "password_correct" in st.session_state and not st.session_state["password_correct"]:
        st.error("😕 User not known or password incorrect")

    return False




# Update the record_diagnosis function to use SQLite
def record_diagnosis(disease_name):
    """Record the diagnosis in the SQLite database under the logged-in user's history."""
    user = st.session_state["current_user"]
    update_diagnosis(user, disease_name)





def diabetes_prediction():
    # Page title
    st.title('Diabetes Prediction using ML')

    # User inputs
    col1, col2, col3 = st.columns(3)
    with col1:
        Pregnancies = st.text_input('Number of Pregnancies')
    with col2:
        Glucose = st.text_input('Glucose Level')
    with col3:
        BloodPressure = st.text_input('Blood Pressure value')
    with col1:
        SkinThickness = st.text_input('Skin Thickness value')
    with col2:
        Insulin = st.text_input('Insulin Level')
    with col3:
        BMI = st.text_input('BMI value')
    with col1:
        DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function value')
    with col2:
        Age = st.text_input('Age of the Person')

    # Prediction button
    if st.button('Diabetes Test Result'):
        user_input = [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]
        user_input = [float(x) for x in user_input]
        diab_prediction = diabetes_model.predict([user_input])
        if diab_prediction[0] == 1:
            st.success('The person is Diabetic')
            record_diagnosis('Diabetes')
        else:
            st.success('The person is not Diabetic')


def heart_disease_prediction():
    # Page title
    st.title('Heart Disease Prediction using ML')

    # User inputs
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.text_input('Age')
    with col2:
        sex = st.text_input('Sex')
    with col3:
        cp = st.text_input('Chest Pain types')
    with col1:
        trestbps = st.text_input('Resting Blood Pressure')
    with col2:
        chol = st.text_input('Serum Cholesterol in mg/dL')
    with col3:
        fbs = st.text_input('Fasting Blood Sugar > 120 mg/dL')
    with col1:
        restecg = st.text_input('Resting Electrocardiographic results')
    with col2:
        thalach = st.text_input('Maximum Heart Rate achieved')
    with col3:
        exang = st.text_input('Exercise Induced Angina')
    with col1:
        oldpeak = st.text_input('ST depression induced by exercise')
    with col2:
        slope = st.text_input('Slope of the peak exercise ST segment')
    with col3:
        ca = st.text_input('Major vessels colored by flourosopy')
    with col1:
        thal = st.text_input('Thal: 0 = normal; 1 = fixed defect; 2 = reversible defect')

    # Prediction button
    if st.button('Heart Disease Test Result'):
        user_input = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
        user_input = [float(x) for x in user_input]
        heart_prediction = heart_disease_model.predict([user_input])
        if heart_prediction[0] == 1:
            st.success('The person is having heart disease')
            record_diagnosis('Heart Disease')
        else:
            st.success('The person does not have heart disease')


def parkinsons_prediction():
    # Page title
    # page title
    st.title("Parkinson's Disease Prediction using ML")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        fo = st.text_input('MDVP:Fo(Hz)')

    with col2:
        fhi = st.text_input('MDVP:Fhi(Hz)')

    with col3:
        flo = st.text_input('MDVP:Flo(Hz)')

    with col4:
        Jitter_percent = st.text_input('MDVP:Jitter(%)')

    with col5:
        Jitter_Abs = st.text_input('MDVP:Jitter(Abs)')

    with col1:
        RAP = st.text_input('MDVP:RAP')

    with col2:
        PPQ = st.text_input('MDVP:PPQ')

    with col3:
        DDP = st.text_input('Jitter:DDP')

    with col4:
        Shimmer = st.text_input('MDVP:Shimmer')

    with col5:
        Shimmer_dB = st.text_input('MDVP:Shimmer(dB)')

    with col1:
        APQ3 = st.text_input('Shimmer:APQ3')

    with col2:
        APQ5 = st.text_input('Shimmer:APQ5')

    with col3:
        APQ = st.text_input('MDVP:APQ')

    with col4:
        DDA = st.text_input('Shimmer:DDA')

    with col5:
        NHR = st.text_input('NHR')

    with col1:
        HNR = st.text_input('HNR')

    with col2:
        RPDE = st.text_input('RPDE')

    with col3:
        DFA = st.text_input('DFA')

    with col4:
        spread1 = st.text_input('spread1')

    with col5:
        spread2 = st.text_input('spread2')

    with col1:
        D2 = st.text_input('D2')

    with col2:
        PPE = st.text_input('PPE')

    # code for Prediction
    parkinsons_diagnosis = ''

    # creating a button for Prediction    
    if st.button("Parkinson's Test Result"):

        user_input = [fo, fhi, flo, Jitter_percent, Jitter_Abs,
                      RAP, PPQ, DDP,Shimmer, Shimmer_dB, APQ3, APQ5,
                      APQ, DDA, NHR, HNR, RPDE, DFA, spread1, spread2, D2, PPE]

        user_input = [float(x) for x in user_input]

        parkinsons_prediction = parkinsons_model.predict([user_input])

        if parkinsons_prediction[0] == 1:
            st.success("The person has Parkinson's disease")
            record_diagnosis("Parkinson's Disease")
        elif parkinsons_prediction[0] == 0:
            st.success("The person does not have Parkinson's disease")
            
         
       



def symptom_based_prediction():
    # Page title
    st.title('Disease Prediction using Symptoms')

    no_symptom = 'No Symptom'
    symptoms_list = df_severity['Symptom'].unique().tolist()
    symptoms_list.append(no_symptom)

    # Dropdowns for selecting symptoms
    symptom_inputs = []
    for i in range(9):
        symptom = st.selectbox(f'Select Symptom {i + 1}', symptoms_list, index=symptoms_list.index(no_symptom))
        symptom_inputs.append(symptom)

    weights = []
    for symptom in symptom_inputs:
        weight = df_severity[df_severity['Symptom'] == symptom]['weight'].values[0] if symptom != no_symptom else 0
        weights.append(weight)

    while len(weights) < 17:
        weights.append(0)

    # Prediction button
    if st.button('Predict Disease'):
        input_data = pd.DataFrame([weights], columns=[f'Symptom {i+1}' for i in range(17)])
        gbc_disease = GBC_model.predict(input_data)[0]
        svc_disease = hyper_tuned_svc.predict(input_data)[0]
        svm_disease = model_SVM_init.predict(input_data)[0]

        st.write(f"Gradient Boosting predicts: {gbc_disease}")
        st.write(f"Tuned SVC predicts: {svc_disease}")
        st.write(f"Initial SVM predicts: {svm_disease}")
        st.write("GBC Accuracy: 99.59%")
        st.write("SVC Accuracy: 99.79%")
        st.write("SVM Accuracy: 99.79%")
        record_diagnosis(f"Symptoms-based prediction: GBC - {gbc_disease}; SVC - {svc_disease}; SVM - {svm_disease}")


# Update the display_diagnoses function to use SQLite
def display_diagnoses():
    """Display the diagnosis history for the logged-in user."""
    st.title('Your Diagnosis History')
    user = st.session_state["current_user"]
    diagnoses = get_user_diagnoses(user)
    if diagnoses:
        st.write(f"Diagnoses for {user}:")
        for index, diagnosis in enumerate(diagnoses.split(", "), 1):
            st.write(f"{index}. {diagnosis}")
    else:
        st.write("No diagnosis history found.")



def main_app():
    with st.sidebar:
        selected = option_menu(
            'Multiple Disease Prediction System',
            ['Diabetes Prediction', 'Heart Disease Prediction', 'Parkinsons Prediction', 'Prediction based on Symptoms', 'Diagnosis'],
            default_index=0
        )


    if selected == 'Diabetes Prediction':
        diabetes_prediction()
    elif selected == 'Heart Disease Prediction':
        heart_disease_prediction()
    elif selected == 'Parkinsons Prediction':
        parkinsons_prediction()
    elif selected == 'Prediction based on Symptoms':
        symptom_based_prediction()
    elif selected == 'Diagnosis':
        display_diagnoses()



if __name__ == "__main__":
    if check_password():
        main_app()
    else:
        st.stop()
