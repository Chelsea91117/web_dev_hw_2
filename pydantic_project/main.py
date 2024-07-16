from pydantic import BaseModel, EmailStr, Field, field_validator, ValidationError


class Address(BaseModel):
    city: str = Field(min_length=2, description="The name of the city")
    street: str = Field(min_length=3, description="The name of the street")
    house_number: int = Field(gt=0, description="The house number must be greater than zero")


class User(BaseModel):
    name: str = Field(min_length=2, description="The name of the user")
    age: int = Field(gt=0, le=120, description="Age must be between 0 and 120")
    email: EmailStr
    is_employed: bool
    address: Address


    @field_validator('name')
    def validate_name(cls, value):
        if not value.isalpha():
            raise ValueError("Name must contain only letters")
        return value



    @field_validator('is_employed')
    def check_age_and_employment(cls, value, values):
        age = values.data.get('age')
        if value and age is not None and age < 18:
            raise ValueError('User must be employed at least 18 years old')
        return value



def process_json(some_json_string):
    try:
        user = User.parse_raw(some_json_string)
        return user.json()
    except ValidationError as e:
        print("Validation error:", e)


right_json_string = """{
    "name": "Peter",
    "age": 29,
    "email": "peter@yahoo.com",
    "is_employed": true,
    "address": {
        "city": "London",
        "street": "St. Patrick",
        "house_number": 99
    }
}"""

wrong_json_string = """{
    "name": "Dan",
    "age": 17,
    "email": "dan@yahoo.com",
    "is_employed": true,
    "address": {
        "city": "Moscow",
        "street": "Suzdal",
        "house_number": 15
    }
}"""


print(process_json(right_json_string))
print(process_json(wrong_json_string))