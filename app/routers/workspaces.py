from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth import decode_token
from app.database import get_db
from app.models import UsersTable, WorkspacesTable
from app.schemas import WorkspaceCreate, WorkspaceResponse, WorkspacesListResponse

router = APIRouter(prefix="/api/v1.0", tags=["Workspaces"])

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
#       CRUD DE WORKSPACES (PROTEGIDO)
# ==========================================

@router.post("/workspaces", status_code=201, response_model=WorkspaceResponse)
def create_workspace(workspace_data: WorkspaceCreate, db: Session = Depends(get_db), current_user: UsersTable = Depends(get_current_user)): #noqa: B008
    new_workspace = WorkspacesTable(
        name=workspace_data.name,
        description=workspace_data.description,
        owner_id=current_user.id
    )
    db.add(new_workspace)
    db.commit()
    db.refresh(new_workspace)
    return {
        "id": new_workspace.id,
        "name": new_workspace.name,
        "description": new_workspace.description,
        "owner_id": new_workspace.owner_id
    }

@router.get("/workspaces", status_code=200, response_model=WorkspacesListResponse)
def list_workspaces(db: Session = Depends(get_db), current_user: UsersTable = Depends(get_current_user)): #noqa: B008
    workspaces = db.query(WorkspacesTable).filter(WorkspacesTable.owner_id == current_user.id).all()

    return { "workspaces": workspaces }

@router.get("/workspaces/{workspace_id}", status_code=200, response_model=WorkspaceResponse)
def read_task(workspace_id: int, db: Session = Depends(get_db), current_user: UsersTable = Depends(get_current_user)): #noqa: B008
    workspace = db.query(WorkspacesTable).filter(WorkspacesTable.id == workspace_id, WorkspacesTable.owner_id == current_user.id).first()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found or unauthorized")
    return {"id": workspace.id, "name": workspace.name, "description": workspace.description, "owner_id": workspace.owner_id}

@router.put("/workspaces/{workspace_id}", status_code=200, response_model=WorkspaceResponse)
def update_task(workspace_id: int, workspace_data: WorkspaceCreate, db: Session = Depends(get_db), current_user: UsersTable = Depends(get_current_user)): #noqa: B008
    workspace = db.query(WorkspacesTable).filter(WorkspacesTable.id == workspace_id, WorkspacesTable.owner_id == current_user.id).first()
    if not workspace:
        raise HTTPException(status_code=404, detail="Task not found or unauthorized")
    
    workspace.name = workspace_data.name
    workspace.description = workspace_data.description
    workspace.owner_id = current_user.id
    
    db.commit()
    db.refresh(workspace)
    return {"id": workspace.id, "name": workspace.name, "description": workspace.description, "owner_id": workspace.owner_id}

@router.delete("/workspaces/{workspace_id}", status_code=204)
def delete_task(workspace_id: int, db: Session = Depends(get_db), current_user: UsersTable = Depends(get_current_user)): #noqa: B008
    task = db.query(WorkspacesTable).filter(WorkspacesTable.id == workspace_id, WorkspacesTable.owner_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or unauthorized")
    
    db.delete(task)
    db.commit()