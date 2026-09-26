# AI USAGE STATEMENT: I used AI to help with labeling the graphs. 
#   I also used AI to help with the linear regression code for the scatter plot because the code from the lecture was not working for me. 
#   Additionally, AI was used to troubleshoot any problems/errors I was having with the code and to explain some lines that I didn't 
#   understand such as the reason for the error bar being set to the top of the bar.


import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import statistics
from patient_Claire import * 
from sklearn.linear_model import LinearRegression

# code for printing headers
df = pd.read_csv("/Users/clair/Documents/BME 2315/Module 1/BME2315_Module1/Metadata and Protein Data for Module 1.csv")

for header in df.columns:
    print(header)

######### code for patient assignment starts here:
# the following line creates objects from the .csv data
Patient.instantiate_from_csv("/Users/clair/Documents/BME 2315/Module 1/BME2315_Module1/Metadata and Protein Data for Module 1.csv") 
# sort and print patients based on age of death
Patient.all_patients.sort(key=Patient.get_age_death, reverse=False)
for patient in Patient.all_patients:
    print(patient)

# filter & print patients based on sex and cognitive status
filtered = Patient.filter(Patient.all_patients, sex = "Female", cog_status= "No dementia")
for patient in filtered:
    print(patient)

########## bar graph code: 
# Analyzing brain weight between dementia and no dementia patients

# start with empty lists for brain weight with dementia and no dementia respectively
brain_weight_dementia = []
brain_weight_no_dementia = []

for patient in Patient.filter(Patient.all_patients, cog_status = "Dementia"):
    if patient.brain_weight is not None:
        brain_weight_dementia.append(patient.brain_weight)
for patient in Patient.filter(Patient.all_patients, cog_status = "No dementia"):
    if patient.brain_weight is not None:
        brain_weight_no_dementia.append(patient.brain_weight)

# calculating the mean of each data set for dementia/no dementia
x_dementia_bar = statistics.mean(brain_weight_dementia)
x_no_dementia_bar = statistics.mean(brain_weight_no_dementia)

# calculating the standard deviation for dementia/no dementia
brain_weight_dementia_stdev = statistics.stdev(brain_weight_dementia)
brain_weight_no_dementia_stdev = statistics.stdev(brain_weight_no_dementia)

# print calculations
print(f'x_dementia_bar = {x_dementia_bar}, brain_weight_dementia_stdev {brain_weight_dementia_stdev}')
print(f'x_no_dementia_bar = {x_no_dementia_bar}, brain_weight_no_dementia_stdev {brain_weight_no_dementia_stdev}')

# setting up axis labels, heights, error bar length
patient_cog_status_cols = ['Dementia', 'No Dementia']
mean_brain_weight = [x_dementia_bar, x_no_dementia_bar]
stdev_brain_weight = [brain_weight_dementia_stdev, brain_weight_no_dementia_stdev]

yerr = [np.zeros(len(mean_brain_weight)), stdev_brain_weight] # sets the error bottom as the top of the bar


t_stat, p_val = stats.ttest_ind(brain_weight_dementia, brain_weight_no_dementia)
print(f't_stat =  {t_stat}, p_val = {p_val}') # finding the p value and t statistic

# plot graph with colors and error bars
plt.bar(patient_cog_status_cols, mean_brain_weight, yerr = yerr, capsize=10, color=["pink", "blue"])
plt.title("Average Brain Weight by Cognitive Status") # set title

#labeling axises
plt.xlabel("Cognitive Status")
plt.ylabel("Average Brain Weight (g)")

# set y-axis range to 1500 so bars and error caps have plenty of room
plt.ylim(0, 1500)

# Position text of p value and t stat 
plt.text(
        0.5, 0.92,
        f"t = {t_stat:.2f}\np = {p_val:.3e}",
        ha = 'center',
        va = 'top',
        transform = plt.gca().transAxes
        )
plt.show()

########## scatter plot code: 
# Analyzing correlation between amyloid beta levels and brain weight
# creating empty lists for patients brain weight and amyloid beta levels
patient_abeta42 = []
patient_brain_weight = []

# populating the empty lists above
for patient in Patient.all_patients:
    if patient.abeta42_level is not None and patient.brain_weight is not None:
        patient_abeta42.append(patient.abeta42_level)
        patient_brain_weight.append(patient.brain_weight)

# defining x and y axises
X = patient_abeta42 # independent variable (amyloid beta level)
y = patient_brain_weight # dependent variable (brain weight)

array_x = np.asarray(patient_abeta42, dtype = float).reshape(-1, 1) # shape: (n_samples, 1)
array_y = np.asarray(patient_brain_weight, dtype = float).ravel() # shape: (n_samples,)

model = LinearRegression()
model.fit(array_x, array_y)

# Create predicted values for the regression line
predicted_y = model.predict(array_x)

# Sort x-values so the line displays correctly
sort_indices = np.argsort(array_x[:, 0])

# adding labels and titles
plt.scatter(array_x.ravel(), array_y, color='blue')
plt.plot(
    array_x[sort_indices].ravel(),
    predicted_y[sort_indices],
    color="red",
    linewidth=2,
    label="Linear regression"
) # adding the regression line

slope = model.coef_[0]
intercept = model.intercept_
r_squared = model.score(array_x, array_y)
plt.text(
    0.55, 0.95,
    f"y = {slope:.3f}x + {intercept:.3f}\nR² = {r_squared:.3f}",
    transform=plt.gca().transAxes,
    verticalalignment="top",
    fontsize=11
) # adding the R^2 value and the line equation

plt.xlabel('Aβ42 Level (pg/ug)')
plt.ylabel('Brain Weight (g)')
plt.title('Scatter Plot of Aβ42 Level vs Brain Weight')
plt.show()