from datetime import timedelta
from typing import List, List, Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import jwt

from app.database import engine, Base, get_db
from app.models import User, Task, Workspace
from app.schemas import UserCreate, UserResponse, TaskCreate, TaskResponse, Token
from app.auth import verify_password, get_password_hash, create_access_token, SECRET_KEY, ALGORITHM

# Crear las tablas en la base de datos si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TaskForge API",
    description="Full Backend with JWT Authentication and Tasks CRUD",
    version="1.0.0"
)

# Configuración del esquema de seguridad para Swagger UI (/docs)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Dependencia para obtener el usuario actual autenticado a través del Token JWT
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
        
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user


# ==========================================
#          ENDPOINTS DE AUTENTICACIÓN
# ==========================================

@app.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # Verificar si el correo ya está registrado
    db_user = db.query(User).filter(User.email == user_data.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hashear la contraseña antes de guardar
    hashed_pwd = get_password_hash(user_data.password)
    
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_pwd
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm usa 'username' para el campo de texto, ahí pasaremos el email
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Crear el token de acceso JWT
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# ==========================================
#       CRUD DE WORKSPACES (PROTEGIDO)
# ==========================================

@app.post("/workspaces", status_code=status.HTTP_201_CREATED)
def create_workspace(name: str, description: Optional[str] = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Creamos el espacio asignándote a ti como el owner_id original
    new_workspace = Workspace(
        name=name,
        description=description,
        owner_id=current_user.id
    )
    db.add(new_workspace)
    db.commit()
    db.refresh(new_workspace)
    return {
        "id": new_workspace.id,
        "name": new_workspace.name,
        "owner_id": new_workspace.owner_id
    }

@app.get("/workspaces")
def list_workspaces(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Lista los espacios de trabajo donde eres el creador
    return db.query(Workspace).filter(Workspace.owner_id == current_user.id).all()
# ==========================================
#          CRUD DE TAREAS (PROTEGIDO)
# ==========================================

@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskCreate, workspace_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Buscamos si el workspace existe antes de meter la tarea
    workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace no encontrado")

    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        status=task_data.status or "Todo",
        workspace_id=workspace_id,          # Vincula la tarea al espacio de trabajo real
        assignee_id=current_user.id         # El creador queda asignado automáticamente
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.get("/tasks", response_model=List[TaskResponse])
def read_tasks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Corrección: Cambiar Task.owner_id por Task.assignee_id
    return db.query(Task).filter(Task.assignee_id == current_user.id).all()

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def read_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Corrección: Cambiar Task.owner_id por Task.assignee_id
    task = db.query(Task).filter(Task.id == task_id, Task.assignee_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or unauthorized")
    return task

@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_data: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Corrección: Cambiar Task.owner_id por Task.assignee_id
    task = db.query(Task).filter(Task.id == task_id, Task.assignee_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or unauthorized")
    
    task.title = task_data.title
    task.description = task_data.description
    task.status = task_data.status
    
    db.commit()
    db.refresh(task)
    return task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Corrección: Cambiar Task.owner_id por Task.assignee_id
    task = db.query(Task).filter(Task.id == task_id, Task.assignee_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or unauthorized")
    
    db.delete(task)
    db.commit()
    return None
