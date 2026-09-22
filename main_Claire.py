# AI USAGE STATEMENT: I used AI to help with labeling the graphs.


import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import statistics
from patient_Claire import * 

# code for printing headers
df = pd.read_csv("/Users/clair/Documents/BME 2315/Module 1/BME2315_Module1/Metadata and Protein Data for Module 1.csv")

for header in df.columns:
    print(header)

######### code for assignment starts here:
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
# Analyzing amyloid beta levels between female and male patients

# start with empty lists for amyloid beta levels in female and male respectively
abeta42_female = []
abeta42_male = []

for patient in Patient.filter(Patient.all_patients, sex = "Female"):
    abeta42_female.append(patient.abeta42_level)
for patient in Patient.filter(Patient.all_patients, sex = "Male"):
    abeta42_male.append(patient.abeta42_level)

# calculating the mean of each data set for female/male
x_female_bar = statistics.mean(abeta42_female)
x_male_bar = statistics.mean(abeta42_male)

# calculating the standard deviation for female/male
abeta42_female_stdev = statistics.stdev(abeta42_female)
abeta42_male_stdev = statistics.stdev(abeta42_male)


# print calculations
print(f'x_female_bar = {x_female_bar}, abeta42_female_stdev {abeta42_female_stdev}')
print(f'x_male_bar = {x_male_bar}, abeta42_male_stdev {abeta42_male_stdev}')

# setting up axis labels, heights, error bar length
patient_sex_cols = ['Female Patients', 'Male Patients']
mean_abeta42 = [x_female_bar, x_male_bar]
stdev_abeta42 = [abeta42_female_stdev, abeta42_male_stdev]

yerr = [np.zeros(len(mean_abeta42)), stdev_abeta42] # sets the bottom as zero

# plot graph with colors and error bars
plt.bar(patient_sex_cols, mean_abeta42, yerr = yerr, capsize=10, color=["pink", "blue"])
plt.title("Average Aβ42 Levels by Sex") # set title
#labeling axises
plt.xlabel("Sex")
plt.ylabel("Average Aβ42 Level (pg/ug)")
plt.show()

########## scatter plot code: 
# Analyzing correlation between amyloid beta levels and age of death
# creating empty lists for patients age at death and amyloid beta levels
patient_age_at_death = []
patient_abeta42 = []

# populating the empty lists above
for patient in Patient.all_patients:
    patient_age_at_death.append(patient.age_at_death)
for patient in Patient.all_patients:
    patient_abeta42.append(patient.abeta42_level)

# defining x and y axises
X = patient_age_at_death # independent variable (age at death)
y = patient_abeta42 # dependent variable (amyloid beta level)

# adding labels and titles
plt.scatter(X, y, color='blue')
plt.xlabel('Age at Death (Years)')
plt.ylabel('Aβ42 Level (pg/ug)')
plt.title('Scatter Plot of Age at Death vs Aβ42 Level')
plt.show()