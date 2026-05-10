from pydantic import BaseModel, EmailStr, Field #type:ignore
from typing import List, Dict , Optional, Annotated  

class Patients(BaseModel):
    name : Annotated[str, Field(max_length = 50, title = "Name of the patient")]
    age : int = Field(gt = 0)  #Constraint
    email : EmailStr
    weight : float 
    married : Optional[bool] = False   #Optional field, Default Value
    allergies : List[str]
    contact : Dict[str , str]

paatient_record = {'name':'Jack', 'age':30,'email':'jack@gmail.com', 'weight':60.5,
                   'allergies':['Peanut','Pollen'],
                   'contact':{
                   'number':'9000000000'
                }}

patient1 = Patients(**paatient_record)

def view_record(patient : Patients):
    for key,value in patient:
        print(f"{key}:{value}")

view_record(patient1)

