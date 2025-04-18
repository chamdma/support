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