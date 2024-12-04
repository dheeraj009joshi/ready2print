from marshmallow import Schema, fields, validate

class PrinterOwnerSchema(Schema):
    _id=fields.Str()
    name = fields.Str()
    email = fields.Str()
    password = fields.Str()
    phoneNo=fields.Str(validate=validate.Regexp(
            r'^\+?1?\d{9,15}$',  # Regex to validate mobile numbers with optional country code
            error="Invalid mobile number format",
        ))
    location=fields.Str()
    role=fields.Str(default="PRINTER")
    PrintsRequestsAssigned = fields.List(fields.Nested("PrintsRequests"))
    credits=fields.Int(default=0)