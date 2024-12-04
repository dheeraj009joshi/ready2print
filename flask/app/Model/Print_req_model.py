
from marshmallow import Schema, fields, validate

class PrintsDocuments(Schema):
    documentName=fields.Str()
    documentUrl=fields.Str()
    documentPrintQuantity=fields.Int(default=1)
    documentPrintType=fields.Str(validate=validate.OneOf([ "black&white","colored"]))
    documentDescription=fields.Str()

class PrintsRequests(Schema):
    _id=fields.Str()
    name=fields.Str()
    users = fields.Str()  # List of users
    printerOwners =fields.Str()
    PrintsRequestStatus=fields.Boolean()
    documentsAssigned=fields.List(fields.Nested("PrintsDocuments"))
    
    

    
    
    