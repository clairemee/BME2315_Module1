# AI USAGE STATEMENT: I used Gemini AI to do stuff I didn't understand like making the return line for the representer method.
    # I also asked AI to explain some of the lines of code that I didn't know.
    # I used AI to add variables so I could filter patients by more attributes.

import csv

class Patient:
    all_patients = []
    # the following lines assign attributes to each patient object 
    def __init__(self, id: str, sex: str, age_at_death: float, cog_status: str, ptau_level: float, abeta42_level: float, brain_weight: int | None):
        self.id = id
        self.sex = sex
        self.age_at_death = age_at_death
        self.cog_status =  cog_status
        self.ptau_level = ptau_level
        self.abeta42_level = abeta42_level
        self.brain_weight = brain_weight
        Patient.all_patients.append(self) # add the patient to the list of patients
    
    # the following lines set how the patient will be displayed as text when printed
    def __repr__(self): 
        return f"Patient {self.id}: (Sex: {self.sex} | Age at Death: {self.age_at_death} | Cognitive Status: {self.cog_status} | Aβ42: {self.abeta42_level} pg/ug | pTAU: {self.ptau_level} pg/ug | Brain Weight: {self.brain_weight} g)"

    # retrieves patient age at death
    def get_age_death(self):
        return self.age_at_death
    
    # the following lines read the data from the csv file and create patient objects
    @classmethod
    def instantiate_from_csv(cls, filename: str):
        with open(filename, encoding = "utf8") as f:
            reader = csv.DictReader(f)
            rows_of_patients = list(reader)
            # iterates through each row of patient data
        for row in rows_of_patients:
            Patient(
                id = row['Donor ID'],
                sex = row['Sex'],
                age_at_death = float(row['Age at Death']),
                cog_status = row['Cognitive Status'],
                ptau_level = float(row['pTAU pg/ug']),
                abeta42_level = float(row['ABeta42 pg/ug']),
                brain_weight = int(row['Fresh Brain Weight']) if row['Fresh Brain Weight'] != 'Unavailable' else None
            )   
    # retrieve patient data with their id   
    @classmethod
    def get_patient(cls, id):
        for patient in Patient.all_patients:
            if id == patient.id: 
                return patient
    # the following lines help to filter patients based on given attributes            
    @classmethod
    def filter(cls, list, id:str = "any",sex:str ="any", age_at_death:int ="any", cog_status:str ="any", ptau_level:int ="any", abeta42_level:int ="any", brain_weight:int ="any"):
        all_patients = list
        remove_list = []
        # grouping attribute names into tuples
        attr_list = (id, sex, age_at_death, cog_status, ptau_level, abeta42_level)
        attr_name = ("id", "sex", "age_at_death", "cog_status", "ptau_level", "abeta42_level")
    # loop through attributes to remove unwanted objects
        for attr in range(len(attr_list)):
            if attr_list[attr] != 'any':
                for patient in all_patients:
                    if getattr(patient, attr_name[attr]) != attr_list[attr]:
                        remove_list.append(patient)
            all_patients = [patient for patient in all_patients if patient not in remove_list]
            remove_list.clear()
        return all_patients
