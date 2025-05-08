from mongoengine import Document, StringField, BooleanField,DateTimeField,ListField,EmbeddedDocument, EmbeddedDocumentField
from datetime import datetime




class ReplyMail(EmbeddedDocument):
    datetime = DateTimeField()
    email = StringField()

class CaseAnalysis(EmbeddedDocument):
    datetime = DateTimeField()
    detail = StringField()

class CaseUpdate(EmbeddedDocument):
    datetime = DateTimeField()
    detail = StringField()


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
    case_status = StringField(default="Resolved")
    update_profile = BooleanField(default=False)
    case_analysis = ListField(EmbeddedDocumentField(CaseAnalysis))
    case_update = ListField(EmbeddedDocumentField(CaseUpdate))
    reply_mail = ListField(EmbeddedDocumentField(ReplyMail))
    attachments=ListField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow) 
    assigned_to = StringField(default="")
    assigned_to_name=StringField(default="")
    source=StringField(required=True)
    type=StringField(required=True)
    version=StringField(required=True)


    case_analysis = ListField(EmbeddedDocumentField(CaseAnalysis))
    case_update = ListField(EmbeddedDocumentField(CaseUpdate))
    reply_mail = ListField(EmbeddedDocumentField(ReplyMail))
