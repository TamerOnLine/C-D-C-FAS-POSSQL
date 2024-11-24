import os
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from pydantic import BaseModel

# Initialize FastAPI
app = FastAPI()

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise Exception("DATABASE_URL is not set in .env")

# Database setup
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Define data model
class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)


# Create database tables
Base.metadata.create_all(bind=engine)


# Dependency: Database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Define validation model
class TaskCreate(BaseModel):
    name: str


# CRUD endpoints
@app.post("/tasks/")
def create_task(task: TaskCreate, db: sessionmaker = Depends(get_db)):
    new_task = Task(name=task.name)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@app.get("/tasks/")
def get_tasks(db: sessionmaker = Depends(get_db)):
    return db.query(Task).all()


@app.get("/tasks/{task_id}")
def get_task(task_id: int, db: sessionmaker = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskCreate, db: sessionmaker = Depends(get_db)):
    existing_task = db.query(Task).filter(Task.id == task_id).first()
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")
    existing_task.name = task.name
    db.commit()
    db.refresh(existing_task)
    return existing_task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: sessionmaker = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"detail": "Task deleted"}
