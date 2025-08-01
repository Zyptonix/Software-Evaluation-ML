# -*- coding: utf-8 -*-
"""422_Project_Group1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1nFxqfVbha9yfAZ09t7cKQ3EV-LjNjul7

# Introduction

In this project we aim to build a model that can classify the quality of a model based on various code-related features. This model will help us automate the assessment of software quality and allow us to identify which parts of our coding is having a greater impact on the performance of the code. It saves time helping us identify problems quicker by using the power of machine learning models for classification.

# Dataset Description

## **Importing Required Python libraries**
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

"""**Load dataset**"""

dataset=pd.read_csv("software_quality_dataset.csv")

"""## Basic Dataset information

**Summarize data**
"""

dataset

dataset.head(10)

print ('Shape of the dataset is {}. This dataset contains {} rows and {} columns.'.format(dataset.shape,dataset.shape[0],dataset.shape[1]))

"""### **Feature Names and its Datatypes**"""

dataset.info()

"""## **Descriptive Analysis**
#### In descriptive Analysis we analysis each variable separately to get inference about the feature.
### **Summary satistics of Numerical Features**

### **Data Spliting**
#### Select and separately store Numerical and Categorical features in different variables.
"""

##Selecting numerical features
numerical_data = dataset.select_dtypes(include='number')

#append the features of numerical_data to list
numerical_features=numerical_data.columns.tolist()

print(f'There are {len(numerical_features)} numerical features:', '\n')
print(numerical_features)

#Selecting categoricalfeatures
categorical_data=dataset.select_dtypes(include= 'object')

#append the features of categorical_data to list
categorical_features=categorical_data.columns.tolist()

print(f'There are {len(categorical_features)} categorical features:', '\n')
print(categorical_features)

# Transposed stats for numerical features

numerical_data.describe().T

"""### **Summary satistics of Categorical features**"""

# Transposed stats for categorical features

categorical_data.describe().T

"""### **Variance of each numerical features**"""

numerical_data.var()

numerical_data.skew()

"""**Skewness Interpretation**

*Lines_of_Code (0.055):  Almost symmetrical – no transformation needed.

*Cycolmatic_Complexity (0.015):  Almost symmetrical – no transformation needed.

*Num_Functions (-0.034):  Almost symmetrical – no transformation needed.

*Code_churn (-0.113):  Slightly left-skewed – not a concern.

*Comment_Density (0.004):  Almost symmetrical – no transformation needed.

*Num_bugs (0.667): Moderately left-skewed – may benefit from transformation.


*Code_owner_experience (-0.042):  Almost symmetrical – no transformation needed.

### **Histograms and Box Plot**
#### To find the distributions and outlier in the each feature
"""

numerical_data.hist(figsize=(12,12),bins=20)
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns

# Select only numerical columns for boxplot analysis
numeric_cols = dataset.select_dtypes(include=['int64', 'float64']).columns

# Set up the figure
plt.figure(figsize=(20, 30))

# Plot boxplots for each numerical feature
for i, col in enumerate(numeric_cols, 1):
    plt.subplot(len(numeric_cols), 1, i)
    sns.boxplot(x=dataset[col], color='skyblue')
    plt.title(f'Boxplot of {col}', fontsize=12)
    plt.tight_layout()

plt.show()

"""## Scatter Diagram"""

# Plot scatter matrix
dataset['Has_Unit_Tests'] = dataset['Has_Unit_Tests'].map({'Yes': 1, 'No': 0})
sns.pairplot(dataset, hue='Quality_Label', diag_kind='kde', plot_kws={'alpha': 0.6})
plt.suptitle("Scatter Plot Matrix of All Features", y=1.02)
plt.show()

"""### **Number Unique values in each feature**"""

numerical_data.nunique()

"""### **Missing Values**"""

numerical_data.isnull().sum()

"""### **Categorical Features**

#### **No of unique values in each categorical feature**
"""

# unique values counts
unique_counts=categorical_data.nunique()
print(unique_counts)

"""### **Barplot of unique value counts in every categorical features**"""

for col in categorical_features:
    plt.title(f'Distribution of {col}')
    categorical_data[col].value_counts().sort_index().plot(kind='bar', rot=0, xlabel=col,ylabel='count')
    plt.show()

"""## **Correlation Analysis**
### **Correlation matrix of whole dataset**
"""

# Calculate the correlation matrix
dataset1=pd.read_csv("software_quality_dataset.csv")

dataset1['Quality_Label']=dataset1['Quality_Label'].map({'High':3,'Medium':2,'Low':1})
dataset1['Has_Unit_Tests']=dataset1['Has_Unit_Tests'].map({'No':0,'Yes':1})


print(dataset1)
numerical_data1 = dataset1.select_dtypes(include='number')
correlation_matrix = numerical_data1.corr()
correlation_matrix

"""### **Correlation Heatmap plot of whole dataset**"""

