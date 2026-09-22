#AI assistance acknowledgment: OpenAI's Codex helped me add things I did not
#know how to do: making separate figures with plt.figure(), fitting labels
#with plt.tight_layout(), showing both plus and minus SD, passing the lists
#directly to the scatter plot, and displaying numbers to three decimal places.
#It also helped me add the mean difference and a second bar graph to cover
#both my question and the assignment requirements. September 15, 2026.

from patient_faye import *
import matplotlib.pyplot as plt
import statistics
from scipy import stats

Patient.instantiate_from_csv("/Users/fayechiang/Library/Mobile Documents/com~apple~CloudDocs/Computational BME/Module 1/Metadata and Protein Data for Module 1.csv")

#this sorts and prints patients from lowest to highest pTAU concentration
Patient.all_patients.sort(key=Patient.get_ptau, reverse=False)
print("Patients sorted by pTAU concentration:")
for patient in Patient.all_patients:
    print(patient)

#this filters and prints patients using sex and cognitive status
print("\nFemale patients with dementia:")
female_dementia_patients = Patient.filter(
    Patient.all_patients, sex="Female", cognitive_status="Dementia",
    print_patients=True
)
print(f'Number of female patients with dementia = {len(female_dementia_patients)}')

#these lists hold pTAU concentrations 
ptau_dementia = []
ptau_no_dementia = []

for patient in Patient.filter(Patient.all_patients, cognitive_status="Dementia"):
    ptau_dementia.append(patient.ptau)
for patient in Patient.filter(Patient.all_patients, cognitive_status="No dementia"):
    ptau_no_dementia.append(patient.ptau)

#this tests if mean pTAU differs between donors with and without dementia
t_stat, p_val = stats.ttest_ind(ptau_dementia, ptau_no_dementia)
print(f't_stat = {t_stat}, p_val = {p_val}')

#this calculates the standard deviation for each group
x_dementia_bar = statistics.mean(ptau_dementia)
x_no_dementia_bar = statistics.mean(ptau_no_dementia)
ptau_dementia_stdev = statistics.stdev(ptau_dementia)
ptau_no_dementia_stdev = statistics.stdev(ptau_no_dementia)

print(f'\nDementia: n = {len(ptau_dementia)}, mean = {x_dementia_bar:.3f}, SD = {ptau_dementia_stdev:.3f} pg/ug')
print(f'No dementia: n = {len(ptau_no_dementia)}, mean = {x_no_dementia_bar:.3f}, SD = {ptau_no_dementia_stdev:.3f} pg/ug')
print(f'Mean difference (dementia - no dementia) = {x_dementia_bar - x_no_dementia_bar:.3f} pg/ug')

#this bar graph compares pTAU between donors 
Patient_status_cols = ['Dementia', 'No dementia']
mean_status = [x_dementia_bar, x_no_dementia_bar]
stdev_status = [ptau_dementia_stdev, ptau_no_dementia_stdev]

plt.figure()
plt.bar(Patient_status_cols, mean_status, yerr=stdev_status,
        capsize=10, color=["blue", "orange"])
plt.title("Mean pTAU by Dementia Status (± SD)")
plt.xlabel("Cognitive Status")
plt.ylabel("Mean pTAU Concentration (pg/ug)")
#this displays the t-test results above the bars, following the example
y_max = max(mean_status) + max(stdev_status) * 1.2
plt.text(
    0.5, y_max,
    f't = {t_stat:.2f}\np = {p_val:.3e}',
    ha='center',
    va='bottom'
)
plt.ylim(0, y_max + max(stdev_status) * .6)
plt.tight_layout()
plt.show()

#these lists hold pTAU for female and male donors with dementia
ptau_female = []
ptau_male = []

for patient in Patient.filter(Patient.all_patients, sex="Female", cognitive_status="Dementia"):
    ptau_female.append(patient.ptau)
for patient in Patient.filter(Patient.all_patients, sex="Male", cognitive_status="Dementia"):
    ptau_male.append(patient.ptau)

#this calculates the mean and sample standard deviation for each sex
x_female_bar = statistics.mean(ptau_female)
x_male_bar = statistics.mean(ptau_male)
ptau_female_stdev = statistics.stdev(ptau_female)
ptau_male_stdev = statistics.stdev(ptau_male)

print(f'\nFemale donors with dementia: n = {len(ptau_female)}, mean = {x_female_bar:.3f}, SD = {ptau_female_stdev:.3f} pg/ug')
print(f'Male donors with dementia: n = {len(ptau_male)}, mean = {x_male_bar:.3f}, SD = {ptau_male_stdev:.3f} pg/ug')

#this bar graph compares female and male donors as required in the assignment
Patient_sex_cols = ['Female', 'Male']
mean_sex = [x_female_bar, x_male_bar]
stdev_sex = [ptau_female_stdev, ptau_male_stdev]

plt.figure()
plt.bar(Patient_sex_cols, mean_sex, yerr=stdev_sex,
        capsize=10, color=["blue", "orange"])
plt.title("Mean pTAU in Donors with Dementia (± SD)")
plt.xlabel("Sex")
plt.ylabel("Mean pTAU Concentration (pg/ug)")
plt.tight_layout()
plt.show()

#this collects two continuous measurements from each donor for the scatter plot
patient_abeta42 = []
patient_ptau = []

for patient in Patient.all_patients:
    patient_abeta42.append(patient.abeta42)
    patient_ptau.append(patient.ptau)

#this plots amyloid-beta42 on the x-axis and pTAU on the y-axis
X = patient_abeta42
y = patient_ptau

#this fits a straight line to predict pTAU (y) from amyloid-beta42 (X)
slope, intercept, r_value, regression_p_val, std_err = stats.linregress(X, y)

#for linear regression with an intercept, R squared is the correlation squared
#it describes the fraction of variation in pTAU explained by this fitted line
r_squared = r_value ** 2

#these endpoints draw the regression line across the observed amyloid-beta42 range
line_x = [min(X), max(X)]
line_y = [slope * x + intercept for x in line_x]

plt.figure()
plt.scatter(X, y, color='blue')

#this adds the regression line and shows its equation and R squared in the legend
plt.plot(line_x, line_y, color='red',
         label=f'y = {slope:.3f}x {intercept:+.3f}\n$R^2$ = {r_squared:.3f}')
plt.legend()
plt.xlabel('Amyloid-Beta42 Concentration (pg/ug)')
plt.ylabel('pTAU Concentration (pg/ug)')
plt.title('pTAU vs. Amyloid-Beta42 in All Donors')
plt.tight_layout()
plt.show()