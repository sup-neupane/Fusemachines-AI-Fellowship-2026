from pydantic import BaseModel, EmailStr, Field, field_validator #type:ignore
from typing import List, Dict , Optional, Annotated 

class Patients(BaseModel):
    name : str
    age : int 
    email : EmailStr
    weight : float 
    married : Optional[bool] = None
    allergies : Optional[List[str]] = None
    contact : Dict[str , str]

    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        valid_domains = ['gmail.com']
        domain_name = value.split("@")[-1]
        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')
        
        return value
    


paatient_record = {'name':'Jack', 'age':30,'email':'jack@gmail.com', 'weight':60.5,       'allergies':['Peanut','Pollen'],
              'contact':{
                   'number':'9000000000'
              }}

patient1 = Patients(**paatient_record)

def insert_record(patient : Patients):
    for key,value in patient:
        print(f"{key}:{value}")

insert_record(patient1)

#Serialization
temp = patient1.model_dump()
print(temp)