
from marshmallow import Schema, fields, validate

class PrintsDocuments(Schema):
    documentName=fields.Str()
    documentUrl=fields.Str()
    documentPrintQuantity=fields.Int(default=1)
    documentPrintType=fields.Str(validate=validate.OneOf(["colored", "black&white"]))
    documentDescription=fields.Str()

class PrintsRequests(Schema):
    name=fields.Str()
    users = fields.Nested("UserSchema")  # List of users
    printerOwners =fields.Nested("PrinterOwnerSchema")
    PrintsRequestStatus=fields.Boolean()
    documentsAssigned=fields.List(fields.Nested("PrintsDocuments"))
    
    

    
    
    