from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from pydantic_classes import *
from sql_alchemy import *
from database import get_db
from bal_stdlib import *

router = APIRouter()

############################################
#   Manager Method Endpoints
############################################





@router.post("/manager/{manager_id}/methods/approveTimeOff/", response_model=None, tags=["Manager Methods"])
async def execute_manager_approveTimeOff(
    manager_id: int,  # the Manager that approveTimeOff runs on
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """Execute the approveTimeOff method on a Manager instance.

    Parameters:
    - request: TimeOffRequest    """
    # Manager.approveTimeOff: load the instance
    _manager_object = database.query(Manager).filter(Manager.id == manager_id).first()
    if _manager_object is None:
        raise HTTPException(status_code=404, detail="Manager not found")
    # Manager.approveTimeOff
    raise HTTPException(
        status_code=501,
        detail="Method 'approveTimeOff' of Manager is modeled but has no implementation - 501, never a fake success",
    )

