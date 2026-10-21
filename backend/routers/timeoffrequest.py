from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from pydantic_classes import *
from sql_alchemy import *
from database import get_db
from bal_stdlib import *

router = APIRouter()


@router.get("/timeoffrequest/", response_model=None, tags=["TimeOffRequest"])
def get_all_timeoffrequest(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(TimeOffRequest)
        query = query.options(joinedload(TimeOffRequest.approvedBy))
        query = query.options(joinedload(TimeOffRequest.requester))
        timeoffrequest_list = query.all()

        # Serialize with relationships included
        result = []
        for timeoffrequest_item in timeoffrequest_list:
            item_dict = timeoffrequest_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if timeoffrequest_item.approvedBy:
                related_obj = timeoffrequest_item.approvedBy
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['approvedBy'] = related_dict
            else:
                item_dict['approvedBy'] = None
            if timeoffrequest_item.requester:
                related_obj = timeoffrequest_item.requester
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['requester'] = related_dict
            else:
                item_dict['requester'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(TimeOffRequest).all()


@router.get("/timeoffrequest/count/", response_model=None, tags=["TimeOffRequest"])
def get_count_timeoffrequest(database: Session = Depends(get_db)) -> dict:
    """Get the total count of TimeOffRequest entities"""
    count = database.query(TimeOffRequest).count()
    return {"count": count}


@router.get("/timeoffrequest/paginated/", response_model=None, tags=["TimeOffRequest"])
def get_paginated_timeoffrequest(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of TimeOffRequest entities"""
    total = database.query(TimeOffRequest).count()
    timeoffrequest_list = database.query(TimeOffRequest).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": timeoffrequest_list
    }
@router.get("/timeoffrequest/search/", response_model=None, tags=["TimeOffRequest"])
def search_timeoffrequest(
    id: int = None,
    reason: str = None,
    database: Session = Depends(get_db)
) -> list:
    """Search TimeOffRequest entities by attributes"""
    query = database.query(TimeOffRequest)

    if id is not None:
        query = query.filter(TimeOffRequest.id == id)
    if reason is not None:
        query = query.filter(TimeOffRequest.reason.ilike(f"%{reason}%"))

    results = query.all()
    return results


@router.get("/timeoffrequest/{timeoffrequest_id}/", response_model=None, tags=["TimeOffRequest"])
async def get_timeoffrequest(timeoffrequest_id: int, database: Session = Depends(get_db)) -> TimeOffRequest:
    db_timeoffrequest = database.query(TimeOffRequest).filter(TimeOffRequest.id == timeoffrequest_id).first()
    if db_timeoffrequest is None:
        raise HTTPException(status_code=404, detail="TimeOffRequest not found")

    response_data = {
        "timeoffrequest": db_timeoffrequest,
}
    return response_data



@router.post("/timeoffrequest/", response_model=None, tags=["TimeOffRequest"])
async def create_timeoffrequest(timeoffrequest_data: TimeOffRequestCreate, database: Session = Depends(get_db)) -> TimeOffRequest:

    if timeoffrequest_data.approvedBy :
        db_approvedBy = database.query(Manager).filter(Manager.id == timeoffrequest_data.approvedBy).first()
        if not db_approvedBy:
            raise HTTPException(status_code=400, detail="Manager not found")
    if timeoffrequest_data.requester is not None:
        db_requester = database.query(Employee).filter(Employee.id == timeoffrequest_data.requester).first()
        if not db_requester:
            raise HTTPException(status_code=400, detail="Employee not found")
    else:
        raise HTTPException(status_code=400, detail="Employee ID is required")

    db_timeoffrequest = TimeOffRequest(
        approvedAt=timeoffrequest_data.approvedAt,        endDate=timeoffrequest_data.endDate,        reason=timeoffrequest_data.reason,        startDate=timeoffrequest_data.startDate,        status=timeoffrequest_data.status.name,        submittedAt=timeoffrequest_data.submittedAt,        approvedBy_id=timeoffrequest_data.approvedBy,        requester_id=timeoffrequest_data.requester        )

    database.add(db_timeoffrequest)
    database.flush()
    database.refresh(db_timeoffrequest)




    database.commit()
    database.refresh(db_timeoffrequest)
    return db_timeoffrequest


@router.post("/timeoffrequest/bulk/", response_model=None, tags=["TimeOffRequest"])
async def bulk_create_timeoffrequest(items: list[TimeOffRequestCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple TimeOffRequest entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.requester:
                raise ValueError("Employee ID is required")

            db_timeoffrequest = TimeOffRequest(
                approvedAt=item_data.approvedAt,                endDate=item_data.endDate,                reason=item_data.reason,                startDate=item_data.startDate,                status=item_data.status.name,                submittedAt=item_data.submittedAt,                approvedBy_id=item_data.approvedBy,                requester_id=item_data.requester            )
            database.add(db_timeoffrequest)
            database.flush()  # Get ID without committing
            created_items.append(db_timeoffrequest.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} TimeOffRequest entities"
    }


@router.delete("/timeoffrequest/bulk/", response_model=None, tags=["TimeOffRequest"])
async def bulk_delete_timeoffrequest(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple TimeOffRequest entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_timeoffrequest = database.query(TimeOffRequest).filter(TimeOffRequest.id == item_id).first()
        if db_timeoffrequest:
            database.delete(db_timeoffrequest)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} TimeOffRequest entities"
    }

@router.put("/timeoffrequest/{timeoffrequest_id}/", response_model=None, tags=["TimeOffRequest"])
async def update_timeoffrequest(timeoffrequest_id: int, timeoffrequest_data: TimeOffRequestCreate, database: Session = Depends(get_db)) -> TimeOffRequest:
    db_timeoffrequest = database.query(TimeOffRequest).filter(TimeOffRequest.id == timeoffrequest_id).first()
    if db_timeoffrequest is None:
        raise HTTPException(status_code=404, detail="TimeOffRequest not found")

    setattr(db_timeoffrequest, 'approvedAt', timeoffrequest_data.approvedAt)
    setattr(db_timeoffrequest, 'endDate', timeoffrequest_data.endDate)
    setattr(db_timeoffrequest, 'reason', timeoffrequest_data.reason)
    setattr(db_timeoffrequest, 'startDate', timeoffrequest_data.startDate)
    setattr(db_timeoffrequest, 'status', timeoffrequest_data.status.name)
    setattr(db_timeoffrequest, 'submittedAt', timeoffrequest_data.submittedAt)
    if timeoffrequest_data.approvedBy is not None:
        db_approvedBy = database.query(Manager).filter(Manager.id == timeoffrequest_data.approvedBy).first()
        if not db_approvedBy:
            raise HTTPException(status_code=400, detail="Manager not found")
        setattr(db_timeoffrequest, 'approvedBy_id', timeoffrequest_data.approvedBy)
    else:
        setattr(db_timeoffrequest, 'approvedBy_id', None)
    if timeoffrequest_data.requester is not None:
        db_requester = database.query(Employee).filter(Employee.id == timeoffrequest_data.requester).first()
        if not db_requester:
            raise HTTPException(status_code=400, detail="Employee not found")
        setattr(db_timeoffrequest, 'requester_id', timeoffrequest_data.requester)
    database.commit()
    database.refresh(db_timeoffrequest)

    return db_timeoffrequest


@router.delete("/timeoffrequest/{timeoffrequest_id}/", response_model=None, tags=["TimeOffRequest"])
async def delete_timeoffrequest(timeoffrequest_id: int, database: Session = Depends(get_db)):
    db_timeoffrequest = database.query(TimeOffRequest).filter(TimeOffRequest.id == timeoffrequest_id).first()
    if db_timeoffrequest is None:
        raise HTTPException(status_code=404, detail="TimeOffRequest not found")
    # Snapshot the columns before deleting: cascading the association-class
    # links loads relationship collections whose back-references would make
    # the JSON encoder recurse endlessly on the live object.
    deleted_timeoffrequest = {
        attr.key: getattr(db_timeoffrequest, attr.key)
        for attr in db_timeoffrequest.__mapper__.column_attrs
    }
    database.delete(db_timeoffrequest)
    database.commit()
    return deleted_timeoffrequest



