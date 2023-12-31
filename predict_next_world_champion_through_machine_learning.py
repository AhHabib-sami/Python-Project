# -*- coding: utf-8 -*-
"""Predict Next World Champion through Machine Learning

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jLt1OJmNu1pQHtthD1H5GnyKaaj7tx-Z

# Libraries
"""

import pandas as pd # Needed For Various Python Built-in Functions
from sklearn.model_selection import train_test_split # Used to Split the dataset into train_dataset and test_dataset
from sklearn.preprocessing import StandardScaler # Needed to ensures that all of the features are given equal importance during modeling
from sklearn.naive_bayes import MultinomialNB # Naive Bayes Model
from sklearn.neighbors import KNeighborsClassifier # KNN Model
from sklearn.tree import DecisionTreeClassifier # Decision Tree Model
from sklearn.linear_model import LogisticRegression # Logistic Regression
from sklearn.svm import SVC # SVM Model
from sklearn.metrics import confusion_matrix # Used for model evaluation, that means in depth details of testing and generates accuracy for the model
from sklearn.calibration import calibration_curve # Used to Plot the Prediction Result of a binary classifier Trained Model
import seaborn as sns # Used to Plot the Heatmap of the Co-Relation Diagram
import matplotlib.pyplot as plt # Used to declare the the figure or frame size

"""# Load dataset"""

from google.colab import files
df = files.upload()

"""# Data Pre-processing

## Dataset Shape
"""

df.shape

"""## Dataset Summary"""

df.describe()

"""## Total Null Values"""

df.isnull().sum()

"""## All Data types"""

df.dtypes

"""## Show all the categorical attributes"""

cat_cols = [col for col in df.columns if df[col].dtype == 'object']
cat_cols

"""## Dataset Glimpse"""

df.head()

"""## Rename Problematic Columns"""

df = df.rename(columns={'Score Percentage': 'Score_Percentage'})

"""## Unique values"""

for col in df.columns:
    print(f'Unique values for {col}:')
    print(df[col].unique())
    print('---')

"""## Mapping the categorical data to numarical"""

df['Host'] = df['Host'].map({'Netherlands': 14, 'United States': 5, 'Canada' : 1, 'Czechia' : 23, 'China' : 8, 'Japan' : 13, 'Sweden' : 25, 'Poland' : 7, 'Russia' : 3, 'Morocco' : 21, 'Thailand' : 65, 'Portugal' : 73, 'Bangladesh' : 19})
df['Country'] = df['Country'].map({'Canada': 1, 'Germany': 2, 'Russia': 3, 'Romania': 4, 'United States': 5, 'Taiwan': 6, 'Poland': 7, 'China': 8, 'New Zealand': 9, 'Singapore': 10, 'Slovakia': 11, 'South Korea': 12, 'Japan': 13, 'Netherlands': 14, 'Australia': 15,
    'Belarus': 16, 'Brazil': 17, 'Argentina': 18, 'Bangladesh': 19, 'Mexico': 20, 'Morocco': 21,'Hong Kong': 22,'Czechia': 23,'Spain': 24,'Sweden': 25,'South Africa': 26,'Venezuela': 27,'North Macedonia': 28,'Iran': 29,
    'India': 30,'Egypt': 31,'Estonia': 32,'Bulgaria': 33,'France': 34,'Ukraine': 35,'Kyrgyzstan': 36,'Norway': 37,'Philippines': 38,'Colombia': 39,'Kazakhstan': 40,'Viet Nam': 41,'Austria': 42,'Indonesia': 43, 'Chile': 44, 'Croatia': 45,
    'Finland': 46,'United Kingdom': 47,'North Korea': 48, 'Georgia': 49, 'Cuba': 50,'Lebanon': 51,
    'Switzerland': 52,'Peru': 53, 'United Arab Emirates': 54, 'Bolivia': 55, 'Saudi Arabia': 56,'Latvia': 57,'Dominican Republic': 58,'Malaysia': 59, 'Lithuania': 60,'Syria': 61, 'Uzbekistan': 62,'Jordan': 63,'Denmark': 64,'Thailand': 65,
    'Armenia': 66,'Turkey': 67,'Pakistan': 68,'Italy': 69,'Costa Rica': 70,'Myanmar': 71,'Serbia': 72,'Portugal': 73,'Tunisia': 74,'Afghanistan': 75,'Ethiopia': 76,
})
df['Gold'] = df['Gold'].astype(int)
df['Silver'] = df['Silver'].astype(int)
df['Bronze'] = df['Bronze'].astype(int)
df['Honorable'] = df['Honorable'].astype(int)
df['Prize'] = df['Prize'].map({'World Champion': 1,'World Champion, Europe Champion': 2,'South Pacific Champion': 3,'North America Champion': 4,'Asia Champion': 5,'Latin America Champion': 6,'Africa and the Middle East Champion': 7,'World Champion, Asia Champion': 8,
                               'Europe Champion': 9,'World Champion, Northern Eurasia Champion': 10,'Asia East Champion': 11,'Asia Pacific Champion': 12,'Asia West Champion': 13,'World Champion, North America Champion': 14,'Northern Eurasia Champion': 15}).fillna(0)
