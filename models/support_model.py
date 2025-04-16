from mongoengine import Document, StringField, ObjectIdField, BooleanField,DateTimeField
from datetime import datetime

class SupportCase(Document):
    id = StringField(primary_key=True, required=True)
    case_id = StringField(required=True, unique=True)
    customer_id = StringField()
    customer_name = StringField(required=True)
    customer_email = StringField(required=True)
    customer_fname = StringField(required=True)
    customer_lname = StringField(required=True)
    email_subject = StringField(required=True)
    issue_detail = StringField(required=True)
    case_status = StringField(default="Work in Progress")
    update_profile = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow) 