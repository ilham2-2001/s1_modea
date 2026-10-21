from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from pydantic_classes import *
from sql_alchemy import *
from database import get_db
from bal_stdlib import *

router = APIRouter()


@router.get("/manager/", response_model=None, tags=["Manager"])
def get_all_manager(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Manager)
        query = query.options(joinedload(Manager.manager))
        manager_list = query.all()

        # Serialize with relationships included
        result = []
        for manager_item in manager_list:
            item_dict = manager_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if manager_item.manager:
                related_obj = manager_item.manager
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['manager'] = related_dict
            else:
                item_dict['manager'] = None

            # Add many-to-many and one-to-many relationship objects (full details)
            timeoffrequest_list = database.query(TimeOffRequest).filter(TimeOffRequest.approvedBy_id == manager_item.id).all()
            item_dict['approvedRequests'] = []
            for timeoffrequest_obj in timeoffrequest_list:
                timeoffrequest_dict = timeoffrequest_obj.__dict__.copy()
                timeoffrequest_dict.pop('_sa_instance_state', None)
                item_dict['approvedRequests'].append(timeoffrequest_dict)
            employee_list = database.query(Employee).filter(Employee.manager_id == manager_item.id).all()
            item_dict['teamMembers'] = []
            for employee_obj in employee_list:
                employee_dict = employee_obj.__dict__.copy()
                employee_dict.pop('_sa_instance_state', None)
                item_dict['teamMembers'].append(employee_dict)
            timeoffrequest_list = database.query(TimeOffRequest).filter(TimeOffRequest.requester_id == manager_item.id).all()
            item_dict['timeOffRequests'] = []
            for timeoffrequest_obj in timeoffrequest_list:
                timeoffrequest_dict = timeoffrequest_obj.__dict__.copy()
                timeoffrequest_dict.pop('_sa_instance_state', None)
                item_dict['timeOffRequests'].append(timeoffrequest_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Manager).all()