df.head()

df.dtypes

df.isnull().sum()

"""## Fix Missing Values by using the previous values"""

df.fillna(method='ffill', inplace=True)
df.isnull().sum()

"""# Co-Relationship

## Pair Plot
"""

sns.set(style='ticks')
sns.pairplot(df, vars=['Year', 'Host', 'Rank', 'Country', 'Gold', 'Silver', 'Bronze', 'Honorable', 'Score', 'Total', 'Score_Percentage', 'Penalty', 'Prize'], kind='scatter')
plt.show()

sns.set(style='ticks')
sns.pairplot(df, vars=['Year', 'Host', 'Rank', 'Country', 'Gold', 'Silver', 'Bronze', 'Honorable', 'Score', 'Total', 'Score_Percentage', 'Penalty', 'Prize'], kind='reg')
plt.show()

"""## Heatmap"""

corr_matrix = data.corr() # create a correlation matrix
plt.figure(figsize=(12, 12))
cmap = sns.diverging_palette(10, 220, as_cmap=True) # define a custom diverging color palette with red for negative values and blue for positive values
sns.heatmap(corr_matrix, annot=True, cmap=cmap, linewidths=0.1, linecolor='white', fmt='.2f', center=0, square=True, cbar=True, cbar_kws={'orientation': 'horizontal'}) # create a heatmap with colorbar and annotations

"""# Feature Selection"""

# Separate the features and target variable (## Rank Gold Silver Honorable Score Score_Percentage Penalty)
y = df['Prize']
X = df.drop(['Year', 'Date', 'Host', 'City', 'Venue', 'University', 'Country', 'Team', 'Contestant 1', 'Contestant 2', 'Contestant 3', 'Bronze', 'Total', 'Prize'], axis=1)

"""# Dataset Splitting"""

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) # 80% Training and 20% Testing
# Preprocess the data by scaling the features
scaler = StandardScaler()
# X_train = scaler.fit_transform(X_train)
# X_test = scaler.transform(X_test)

"""# Model Training

### Naive Bayes
"""

# Train a Multinomial Naive Bayes classifier on the training set
clf = MultinomialNB()
clf.fit(X_train, y_train)

# Predict the target values for the test set
y_pred = clf.predict(X_test)

# Evaluate the performance of the classifier on the test set
Naive_Bayes_Accuracy = clf.score(X_test, y_test)
print("Naive Bayes Accuracy:", Naive_Bayes_Accuracy*100,"%")

"""### Knn"""

knn = KNeighborsClassifier(n_neighbors=5)

# Fitting the model with training data
knn.fit(X_train, y_train)

# Predicting the class labels for testing data
y_pred = knn.predict(X_test)

# Evaluating the model performance
KNN_Accuracy = knn.score(X_test, y_test)
print("Accuracy:", KNN_Accuracy*100,"%")

"""## Decision Tree"""

# Creating the Decision Tree model
dt = DecisionTreeClassifier()

# Fitting the model with training data
dt.fit(X_train, y_train)

# Predicting the class labels for testing data
y_pred = dt.predict(X_test)

# Evaluating the model performance
Decision_Tree_Accuracy = dt.score(X_test, y_test)
print("Accuracy:", Decision_Tree_Accuracy*100, "%")

"""### Logistic Regression"""

# Creating the Logistic Regression model
lr = LogisticRegression()

# Fitting the model with training data
lr.fit(X_train, y_train)

# Predicting the class labels for testing data
y_pred = lr.predict(X_test)

# Evaluating the model performance
Logistic_Regression_Accuracy = lr.score(X_test, y_test)
print("Accuracy:", Logistic_Regression_Accuracy*100, "%")

"""### SVM"""

# Creating the SVM model
svm = SVC()

# Fitting the model with training data
svm.fit(X_train, y_train)

# Predicting the class labels for testing data
y_pred = svm.predict(X_test)

# Evaluating the model performance
SVM_Accuracy = svm.score(X_test, y_test)
print("Accuracy:", SVM_Accuracy*100, "%")