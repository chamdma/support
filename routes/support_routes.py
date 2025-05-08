from fastapi import FastAPI,APIRouter,Body,Request
from models.support_model import SupportCase
from utils import generate_case_id
from auth.generate_token import create_access_token
from datetime import datetime
from bson import ObjectId


router=APIRouter()

@router.post("/support/cases/create")
async def create_support_case(
    request: Request,
    customer_id: str = Body(""),
    customer_name: str = Body(...),
    customer_email: str = Body(...),
    email_subject: str = Body(...),
    issue_detail: str = Body(...),
    customer_fname: str = Body(...),
    customer_lname: str = Body(...),
    update_profile: bool = Body(...),
    source:str=Body(...),
    type: str = Body(...),
    version:str=Body(...)
):
    try:
        created_at = datetime.utcnow()
        updated_at = datetime.utcnow()
        access_token = create_access_token({"case_id": generate_case_id()}) 

        new_case = SupportCase(
            id=ObjectId(),
            case_id=generate_case_id(),
            case_status="Resolved",
            customer_name=customer_name,
            customer_email=customer_email,
            email_subject=email_subject,
            issue_detail=issue_detail,
            customer_fname=customer_fname,      
            customer_lname=customer_lname,    
            created_at=created_at,
            updated_at=updated_at,
            source=source,
            type=type,
            version=version

        )
        new_case.access_token = access_token

        new_case.id = str(new_case.id)
        new_case.save()

        case_data = new_case.to_mongo()
        case_data["created_at"] = case_data["created_at"].isoformat(timespec='seconds') + "Z"
        case_data["updated_at"] = case_data["updated_at"].isoformat(timespec='seconds') + "Z"

        return {
            "status": True,
            "status_code": 200,
            "description": "Customer support added successfully",
            "access_token": access_token,
            "data": [case_data]
        }

    except Exception as e:
        return {
            "status": False,
            "status_code": 500,
            "description": f"Error creating support case: {str(e)}",
            "data": [],
            "error": str(e)
        }
    
@router.post("/support/case/list")
async def list_support_case(
    request:Request,
    search: str = Body(...),
    case_status:str=Body(...),
    assigned_to:str=Body(""),
    sort_by:str=Body("created_at"),
    sort_order:str=Body("asc")                           
):
    try:
        query = SupportCase.objects()
        if search:
            query = query.filter(case_id__icontains=search)
        if case_status:
            query = query.filter(case_status=case_status)

        if assigned_to:
            query = query.filter(assigned_to=assigned_to)
           

        sort_field = "+" + sort_by if sort_order == "asc" else "-" + sort_by
        cases = query.order_by(sort_field)

        cases = query.all() 

        if not cases:
            return {
                "status": True,
                "status_code": 200,
                "description": "No support cases found",
                "data": []
            }
        
        case_list=[
            {
                "case_id":case.case_id,
                "case_status":case.case_status,
                "assigned_to": case.assigned_to,
                "customer_name":case.customer_name,
                "customer_email":case.customer_email,
                "email_subject":case.email_subject,
                "created_at":case.created_at.isoformat(),
                "updated_at":case.updated_at.isoformat(),
                "assigned_to":case.assigned_to

            }
            for case in cases
        ]
        return {
            "status": True,
            "status_code": 200,
            "description": "Customer support case list fetched successfully",
            "data": case_list
        }
    except Exception as e:
        return {
            "status": False,
            "status_code": 500,
            "description": f"Error fetching support cases: {str(e)}"
        }


@router.post("/support/case/detail")
async def detail_support_case(
    request:Request,
    case_id:str=Body(...,embed=True)
):
    try:
        case=SupportCase.objects(case_id=case_id).first()
        if not case:
            return {
                "status": False,
                "status_code": 404,
                "description": "Support case not found",
                "data": []
            }
        case_data={
            "id":str(case.id),
            "case_id": case.case_id,
            "assigned_to":case.assigned_to,
            "assigned_to_name":case.assigned_to_name,
            "case_status":case.case_status,
            "customer_name": case.customer_name,
            "customer_fname": case.customer_fname,
            "customer_lname": case.customer_lname,
            "customer_email": case.customer_email,
            "email_subject":case.email_subject,
            "issue_detail":case.issue_detail,
            "created_at":case.created_at,
            "updated_at":case.updated_at,
            "case_analysis":[
                {
                    "datetime":analysis.datetime.isoformat() +"z",
                    "detail":analysis.detail
                }for analysis in case.case_analysis or []
            ],
            "case_update": [
                {
                    "datetime": update.datetime.isoformat() +"z",
                    "detail": update.detail
                } for update in case.case_update or []
            ],
            "reply_mail": [
                {
                    "datetime": reply.datetime.isoformat() +"z",
                    "email": reply.email
                } for reply in case.reply_mail or []
            ]
        }

        return {
            "status": True,
            "status_code": 200,
            "description": "Customer support added successfully",
            "data": [case_data]
        }

    except Exception as e:
        return {
            "status": False,
            "status_code": 500,
            "description": f"Error fetching support case detail: {str(e)}"
        }
        

@router.post("/support/case/update")
async def update_support_case(
    request:Request,
    case_id:str=Body(...),
    customer_name:str=Body(...),
    customer_fname:str=Body(...),
    customer_lname:str=Body(...),
    update_detail: str = Body(default=None),
    analysis_detail: str = Body(default=None),
    reply_mail: str = Body(default=None)
):
    try:
        
        case = SupportCase.objects(case_id=case_id).first()


        if not case:
            return {
                "status_code": 404,
                "description": "SupportCase not found",
                "status": False,
                "data": []
            }
        update_data = {
            "set__customer_name": customer_name,
            "set__customer_fname": customer_fname,
            "set__customer_lname": customer_lname,
            "set__updated_at": datetime.utcnow()
        }

        if not update_data:
            return {
                "status_code": 400,
                "description": "No valid fields to update",
                "status": False
            }
        case.update(**update_data)

        if update_detail:
            case.update(push__case_update={
                "datetime": datetime.utcnow(),
                "detail": update_detail
            })

        if analysis_detail:
            case.update(push__case_analysis={
                "datetime": datetime.utcnow(),
                "detail": analysis_detail
            })

        if reply_mail:
            case.update(push__reply_mail={
                "datetime": datetime.utcnow(),
                "email": reply_mail
            })

        return {
            "status_code": 200,
            "description": "case updated successfully",
            "status": True,
            "data": [{"case_id": case_id}]
        }

    except Exception as e:
        return {
            "status_code": 500,
            "description": f"Error updating user: {str(e)}",
            "status": False
        }

      