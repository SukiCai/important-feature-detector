import re
import sys
import time
import sklearn
import numpy as np
import pandas as pd
import seaborn as sns
import PySimpleGUI as sg
import matplotlib.pyplot as plt
import apply_to_db
from pandas import *
from config import *
from sklearn import metrics
from collections import Counter
from pandas.api.types import is_string_dtype
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def file_clean():
    columns_dropped = open(OUTPUT_FOLDER.joinpath("columns_dropped.csv"), "w+")
    columns_dropped.truncate()
    columns_dropped.close()
    apply_to_ui = open(OUTPUT_FOLDER.joinpath("apply_to_ui.csv"), "w+")
    apply_to_ui.truncate()
    apply_to_ui.close()

class RandomForest:
    # Customize Input
    file_to_analyze = ''            # Path to analysing target file
    result_to_store = ''            # Path to result storing file
    label_column = ''               # Label column name
    pre_set_accuracy = 0.00         # Manual pre-set target accuracy
    pre_set_threshold = 0.00        # Manual pre-set dropping feature cutoff
    columns_manul_drop = []         # Manual drop features
    columns_contain_string = []     # Auto detected
    columns_to_drop = []            # Auto optimized
    data = pd.DataFrame()
    columns_to_recover = pd.DataFrame()

    # Parameterized constructor
    def __init__(self, analyze_file, result_file, classify_target, target_accuracy, cutoff, manul_drop):
        self.file_to_analyze = analyze_file
        self.result_to_store = result_file
        self.label_column = classify_target
        self.pre_set_accuracy = target_accuracy
        self.pre_set_threshold = cutoff
        self.columns_manul_drop = manul_drop

    # Helper Functions
    def clean_rows(self,df):
        assert isinstance(df, pd.DataFrame), "df needs to be a pd.DataFrame"
        df.dropna(inplace=True)
        indices_to_keep = ~df.isin([np.nan, np.inf, -np.inf]).any(1)
        return df[indices_to_keep].astype(np.float64)
    def clean_columns(self,df):
        df.drop(columns=self.columns_to_drop, axis=1, inplace=True)          # Drop least important columns
        df.drop(columns=self.columns_contain_string, axis=1, inplace=True)   # Drop non-numeric columns
        df.drop(columns=self.columns_manul_drop, axis=1, inplace=True)       # Drop manul excluded columns
        return df
    def reorder_columns(self,df):
        first_column = df.pop(self.label_column)
        df.insert(0, self.label_column, first_column)
    def get_string_columns(self,df):
        for x in range(0, len(df.columns) - 1):
            if is_string_dtype(df[df.columns[x]]):
                self.columns_contain_string.append(df.columns[x])
    def rebuild(self):
        self.columns_contain_string = []
        self.start()
        sys.exit()
    def visualize(self,feature_imp):
        feature_imp.sort_values(inplace=True,ascending=False)
        sns.barplot(x=feature_imp, y=feature_imp.index)
        plt.xlabel('Feature Importance Score')
        plt.ylabel('Features')
        plt.title("Visualizing Important Features")
        plt.legend()
        plt.show()

    def start(self):
    # 0. Data Cleanning
        self.data = pd.read_csv(self.file_to_analyze)
        self.data.head()
        self.get_string_columns(self.data)
        self.columns_to_recover = self.data[self.columns_contain_string].copy()
        self.clean_columns(self.data)
        self.clean_rows(self.data)
        self.buildRandomForest()

    def buildRandomForest(self):
    # 1. Build the Classifier
        data = self.data
        # Split dataset
        X=data.loc[:, data.columns!=self.label_column]  # Features
        y=data[self.label_column]  # Label
        X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.3, train_size=0.7)
        # Create a Gaussian Classifier
        clf=RandomForestClassifier(n_estimators=55,max_depth=35,max_leaf_nodes=25)
        # Train the model
        clf.fit(X_train,y_train)
        y_pred=clf.predict(X_test)
        # Model Accuracy
        print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
    # 2. Finding Important Features
        feature_imp = pd.Series(clf.feature_importances_,index=data.columns.drop(self.label_column))
        feature_imp_sorted = feature_imp.sort_values(ascending=False)
        print(feature_imp_sorted)
        last_index= len(feature_imp_sorted) - 1
        # Rebuild the whole modle until reaching the pre-set accuracy
        if (metrics.accuracy_score(y_test, y_pred) < self.pre_set_accuracy):
            # Remove the least important column with importance rate less than the threshold
            if (metrics.accuracy_score(y_test, y_pred) < (self.pre_set_accuracy - 0.02)):
                self.rebuild()
            elif (feature_imp_sorted[last_index] < self.pre_set_threshold):
                column_to_drop = feature_imp_sorted[feature_imp_sorted == feature_imp_sorted[last_index]].index[0]
                self.columns_to_drop.append(column_to_drop)
                print(self.columns_to_drop)
            self.rebuild()
        pd.DataFrame(self.columns_to_drop).to_csv(OUTPUT_FOLDER.joinpath("columns_dropped.csv"),index=False,header=False)
    # 4. Weight the indicator
        self.reorder_columns(data)
        for x in range(0, len(data.columns) - 1):
            if (data.columns[x+1] == feature_imp.keys()[x]):
                scalar = clf.feature_importances_[x]
                data[data.columns[x+1]] = data[data.columns[x+1]].apply(lambda x: x*scalar)
            else:
                print("Wrong Order")
        data['weighted_score'] = data.drop(self.label_column, axis=1).sum(axis=1)
    # 5. Store weigted indicator
        data = pd.concat((self.columns_to_recover,data),axis=1, join="inner")
        data.to_csv(self.result_to_store,index=False,header=True)
    # 7. Visualize Result - Bar Chart
        self.visualize(feature_imp)