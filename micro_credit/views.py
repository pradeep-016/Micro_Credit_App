# loan_application/views.py
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import LoanApplication
import numpy as np
import pickle

from sklearn.preprocessing import StandardScaler
import os
import pyrebase
from django.contrib import auth
firebase_config = {
    'apiKey': "AIzaSyB1-2Q18i_snJ5jmNyX-6lSL3xI-3W8SHU",
    'authDomain': "project01-28525.firebaseapp.com",
    'databaseURL': "https://project01-28525-default-rtdb.asia-southeast1.firebasedatabase.app",
    'projectId': "project01-28525",
    'storageBucket': "project01-28525.appspot.com",
    'messagingSenderId': "598483140438",
    'appId': "1:598483140438:web:ead4bf4cf3cc7c743c60f7",
    'measurementId': "G-4B7FZEYNPM"
}

firebase = pyrebase.initialize_app(firebase_config)
auth_fb= firebase.auth()

# Django views
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth_fb.sign_in_with_email_and_password(email, password)
        request.session['uid'] = user['localId']
        return render(request, 'index.html')

    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = auth_fb.create_user_with_email_and_password(email, password)
            auth_fb.send_email_verification(user['idToken'])
            message = "Account created successfully. Please check your email for verification."
            return render(request, 'signup.html', {'message': message})
        except Exception as e:
            message = str(e)
            return render(request, 'signup.html', {'message': message})

    return render(request, 'signup.html')

def forgotpass(request):
    if request.method == 'POST':
        email = request.POST['email']

        try:
            auth_fb.send_password_reset_email(email)
            message = "Password reset email sent. Please check your email for instructions."
            return render(request, 'forgot_password.html', {'message': message})
        except Exception as e:
            message = str(e)
            return render(request, 'forgotpass.html', {'message': message})

    return render(request, 'forgotpass.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

# Get the base directory of your Django project
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Construct the path to the model file relative to the base directory
model_file_path = os.path.join(base_dir, 'micro_credit', 'models', 'loan_application_model_lr.pickle')

# Open the model file
with open(model_file_path, 'rb') as f:
    clf_lr = pickle.load(f)

ss = StandardScaler()

# Define your view functions
def main(request):
    return render(request, 'index.html')
# ...

def Loan_Application(request):
    if request.method == 'GET':
        return render(request, 'Loan_Application.html')

    if request.method == 'POST':
        genders_type = request.POST.get('genders_type')
        marital_status = request.POST.get('marital_status')
        dependents = request.POST.get('dependents')
        education_status = request.POST.get('education_status')
        self_employment = request.POST.get('self_employment')
        
        # Check and handle empty or missing values
        applicantIncome = request.POST.get('applicantIncome')
        coapplicantIncome = request.POST.get('coapplicantIncome')
        loan_amnt = request.POST.get('loan_amnt')
        term_d = request.POST.get('term_d')
        credit_history = request.POST.get('credit_history')

        # Check for empty or missing values and provide defaults if needed
        if applicantIncome is None or applicantIncome == '':
            applicantIncome = 0.0
        else:
            applicantIncome = float(applicantIncome)

        if coapplicantIncome is None or coapplicantIncome == '':
            coapplicantIncome = 0.0
        else:
            coapplicantIncome = float(coapplicantIncome)

        if loan_amnt is None or loan_amnt == '':
            loan_amnt = 0.0
        else:
            loan_amnt = float(loan_amnt)

        if term_d is None or term_d == '':
            term_d = 0.0
        else:
            term_d = float(term_d)

        if credit_history is None or credit_history == '':
            credit_history = 0.0
        else:
            credit_history = float(credit_history)

        property_area = request.POST.get('property_area')

        arr = np.zeros(21)

        arr[0] = applicantIncome
        arr[1] = coapplicantIncome
        arr[2] = loan_amnt
        arr[3] = term_d
        arr[4] = credit_history

        pred = clf_lr.predict([arr])[0]

        if pred == 1:
            res = 'Your Loan Application has been Approved'
        else:
            res = 'Your Loan Application has been Rejected'

        output_dict = {
            'Applicant Income': applicantIncome,
            'Co-Applicant Income': coapplicantIncome,
            'Loan Amount': loan_amnt,
            'Loan Amount Term': term_d,
            'Credit History': credit_history,
            'Gender': genders_type,
            'Marital Status': marital_status,
            'Education Level': education_status,
            'No of Dependents': dependents,
            'Self Employment': self_employment,
            'Property Area': property_area,
        }

        return render(request, 'Loan_Application.html', {'original_input': output_dict, 'result': res})

        