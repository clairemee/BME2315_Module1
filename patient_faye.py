#AI assistance acknowledgment: OpenAI's Codex helped me add things I did not
#know how to do: printing from the filter with print_patients, clearing the
#patient list before reloading, using utf-8-sig and newline="" to read the CSV,
#and using :.3f to display numbers to three decimal places. September 15, 2026.

import csv

#the code below defines the patient class and keeps a list of all patients
class Patient:
    all_patients = []

    #the constructor gives each patient their attributes
    def __init__(self, donor_id: str, sex: str, cognitive_status: str,
                 ptau: float, abeta42: float):
        self.donor_id = donor_id
        self.sex = sex
        self.cognitive_status = cognitive_status
        self.ptau = ptau
        self.abeta42 = abeta42
        Patient.all_patients.append(self)

    #the representer shows these attributes when a patient is printed
    def __repr__(self):
        return (f"{self.donor_id}: ({self.sex} | {self.cognitive_status} | "
                f"pTAU = {self.ptau:.3f} pg/ug | ABeta42 = {self.abeta42:.3f} pg/ug)")

    #this gets the pTAU concentration so the patients can be sorted
    def get_ptau(self):
        return self.ptau

    @classmethod
    def instantiate_from_csv(cls, filename: str):
        #the code below opens the .csv file and makes a list of its rows
        with open(filename, encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            rows_of_patients = list(reader)

        #this clears the list so loading the file again does not add duplicates
        cls.all_patients.clear()

        #the code below creates a patient object for each row
        for row in rows_of_patients:
            Patient(
                donor_id = row['Donor ID'],
                sex = row['Sex'],
                cognitive_status = row['Cognitive Status'],
                ptau = float(row['pTAU pg/ug']),
                abeta42 = float(row['ABeta42 pg/ug'])
            )

    @classmethod
    def filter(cls, patient_list, sex="any", cognitive_status="any",
               print_patients=False):
        #this keeps patients that match each of the selected attributes
        all_patients = patient_list
        remove_list = []
        attr_list = (sex, cognitive_status)
        attr_name = ("sex", "cognitive_status")

        for attr in range(len(attr_list)):
            if attr_list[attr] != "any":
                for patient in all_patients:
                    if getattr(patient, attr_name[attr]) != attr_list[attr]:
                        remove_list.append(patient)
                all_patients = [patient for patient in all_patients
                                if patient not in remove_list]
                remove_list.clear()

        #this prints the filtered patients when requested
        if print_patients:
            for patient in all_patients:
                print(patient)

        return all_patients