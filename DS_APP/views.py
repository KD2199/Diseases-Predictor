
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.conf import settings
import urllib
import json
from django.contrib.auth.decorators import login_required
import csv
from django.db.models import F
import pandas as pd
import streamlit as st
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, plot_confusion_matrix, plot_precision_recall_curve, plot_roc_curve
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import StandardScaler
import urllib
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc, accuracy_score, f1_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
import math
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from DS_APP.models import Report_Data
import random
from xgboost import XGBClassifier
import speech_recognition as sr



def home(request):

    if request.method == 'POST':

        username = request.POST['uname']
        contact = request.POST['contact']
        age = request.POST['age']
        email = request.POST['email']
        mean_radius = request.POST['mean_radius']
        mean_texture = request.POST['mean_texture']
        mean_perimeter = request.POST['mean_perimeter']
        mean_area = request.POST['mean_area']
        mean_smoothness = request.POST['mean_smoothness']
        diagnosis = 0

        print(f"{username} {contact} {age} {email} {mean_radius} {mean_texture} {mean_perimeter} {mean_area} {mean_smoothness}")

        rows = [[mean_radius, mean_texture,
                 mean_perimeter, mean_area, mean_smoothness, diagnosis]]

        # name of csv file
        
        # writing to csv file
        with open(filename, 'a+') as csvfile:
            # creating a csv writer object
            csvwriter = csv.writer(csvfile)

            # writing the fields
            # csvwriter.writerow(fields)

            # writing the data rows
            csvwriter.writerows(rows)
            print('Data Added Successfully!!')

        

        # print(np.any(np.isnan(df)))
        # print(np.all(np.isfinite(df)))
        x = df.drop(['diagnosis'], axis=1)
        y = df['diagnosis']
        X_train, X_test, Y_train, Y_test = train_test_split(
            x, y, test_size=0.2, random_state=0)
        sc_x = StandardScaler().fit(X_train)
        X_train = sc_x.transform(X_train)
        X_test = sc_x.transform(X_test)

        classifier = XGBClassifier()
        classifier.fit(X_train, Y_train)
        predictions = classifier.predict(X_test)
        Accuracy = classifier.score(X_test, Y_test).round(2)

        Patient_Id = str(username[0:2]) + \
            str(random.randint(100001, 99999999999))
        print(Patient_Id)

        if Accuracy >= 0.70:
            msg = "Your Test Id is: " + str(Patient_Id)
            messages.success(request, "You Have Breast Cancer")
            messages.success(request, msg)
            obj = Report_Data.objects.create(Patient_Name=username, Patient_Id=Patient_Id, Email=email, Mobile_No=contact, Age=age, mean_radius=mean_radius,
                                             mean_texture=mean_texture,
                                             mean_perimeter=mean_perimeter,
                                             mean_area=mean_area,
                                             mean_smoothness=mean_smoothness,
                                             Test_Result='Positive')
        else:

            msg = "Your Test Id is: " + str(Patient_Id)
            messages.success(
                request, "Congratulation You Don't Have Breast Cancer!")
            messages.success(request, msg)
            obj = Report_Data.objects.create(Patient_Name=username, Patient_Id=Patient_Id, Email=email, Mobile_No=contact, Age=age, mean_radius=mean_radius,
                                             mean_texture=mean_texture,
                                             mean_perimeter=mean_perimeter,
                                             mean_area=mean_area,
                                             mean_smoothness=mean_smoothness,
                                             Test_Result='Negative')

    return render(request, 'index.html')


def search(request):

    return render(request, 'search.html')


def result(request):

    if request.method == 'POST':

        username = request.POST['sr'] or request.POST['sp']
        obj = Report_Data.objects.filter(Patient_Name=username) or Report_Data.objects.filter(
            Patient_Id=username) or Report_Data.objects.filter(Email=username) or Report_Data.objects.filter(Mobile_No=username)
        print(username)

    return render(request, 'result.html', {'obj': obj})


def sresult(request):

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Talk")
        audio_text = r.listen(source)
        print("Time over, thanks")

        username = str(r.recognize_google(audio_text))
        print(username)
        
        obj = Report_Data.objects.filter(Patient_Name=username) or Report_Data.objects.filter(
            Patient_Id=username) or Report_Data.objects.filter(Email=username) or Report_Data.objects.filter(Mobile_No=username)
        print(username)

    return render(request, 'result.html',{'obj': obj})