@router.get("/manager/count/", response_model=None, tags=["Manager"])
def get_count_manager(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Manager entities"""
    count = database.query(Manager).count()
    return {"count": count}


@router.get("/manager/paginated/", response_model=None, tags=["Manager"])
def get_paginated_manager(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Manager entities"""
    total = database.query(Manager).count()
    manager_list = database.query(Manager).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": manager_list
        }

    result = []
    for manager_item in manager_list:
        approvedRequests_ids = database.query(TimeOffRequest.id).filter(TimeOffRequest.approvedBy_id == manager_item.id).all()
        teamMembers_ids = database.query(Employee.id).filter(Employee.manager_id == manager_item.id).all()
        timeOffRequests_ids = database.query(TimeOffRequest.id).filter(TimeOffRequest.requester_id == manager_item.id).all()
        item_data = {
            "manager": manager_item,
            "approvedRequests_ids": [x[0] for x in approvedRequests_ids],            "teamMembers_ids": [x[0] for x in teamMembers_ids],            "timeOffRequests_ids": [x[0] for x in timeOffRequests_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }
@router.get("/manager/search/", response_model=None, tags=["Manager"])
def search_manager(
    email: str = None,
    id: int = None,
    name: str = None,
    position: str = None,
    department: str = None,
    database: Session = Depends(get_db)
) -> list:
    """Search Manager entities by attributes"""
    query = database.query(Manager)

    if email is not None:
        query = query.filter(Manager.email.ilike(f"%{email}%"))
    if id is not None:
        query = query.filter(Manager.id == id)
    if name is not None:
        query = query.filter(Manager.name.ilike(f"%{name}%"))
    if position is not None:
        query = query.filter(Manager.position.ilike(f"%{position}%"))
    if department is not None:
        query = query.filter(Manager.department.ilike(f"%{department}%"))

    results = query.all()
    return results


@router.get("/manager/{manager_id}/", response_model=None, tags=["Manager"])
async def get_manager(manager_id: int, database: Session = Depends(get_db)) -> Manager:
    db_manager = database.query(Manager).filter(Manager.id == manager_id).first()
    if db_manager is None:
        raise HTTPException(status_code=404, detail="Manager not found")

    approvedRequests_ids = database.query(TimeOffRequest.id).filter(TimeOffRequest.approvedBy_id == db_manager.id).all()
    teamMembers_ids = database.query(Employee.id).filter(Employee.manager_id == db_manager.id).all()
    timeOffRequests_ids = database.query(TimeOffRequest.id).filter(TimeOffRequest.requester_id == db_manager.id).all()
    response_data = {
        "manager": db_manager,
        "approvedRequests_ids": [x[0] for x in approvedRequests_ids],        "teamMembers_ids": [x[0] for x in teamMembers_ids],        "timeOffRequests_ids": [x[0] for x in timeOffRequests_ids]}
    return response_data



@router.post("/manager/", response_model=None, tags=["Manager"])
async def create_manager(manager_data: ManagerCreate, database: Session = Depends(get_db)) -> Manager:

    if manager_data.manager :
        db_manager = database.query(Manager).filter(Manager.id == manager_data.manager).first()
        if not db_manager:
            raise HTTPException(status_code=400, detail="Manager not found")

    db_manager = Manager(
        email=manager_data.email,        hiredDate=manager_data.hiredDate,        name=manager_data.name,        position=manager_data.position,        department=manager_data.department,        manager_id=manager_data.manager        )

    database.add(db_manager)
    database.flush()
    database.refresh(db_manager)

    if manager_data.approvedRequests:
        # Validate that all TimeOffRequest IDs exist
        for timeoffrequest_id in manager_data.approvedRequests:
            db_timeoffrequest = database.query(TimeOffRequest).filter(TimeOffRequest.id == timeoffrequest_id).first()
            if not db_timeoffrequest:
                raise HTTPException(status_code=400, detail=f"TimeOffRequest with id {timeoffrequest_id} not found")

        # Update the related entities with the new foreign key
        database.query(TimeOffRequest).filter(TimeOffRequest.id.in_(manager_data.approvedRequests)).update(
            {TimeOffRequest.approvedBy_id: db_manager.id}, synchronize_session=False
        )
        database.flush()
    if manager_data.teamMembers:
        # Validate that all Employee IDs exist
        for employee_id in manager_data.teamMembers:
            db_employee = database.query(Employee).filter(Employee.id == employee_id).first()
            if not db_employee:
                raise HTTPException(status_code=400, detail=f"Employee with id {employee_id} not found")

        # Update the related entities with the new foreign key
        database.query(Employee).filter(Employee.id.in_(manager_data.teamMembers)).update(
            {Employee.manager_id: db_manager.id}, synchronize_session=False
        )
        database.flush()
    if manager_data.timeOffRequests:
        # Validate that all TimeOffRequest IDs exist
        for timeoffrequest_id in manager_data.timeOffRequests:
            db_timeoffrequest = database.query(TimeOffRequest).filter(TimeOffRequest.id == timeoffrequest_id).first()
            if not db_timeoffrequest:
                raise HTTPException(status_code=400, detail=f"TimeOffRequest with id {timeoffrequest_id} not found")

        # Update the related entities with the new foreign key
        database.query(TimeOffRequest).filter(TimeOffRequest.id.in_(manager_data.timeOffRequests)).update(
            {TimeOffRequest.requester_id: db_manager.id}, synchronize_session=False
        )
        database.flush()



    approvedRequests_ids = database.query(TimeOffRequest.id).filter(TimeOffRequest.approvedBy_id == db_manager.id).all()
    teamMembers_ids = database.query(Employee.id).filter(Employee.manager_id == db_manager.id).all()
    timeOffRequests_ids = database.query(TimeOffRequest.id).filter(TimeOffRequest.requester_id == db_manager.id).all()
    response_data = {
        "manager": db_manager,
        "approvedRequests_ids": [x[0] for x in approvedRequests_ids],        "teamMembers_ids": [x[0] for x in teamMembers_ids],        "timeOffRequests_ids": [x[0] for x in timeOffRequests_ids]    }
    database.commit()
    database.refresh(db_manager)
    return response_data


@router.post("/manager/bulk/", response_model=None, tags=["Manager"])
async def bulk_create_manager(items: list[ManagerCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Manager entities at once"""
    if any(getattr(item, field, None) for item in items for field in ['approvedRequests', 'teamMembers', 'timeOffRequests']):
        raise HTTPException(status_code=422, detail="Bulk creation of Manager with relationships is not supported; use POST /manager/ to validate and persist its relationships")
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_manager = Manager(
                email=item_data.email,                hiredDate=item_data.hiredDate,                name=item_data.name,                position=item_data.position,                department=item_data.department,                manager_id=item_data.manager            )
            database.add(db_manager)
            database.flush()  # Get ID without committing
            created_items.append(db_manager.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Manager entities"
    }


@router.delete("/manager/bulk/", response_model=None, tags=["Manager"])
async def bulk_delete_manager(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Manager entities at once"""
    # Aggregate deletion must account for every related lower bound. Until it
    # shares that validation, use the guarded individual delete endpoint.
    if ids:
        raise HTTPException(status_code=409, detail="Bulk deletion of Manager can violate required relationships and is not supported; use the individual DELETE /manager/ endpoint")
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_manager = database.query(Manager).filter(Manager.id == item_id).first()
        if db_manager:
            database.delete(db_manager)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Manager entities"
    }

@router.put("/manager/{manager_id}/", response_model=None, tags=["Manager"])
async def update_manager(manager_id: int, manager_data: ManagerCreate, database: Session = Depends(get_db)) -> Manager:
    db_manager = database.query(Manager).filter(Manager.id == manager_id).first()
    if db_manager is None:
        raise HTTPException(status_code=404, detail="Manager not found")

    setattr(db_manager, 'email', manager_data.email)
    setattr(db_manager, 'hiredDate', manager_data.hiredDate)
    setattr(db_manager, 'name', manager_data.name)
    setattr(db_manager, 'position', manager_data.position)
    setattr(db_manager, 'department', manager_data.department)
    if manager_data.approvedRequests is not None:
        requested_approvedRequests = set(manager_data.approvedRequests)
        current_approvedRequests = {
            getattr(item, 'id')
            for item in database.query(TimeOffRequest).filter(TimeOffRequest.approvedBy_id == db_manager.id).all()
        }
        approvedRequests_to_detach = current_approvedRequests - requested_approvedRequests
        if approvedRequests_to_detach:
            database.query(TimeOffRequest).filter(TimeOffRequest.id.in_(approvedRequests_to_detach)).update(
                {TimeOffRequest.approvedBy_id: None}, synchronize_session=False
            )
        approvedRequests_to_attach = requested_approvedRequests - current_approvedRequests
        for timeoffrequest_id in approvedRequests_to_attach:
            db_timeoffrequest = database.query(TimeOffRequest).filter(TimeOffRequest.id == timeoffrequest_id).first()
            if not db_timeoffrequest:
                raise HTTPException(status_code=400, detail="TimeOffRequest with id " + str(timeoffrequest_id) + " not found")
        if approvedRequests_to_attach:
            database.query(TimeOffRequest).filter(TimeOffRequest.id.in_(approvedRequests_to_attach)).update(
                {TimeOffRequest.approvedBy_id: db_manager.id}, synchronize_session=False
            )
    if manager_data.teamMembers is not None:
        requested_teamMembers = set(manager_data.teamMembers)
        current_teamMembers = {
            getattr(item, 'id')
            for item in database.query(Employee).filter(Employee.manager_id == db_manager.id).all()
        }
        teamMembers_to_detach = current_teamMembers - requested_teamMembers
        if teamMembers_to_detach:
            database.query(Employee).filter(Employee.id.in_(teamMembers_to_detach)).update(
                {Employee.manager_id: None}, synchronize_session=False
            )
        teamMembers_to_attach = requested_teamMembers - current_teamMembers
        for employee_id in teamMembers_to_attach:
            db_employee = database.query(Employee).filter(Employee.id == employee_id).first()
            if not db_employee:
                raise HTTPException(status_code=400, detail="Employee with id " + str(employee_id) + " not found")
        if teamMembers_to_attach:
            database.query(Employee).filter(Employee.id.in_(teamMembers_to_attach)).update(
                {Employee.manager_id: db_manager.id}, synchronize_session=False
            )
    if manager_data.timeOffRequests is not None:
        requested_timeOffRequests = set(manager_data.timeOffRequests)
        current_timeOffRequests = {
            getattr(item, 'id')
            for item in database.query(TimeOffRequest).filter(TimeOffRequest.requester_id == db_manager.id).all()
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
                {TimeOffRequest.requester_id: db_manager.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_manager)

    approvedRequests_ids = database.query(TimeOffRequest.id).filter(TimeOffRequest.approvedBy_id == db_manager.id).all()
    teamMembers_ids = database.query(Employee.id).filter(Employee.manager_id == db_manager.id).all()
    timeOffRequests_ids = database.query(TimeOffRequest.id).filter(TimeOffRequest.requester_id == db_manager.id).all()
    response_data = {
        "manager": db_manager,
        "approvedRequests_ids": [x[0] for x in approvedRequests_ids],        "teamMembers_ids": [x[0] for x in teamMembers_ids],        "timeOffRequests_ids": [x[0] for x in timeOffRequests_ids]    }
    return response_data


@router.delete("/manager/{manager_id}/", response_model=None, tags=["Manager"])
async def delete_manager(manager_id: int, database: Session = Depends(get_db)):
    db_manager = database.query(Manager).filter(Manager.id == manager_id).first()
    if db_manager is None:
        raise HTTPException(status_code=404, detail="Manager not found")
    related_timeOffRequests = db_manager.timeOffRequests
    for related in (list(related_timeOffRequests) if isinstance(related_timeOffRequests, list) else [item for item in [related_timeOffRequests] if item is not None]):
        remaining = 0
        if remaining < 1:
            raise HTTPException(status_code=409, detail="Cannot delete Manager " + str(manager_id) + ": TimeOffRequest " + str(getattr(related, 'id')) + " requires at least 1 requester")
    # Snapshot the columns before deleting: cascading the association-class
    # links loads relationship collections whose back-references would make
    # the JSON encoder recurse endlessly on the live object.
    deleted_manager = {
        attr.key: getattr(db_manager, attr.key)
        for attr in db_manager.__mapper__.column_attrs
    }
    database.delete(db_manager)
    database.commit()
    return deleted_manager


@router.get("/manager/{manager_id}/approvedRequests/", response_model=None, tags=["Manager Relationships"])
async def get_approvedRequests_of_manager(manager_id: int, database: Session = Depends(get_db)):
    """Get all TimeOffRequest entities related to this Manager through approvedRequests"""
    db_manager = database.query(Manager).filter(Manager.id == manager_id).first()
    if db_manager is None:
        raise HTTPException(status_code=404, detail="Manager not found")

    approvedRequests_list = database.query(TimeOffRequest).filter(TimeOffRequest.approvedBy_id == manager_id).all()

    return {
        "manager_id": manager_id,
        "approvedRequests_count": len(approvedRequests_list),
        "approvedRequests": approvedRequests_list
    }

@router.get("/manager/{manager_id}/teamMembers/", response_model=None, tags=["Manager Relationships"])
async def get_teamMembers_of_manager(manager_id: int, database: Session = Depends(get_db)):
    """Get all Employee entities related to this Manager through teamMembers"""
    db_manager = database.query(Manager).filter(Manager.id == manager_id).first()
    if db_manager is None:
        raise HTTPException(status_code=404, detail="Manager not found")

    teamMembers_list = database.query(Employee).filter(Employee.manager_id == manager_id).all()

    return {
        "manager_id": manager_id,
        "teamMembers_count": len(teamMembers_list),
        "teamMembers": teamMembers_list
    }

@router.get("/manager/{manager_id}/timeOffRequests/", response_model=None, tags=["Manager Relationships"])
async def get_timeOffRequests_of_manager(manager_id: int, database: Session = Depends(get_db)):
    """Get all TimeOffRequest entities related to this Manager through timeOffRequests"""
    db_manager = database.query(Manager).filter(Manager.id == manager_id).first()
    if db_manager is None:
        raise HTTPException(status_code=404, detail="Manager not found")

    timeOffRequests_list = database.query(TimeOffRequest).filter(TimeOffRequest.requester_id == manager_id).all()

    return {
        "manager_id": manager_id,
        "timeOffRequests_count": len(timeOffRequests_list),
        "timeOffRequests": timeOffRequests_list
    }