# Plotting the heatmap for correlation matrix
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.3f', linewidths=0.3)
plt.show()

"""### **Generating correlation plot between features and target variable using different method**

#### **Correlation plot between features and target**
"""

fig, ax = plt.subplots(3,1, figsize=(10, 10))
## Correlation coefficient using different methods
dataset1=pd.read_csv("software_quality_dataset.csv")
dataset1['Quality_Label']=dataset1['Quality_Label'].map({'High':3,'Medium':2,'Low':1})
# print(dataset1)
numerical_data1 = dataset1.select_dtypes(include='number')
corr1 = numerical_data1.corr('pearson')[['Quality_Label']].sort_values(by='Quality_Label', ascending=False)
corr2 = numerical_data1.corr('spearman')[['Quality_Label']].sort_values(by='Quality_Label', ascending=False)
corr3 = numerical_data1.corr('kendall')[['Quality_Label']].sort_values(by='Quality_Label', ascending=False)

#setting titles for each plot
ax[0].set_title('Pearson method')
ax[1].set_title('spearman method')
ax[2].set_title('Kendall method')

## Generating heatmaps of each methods
sns.heatmap(corr1, ax=ax[0], annot=True)
sns.heatmap(corr2, ax=ax[1], annot=True)
sns.heatmap(corr3, ax=ax[2], annot=True)

plt.show()

import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency

df=pd.read_csv("software_quality_dataset.csv")
def cramers_v(x, y):
    # Create a contingency table
    contingency_table = pd.crosstab(x, y)
    chi2_statistic, p_value, dof, expected = chi2_contingency(contingency_table)

    # Calculate Cramer's V
    n = contingency_table.sum().sum()
    phi2 = chi2_statistic / n
    r, k = contingency_table.shape
    phi2corr = max(0, phi2 - ((k - 1) * (r - 1)) / (n - 1))
    k_corr = k - (k - 1) * (k - 2) / (n - 1)
    r_corr = r - (r - 1) * (r - 2) / (n - 1)
    v = np.sqrt(phi2corr / min(k_corr - 1, r_corr - 1))

    return v

# List of categorical variables


# Initialize a DataFrame to store the results
cramers_v_matrix = pd.DataFrame(index=categorical_features, columns=categorical_features)

# Calculate Cramér's V for each pair of variables
for var1 in categorical_features:
    for var2 in categorical_features:
        cramers_v_matrix.loc[var1, var2] = cramers_v(df[var1], df[var2])

print(cramers_v_matrix)

"""## **Check imbalance in the data**
#### We have classification problem so we need to check the balance of the given data.
"""

#check Imbalance in data
#group instances based on the classes in Quality_Label variable
dataset1=pd.read_csv("software_quality_dataset.csv")
dataset1['Quality_Label']=dataset1['Quality_Label'].map({'High':2,'Medium':1,'Low':0})
print(dataset1)

class_counts=dataset1.groupby("Quality_Label").size()

columns=['Quality_Label','count','percentage']
outcome=['Low','Medium','High']
count=list()
percentage=list()

#Calculate the percentage of each value of the OUTCOME variable from total
for val in range(3):
    count.append(class_counts[val])
    percent=(class_counts[val]/1600)*100
    percentage.append(percent)

# Convert the calulated values into a dataframe
imbalance_df=pd.DataFrame(list(zip(outcome,count,percentage)),columns=columns)
imbalance_df

"""### **Barplot of Outcome vs Percentage**"""

sns.barplot(data=imbalance_df,x=imbalance_df['Quality_Label'],y=imbalance_df['percentage'])
plt.show()

"""## **SUMMARY**

Performed various exploratory data analysis techniques such as univariate, correlation, visualization on the given software quality dataset also found loow imbalance in the given dataset. From the insights acquired through the analysis we will make better decisions when we do Machine learning model development.

### **Density plots of numerical features**
"""

numerical_data.plot(kind='density',figsize=(14,14),subplots=True,layout=(6,2),title="Density plot of Numerical features",sharex=False)
plt.show()

"""# Dataset pre-processing"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, accuracy_score
from sklearn.metrics import roc_curve, auc
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import label_binarize
from sklearn.metrics import roc_auc_score, roc_curve, auc
from sklearn.multiclass import OneVsRestClassifier

"""## Dealing with Null/Missing Values
Dropping all the rows with null values
"""

# database = pd.read_csv('software_quality_dataset.csv')
# database.isnull().sum()
# database=database.dropna()
# print(database.shape)

"""Replacing the null values with median"""

# Check for missing values
database = pd.read_csv('software_quality_dataset.csv')
missing_values = database.isnull().sum()
print(missing_values)
# Fill missing values with median (less sensitive to outliers)
database['Lines_of_Code'].fillna(database['Lines_of_Code'].median(), inplace=True)
database['Code_Churn'].fillna(database['Code_Churn'].median(), inplace=True)
database['Comment_Density'].fillna(database['Comment_Density'].median(), inplace=True)
print(database.head())

"""## Dealing With Categorical Values"""

