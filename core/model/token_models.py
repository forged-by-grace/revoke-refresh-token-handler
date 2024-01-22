from pydantic import EmailStr, Field
from dataclasses_avroschema.pydantic import AvroBaseModel

id_description: str = "Used to identify the account"


class RevokeToken(AvroBaseModel):
    id: str = Field(description='A string used to identify an account')
    token: str = Field(description='A string representing the refresh token.')
    device_ip: str = Field(description='A string representing the IP address of the current device.')
