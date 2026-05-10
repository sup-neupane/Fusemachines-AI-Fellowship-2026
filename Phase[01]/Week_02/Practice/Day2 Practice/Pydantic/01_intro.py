# Why use Pydantic?
# 1. Checks data types automatically
# 2. Validates data format and constraints
# 3. Converts raw input into clean, structured Python objects

# General Workflow:
# 1. Define a Pydantic model (schema/class)
# 2. Pass raw input data (dict/JSON)
# 3. Pydantic validates and converts the data
# 4. Use the validated object safely in your program


from pydantic import BaseModel #type:ignore
class Patient(BaseModel):
    name : str
    age : int

def insert_patient_data(patient : Patient):
    print(f"Name : {patient.name}")
    print(f"Age : {patient.age}")
    print("Inserted")

patient_info = {'name': 'Ron', 'age' : 30}

patient1 = Patient(**patient_info)

insert_patient_data(patient1)