# Binary encoding for Has_Unit_Tests
database['Has_Unit_Tests'] = database['Has_Unit_Tests'].map({'Yes': 1, 'No': 0})

# Label encoding for Quality_Label
from sklearn.preprocessing import LabelEncoder
print(database['Quality_Label'])
label_encoder = LabelEncoder()
database['Quality_Label'] = label_encoder.fit_transform(database['Quality_Label'])

# To map back later:
label_mapping = dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))
print("Label Mapping:", label_mapping)
print(database)

"""## Selecting the prominent features"""

database=database[['Lines_of_Code','Has_Unit_Tests','Comment_Density','Code_Owner_Experience','Quality_Label']]

"""## Seperating the features and labels"""

X = database.drop('Quality_Label', axis=1)
y = database['Quality_Label']

"""## Feature Scaling"""

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

"""# Dataset splitting"""

x_train, x_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, stratify=y, random_state=42)
print("Train set size:", x_train.shape)
print("Test set size:", x_test.shape)

"""# Model Training and Pre-processing"""

# Define models
models = {
    "Logistic Regression": LogisticRegression(),
    "K-Nearest Neighbours": KNeighborsClassifier(n_neighbors=5),
    "Gaussian Naive Bayesian": GaussianNB(),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Neural Networks": MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=500, random_state=42),
}

accuracy={}
y_preds={}

# Training the Model and plotting ROC Curve and AUC
for name, model in models.items():
    model.fit(x_train, y_train)
    y_pred = model.fit(x_train, y_train).predict(x_test)
    acc = accuracy_score(y_test, y_pred)
    accuracy[name]=acc
    y_preds[name]=y_pred
    print(f"{name} Accuracy: {acc:.4f}")

"""# Model selection/Comparison analysis

## Bar chart of model accuracies
"""

print(accuracy)

# Plotting
plt.figure(figsize=(8, 5))
plt.bar(accuracy.keys(), accuracy.values(), color='skyblue')
plt.ylabel('Accuracy')
plt.title('Model Accuracy Comparison')
plt.ylim(0, 0.5)
plt.xticks(rotation=45)
plt.show()

"""## Precision, recall comparison"""

for name, model in models.items():
    print(f"Classification Report ({name}):")
    print(classification_report(y_test, y_preds[name], target_names=label_encoder.classes_))

"""## Confusion Matrix"""

for name, model in models.items():
    cm = confusion_matrix(y_test, y_preds[name])
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=label_encoder.classes_, yticklabels=label_encoder.classes_,
            cbar=True, linewidths=0)
    plt.title(f"Confusion Matrix - {name}")
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.tight_layout()
    plt.show()

"""## AUC score, ROC curve"""

# Plot ROC Curves
from sklearn.preprocessing import LabelBinarizer
label_binarizer = LabelBinarizer()
plt.figure(figsize=(10, 7))
y_test_bin = label_binarizer.fit_transform(y_test)
n_classes=3
for name, model in models.items():
    y_score = model.predict_proba(x_test)

    for i in range(n_classes):
        fpr, tpr, _ = roc_curve(y_test_bin[:, i], y_score[:, i])
        roc_auc = auc(fpr, tpr)
        class_name = label_encoder.inverse_transform([i])[0]
        plt.plot(fpr, tpr, label=f"{name} (class {class_name}) AUC = {roc_auc:.2f}")
    plt.plot([0, 1], [0, 1], 'k--')
    plt.title(f"ROC Curves for {name}")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.legend(loc="lower right")
    plt.grid(True)
    plt.tight_layout()
plt.show()
auc_ovr = roc_auc_score(y_test_bin, y_score, multi_class='ovr')
print(f"Overall AUC (OvR): {auc_ovr:.3f}")

"""# Conclusion

So even though the K-Nearest Neighbour algorithm is biased towards high it can still split ‘High’ and ‘Low’ classes more effectively than others and so is the best model for our dataset. Almost all the models struggle with dealing with the dataset as there are no clear linear splits between the data as seen from the scatter diagram. Logistic Regression and Naive Bayes closely follow the KNN algorithm but  the Neural Network Algorithm can be said to be the most evenly distributed algorithm as the ROC curve for each class is greater than or equal to 0.5 but even so it cannot separate the classes well enough. The Decision Tree can be said to have the most balanced confusion matrix as all the predictions can be said to be consistent between the classes as observed from the confusion matrix. Overall this dataset does not have any easy identifiable splits in the features and so almost all the algorithms struggle to give a good result. It was particularly challenging to select the right features to use for the classification but in the end using the regression analysis we were able to select the best 4 features for us to use. This experiment should help develop a basic knowledge on the dataset and can be used as a stepping stone to further research and improve the classification of software around the world.
"""