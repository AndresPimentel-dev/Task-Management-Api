from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth import decode_token
from app.database import get_db
from app.models import TasksTable, UsersTable, WorkspacesTable
from app.schemas import TaskCreate, TaskResponse, TasksListResponse

router = APIRouter(prefix="/api/v1.0", tags=["Tasks"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1.0/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)): #noqa: B008
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = decode_token(token)
    if email is None:
        raise credentials_exception
    user = db.query(UsersTable).filter(UsersTable.email == email).first()
    if user is None:
        raise credentials_exception
    return user

# ==========================================
#          CRUD DE TAREAS (PROTEGIDO)
# ==========================================

@router.post("/tasks", status_code=201, response_model=TaskResponse)
def create_task(task_data: TaskCreate, db: Session = Depends(get_db), current_user: UsersTable = Depends(get_current_user)): #noqa: B008
    workspace = db.query(WorkspacesTable).filter(WorkspacesTable.id == task_data.workspace_id).first()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace no encontrado")
    new_task = TasksTable(
        title=task_data.title,
        description=task_data.description,
        status=task_data.status or "Todo",
        workspace_id=workspace.id,         
        assignee_id=current_user.id         
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"id": new_task.id, "title": new_task.title, "description": new_task.description, "status": new_task.status, "workspace_id": new_task.workspace_id, "assignee_id": new_task.assignee_id}

@router.get("/tasks", status_code=200, response_model=TasksListResponse)
def read_tasks(db: Session = Depends(get_db), current_user: UsersTable = Depends(get_current_user)): #noqa: B008
    tasks = db.query(TasksTable).filter(TasksTable.assignee_id == current_user.id).all()

    return {"tasks": tasks}

@router.get("/tasks/{task_id}", status_code=200, response_model=TaskResponse)
def read_task(task_id: int, db: Session = Depends(get_db), current_user: UsersTable = Depends(get_current_user)): #noqa: B008
    task = db.query(TasksTable).filter(TasksTable.id == task_id, TasksTable.assignee_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or unauthorized")
    return {"id": task.id, "title": task.title, "description": task.description, "status": task.status, "workspace_id": task.workspace_id, "assignee_id": task.assignee_id}

@router.put("/tasks/{task_id}", status_code=200, response_model=TaskResponse)
def update_task(task_id: int, task_data: TaskCreate, db: Session = Depends(get_db), current_user: UsersTable = Depends(get_current_user)): #noqa: B008
    task = db.query(TasksTable).filter(TasksTable.id == task_id, TasksTable.assignee_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or unauthorized")
    task.title = task_data.title
    task.description = task_data.description
    task.status = task_data.status
    
    db.commit()
    db.refresh(task)
    return {"id": task.id, "title": task.title, "description": task.description, "status": task.status, "workspace_id": task.workspace_id, "assignee_id": task.assignee_id}

@router.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: UsersTable = Depends(get_current_user)): #noqa: B008
    task = db.query(TasksTable).filter(TasksTable.id == task_id, TasksTable.assignee_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or unauthorized")
    
    db.delete(task)
    db.commit()

