from marshmallow import Schema, fields,validate

class UserSchema(Schema):
    _id=fields.Str()
    name = fields.Str()
    email = fields.Str()
    password = fields.Str()
    phoneNo=fields.Str(validate=validate.Regexp(
            r'^\+?1?\d{9,15}$',  # Regex to validate mobile numbers with optional country code
            error="Invalid mobile number format",
           
        ))
    role=fields.Str(default="USER")
    PrintRequests = fields.List(fields.Nested("PrintsRequests"))