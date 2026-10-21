from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from pydantic_classes import *
from sql_alchemy import *
from database import get_db
from bal_stdlib import *

router = APIRouter()


@router.get("/employee/", response_model=None, tags=["Employee"])
def get_all_employee(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Employee)
        query = query.options(joinedload(Employee.manager))
        employee_list = query.all()

        # Serialize with relationships included
        result = []
        for employee_item in employee_list:
            item_dict = employee_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if employee_item.manager:
                related_obj = employee_item.manager
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['manager'] = related_dict
            else:
                item_dict['manager'] = None

            # Add many-to-many and one-to-many relationship objects (full details)
            timeoffrequest_list = database.query(TimeOffRequest).filter(TimeOffRequest.requester_id == employee_item.id).all()
            item_dict['timeOffRequests'] = []
            for timeoffrequest_obj in timeoffrequest_list:
                timeoffrequest_dict = timeoffrequest_obj.__dict__.copy()
                timeoffrequest_dict.pop('_sa_instance_state', None)
                item_dict['timeOffRequests'].append(timeoffrequest_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Employee).all()


@router.get("/employee/count/", response_model=None, tags=["Employee"])
def get_count_employee(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Employee entities"""
    count = database.query(Employee).count()
    return {"count": count}


@router.get("/employee/paginated/", response_model=None, tags=["Employee"])
def get_paginated_employee(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Employee entities"""
    total = database.query(Employee).count()
    employee_list = database.query(Employee).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": employee_list
        }

    result = []
    for employee_item in employee_list:
        timeOffRequests_ids = database.query(TimeOffRequest.id).filter(TimeOffRequest.requester_id == employee_item.id).all()
        item_data = {
            "employee": employee_item,
            "timeOffRequests_ids": [x[0] for x in timeOffRequests_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }
@router.get("/employee/search/", response_model=None, tags=["Employee"])
def search_employee(
    email: str = None,
    id: int = None,
    name: str = None,
    position: str = None,
    database: Session = Depends(get_db)
) -> list:
    """Search Employee entities by attributes"""
    query = database.query(Employee)

    if email is not None:
        query = query.filter(Employee.email.ilike(f"%{email}%"))
    if id is not None:
        query = query.filter(Employee.id == id)
    if name is not None:
        query = query.filter(Employee.name.ilike(f"%{name}%"))
    if position is not None:
        query = query.filter(Employee.position.ilike(f"%{position}%"))

    results = query.all()
    return results


@router.get("/employee/{employee_id}/", response_model=None, tags=["Employee"])
async def get_employee(employee_id: int, database: Session = Depends(get_db)) -> Employee:
    db_employee = database.query(Employee).filter(Employee.id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    timeOffRequests_ids = database.query(TimeOffRequest.id).filter(TimeOffRequest.requester_id == db_employee.id).all()
    response_data = {
        "employee": db_employee,
        "timeOffRequests_ids": [x[0] for x in timeOffRequests_ids]}
    return response_data



@router.post("/employee/", response_model=None, tags=["Employee"])
async def create_employee(employee_data: EmployeeCreate, database: Session = Depends(get_db)) -> Employee:

    if employee_data.manager :
        db_manager = database.query(Manager).filter(Manager.id == employee_data.manager).first()
        if not db_manager:
            raise HTTPException(status_code=400, detail="Manager not found")

    db_employee = Employee(
        email=employee_data.email,        hiredDate=employee_data.hiredDate,        name=employee_data.name,        position=employee_data.position,        manager_id=employee_data.manager        )

    database.add(db_employee)
    database.flush()
    database.refresh(db_employee)

    if employee_data.timeOffRequests:
        # Validate that all TimeOffRequest IDs exist
        for timeoffrequest_id in employee_data.timeOffRequests:
            db_timeoffrequest = database.query(TimeOffRequest).filter(TimeOffRequest.id == timeoffrequest_id).first()
            if not db_timeoffrequest:
                raise HTTPException(status_code=400, detail=f"TimeOffRequest with id {timeoffrequest_id} not found")

        # Update the related entities with the new foreign key
        database.query(TimeOffRequest).filter(TimeOffRequest.id.in_(employee_data.timeOffRequests)).update(
            {TimeOffRequest.requester_id: db_employee.id}, synchronize_session=False
        )
        database.flush()



    timeOffRequests_ids = database.query(TimeOffRequest.id).filter(TimeOffRequest.requester_id == db_employee.id).all()
    response_data = {
        "employee": db_employee,
        "timeOffRequests_ids": [x[0] for x in timeOffRequests_ids]    }
    database.commit()
    database.refresh(db_employee)
    return response_data


@router.post("/employee/bulk/", response_model=None, tags=["Employee"])
async def bulk_create_employee(items: list[EmployeeCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Employee entities at once"""
    if any(getattr(item, field, None) for item in items for field in ['timeOffRequests']):
        raise HTTPException(status_code=422, detail="Bulk creation of Employee with relationships is not supported; use POST /employee/ to validate and persist its relationships")
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_employee = Employee(
                email=item_data.email,                hiredDate=item_data.hiredDate,                name=item_data.name,                position=item_data.position,                manager_id=item_data.manager            )
            database.add(db_employee)
            database.flush()  # Get ID without committing
            created_items.append(db_employee.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Employee entities"
    }


@router.delete("/employee/bulk/", response_model=None, tags=["Employee"])
async def bulk_delete_employee(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Employee entities at once"""
    # Aggregate deletion must account for every related lower bound. Until it
    # shares that validation, use the guarded individual delete endpoint.
    if ids:
        raise HTTPException(status_code=409, detail="Bulk deletion of Employee can violate required relationships and is not supported; use the individual DELETE /employee/ endpoint")
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_employee = database.query(Employee).filter(Employee.id == item_id).first()
        if db_employee:
            database.delete(db_employee)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Employee entities"
    }

@router.put("/employee/{employee_id}/", response_model=None, tags=["Employee"])
async def update_employee(employee_id: int, employee_data: EmployeeCreate, database: Session = Depends(get_db)) -> Employee:
    db_employee = database.query(Employee).filter(Employee.id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    setattr(db_employee, 'email', employee_data.email)
    setattr(db_employee, 'hiredDate', employee_data.hiredDate)
    setattr(db_employee, 'name', employee_data.name)
    setattr(db_employee, 'position', employee_data.position)
    if employee_data.manager is not None:
        db_manager = database.query(Manager).filter(Manager.id == employee_data.manager).first()
        if not db_manager:
            raise HTTPException(status_code=400, detail="Manager not found")
        setattr(db_employee, 'manager_id', employee_data.manager)
    else:
        setattr(db_employee, 'manager_id', None)
    if employee_data.timeOffRequests is not None:
        requested_timeOffRequests = set(employee_data.timeOffRequests)
        current_timeOffRequests = {
            getattr(item, 'id')
            for item in database.query(TimeOffRequest).filter(TimeOffRequest.requester_id == db_employee.id).all()
        }
        timeOffRequests_to_detach = current_timeOffRequests - requested_timeOffRequests
        if timeOffRequests_to_detach:
            raise HTTPException(status_code=409, detail="TimeOffRequest " + ", ".join(str(item) for item in sorted(timeOffRequests_to_detach)) + " requires a requester: reassign it instead of removing it")
        timeOffRequests_to_attach = requested_timeOffRequests - current_timeOffRequests
        for timeoffrequest_id in timeOffRequests_to_attach:
            db_timeoffrequest = database.query(TimeOffRequest).filter(TimeOffRequest.id == timeoffrequest_id).first()
            if not db_timeoffrequest:
                raise HTTPException(status_code=400, detail="TimeOffRequest with id " + str(timeoffrequest_id) + " not found")
        if timeOffRequests_to_attach:
            database.query(TimeOffRequest).filter(TimeOffRequest.id.in_(timeOffRequests_to_attach)).update(
                {TimeOffRequest.requester_id: db_employee.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_employee)

    timeOffRequests_ids = database.query(TimeOffRequest.id).filter(TimeOffRequest.requester_id == db_employee.id).all()
    response_data = {
        "employee": db_employee,
        "timeOffRequests_ids": [x[0] for x in timeOffRequests_ids]    }
    return response_data


@router.delete("/employee/{employee_id}/", response_model=None, tags=["Employee"])
async def delete_employee(employee_id: int, database: Session = Depends(get_db)):
    db_employee = database.query(Employee).filter(Employee.id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    related_timeOffRequests = db_employee.timeOffRequests
    for related in (list(related_timeOffRequests) if isinstance(related_timeOffRequests, list) else [item for item in [related_timeOffRequests] if item is not None]):
        remaining = 0
        if remaining < 1:
            raise HTTPException(status_code=409, detail="Cannot delete Employee " + str(employee_id) + ": TimeOffRequest " + str(getattr(related, 'id')) + " requires at least 1 requester")
    # Snapshot the columns before deleting: cascading the association-class
    # links loads relationship collections whose back-references would make
    # the JSON encoder recurse endlessly on the live object.
    deleted_employee = {
        attr.key: getattr(db_employee, attr.key)
        for attr in db_employee.__mapper__.column_attrs
    }
    database.delete(db_employee)
    database.commit()
    return deleted_employee


@router.get("/employee/{employee_id}/timeOffRequests/", response_model=None, tags=["Employee Relationships"])
async def get_timeOffRequests_of_employee(employee_id: int, database: Session = Depends(get_db)):
    """Get all TimeOffRequest entities related to this Employee through timeOffRequests"""
    db_employee = database.query(Employee).filter(Employee.id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    timeOffRequests_list = database.query(TimeOffRequest).filter(TimeOffRequest.requester_id == employee_id).all()

    return {
        "employee_id": employee_id,
        "timeOffRequests_count": len(timeOffRequests_list),
        "timeOffRequests": timeOffRequests_list
    }


