import os
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from sqlalchemy import create_engine, String, Integer, DateTime, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, sessionmaker
from sqlalchemy.exc import IntegrityError

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+psycopg://students:students@localhost:5432/students')
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

class Student(Base):
    __tablename__ = 'students'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    course: Mapped[str] = mapped_column(String(120), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class StudentInput(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    course: str = Field(min_length=2, max_length=120)
    year: int = Field(ge=1, le=6)

class StudentOutput(StudentInput):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title='Student Management API', version='1.0.0', lifespan=lifespan)
# React is served from the same origin through the Vite dev proxy or production Nginx proxy.

def get_db():
    with SessionLocal() as db:
        yield db

@app.get('/api/health')
def health(db: Session = Depends(get_db)):
    db.execute(select(1))
    return {'status': 'ok', 'database': 'connected'}

@app.get('/api/stats')
def stats(db: Session = Depends(get_db)):
    total = db.scalar(select(func.count()).select_from(Student)) or 0
    courses = db.scalar(select(func.count(func.distinct(Student.course)))) or 0
    return {'students': total, 'courses': courses}

@app.get('/api/students', response_model=list[StudentOutput])
def list_students(search: str = Query('', max_length=120), db: Session = Depends(get_db)):
    query = select(Student)
    if search.strip():
        term = f'%{search.strip()}%'
        query = query.where(Student.name.ilike(term) | Student.email.ilike(term) | Student.course.ilike(term))
    return db.scalars(query.order_by(Student.id.desc())).all()

@app.post('/api/students', response_model=StudentOutput, status_code=201)
def add_student(payload: StudentInput, db: Session = Depends(get_db)):
    student = Student(**payload.model_dump())
    db.add(student)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, 'This email address is already registered')
    db.refresh(student)
    return student

@app.put('/api/students/{student_id}', response_model=StudentOutput)
def update_student(student_id: int, payload: StudentInput, db: Session = Depends(get_db)):
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(404, 'Student not found')
    for key, value in payload.model_dump().items():
        setattr(student, key, value)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, 'This email address is already registered')
    db.refresh(student)
    return student

@app.delete('/api/students/{student_id}', status_code=204)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(404, 'Student not found')
    db.delete(student)
    db.commit()
