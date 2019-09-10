# I wrote this code in Jupyter Notebook but there's some issue with github showing .ipynb files(thread already opened)
# So, I am changing the extension from .ipynb to .py so that if anyone wants, he/she can see the code easily
# For each new line, that code is actually written in new cell of jupyter notebook

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/00267/data_banknote_authentication.txt',names=['Variance','Skewness','Curtosis','Entropy','Class'])

print(df.head())
print(df.isnull().sum())

print(df['Class'].unique())

print(df.info())
print(df['Class'].value_counts())

sns.pairplot(df,hue='Class')

sns.countplot('Class',data=df)

sns.violinplot('Variance',data=df)

sns.violinplot('Skewness',data=df)

plt.figure(figsize=(16,8))
sns.regplot('Skewness','Entropy',data=df)

sns.distplot(df['Variance'])

sns.kdeplot(df['Curtosis'],df['Variance'],cmap='Reds',shade=True)

x = df.iloc[:,:-1]
print(x.head)

y = df.iloc[:,-1]
print(y.head)

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report

train_x,test_x,train_y,test_y = train_test_split(x,y,test_size=.2,random_state=41)

print(train_x.shape)
print(test_x.shape)

from sklearn.linear_model import LogisticRegression
lr = LogisticRegression()
lr.fit(train_x,train_y)
pred_lr = lr.predict(test_x)
print(accuracy_score(test_y,pred_lr)) # 0.9890909090909091

from sklearn.naive_bayes import GaussianNB
gnb = GaussianNB()
gnb.fit(train_x,train_y)
pred_gnb = gnb.predict(test_x)
print(accuracy_score(test_y,pred_gnb)) # 0.8218181818181818

from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier()
rf.fit(train_x,train_y)
pred_rf = rf.predict(test_x)
print(accuracy_score(test_y,pred_rf)) # 1.0

# RandomForest is giving 100% accuracy

print(confusion_matrix(test_y,pred_rf))
print(classification_report(test_y,pred_rf))

# Making AUC-ROC Curve
from sklearn.metrics import roc_curve,roc_auc_score

fin_pred = rf.predict_proba(test_x)[:,1]
print(fin_pred)

fpr,tpr,threshold = roc_curve(test_y,fin_pred)

plt.plot([0,1],[0,1],'k--')
plt.plot(fpr,tpr)
plt.xlabel('FPR')
plt.ylabel('TPR')
plt.title('AUC-ROC Curve')
plt.show()

sc = roc_auc_score(test_y,pred_rf)
print(sc)

# Saving the model
import pickle

fd = open('bank.obj','wb')
pickle.dump(rf,fd)
fd.close()

fl = open('bank.obj','rb')
result = pickle.load(fl)
fl.close()

print(result.score(train_x,train_y))
