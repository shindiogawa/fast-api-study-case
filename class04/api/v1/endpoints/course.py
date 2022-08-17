from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from models.course_model import CourseModel
from core.deps import get_session

# Bypass warning SQLModel select
# Sometimes SQModel throws some warnings and this block of code will ignore these warnings
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True
Select.inherit_cahse = True
# End Bypass

router = APIRouter()

# Post Course
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=CourseModel)
async def post_course(course: CourseModel, db: AsyncSession = Depends(get_session)):
    new_course = CourseModel(title= course.title, classes=course.classes, hours= course.hours)

    db.add(new_course)
    await db.commit()

    return new_course

# Get Courses
@router.get('/', response_model=List[CourseModel])
async def get_courses(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CourseModel)
        result = await session.execute(query)
        courses: List[CourseModel] = result.scalars().all()

        return courses

# Get Course
@router.get('/{course_id}', response_model=CourseModel, status_code=status.HTTP_200_OK)
async def get_course(course_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CourseModel).filter(CourseModel.id == course_id)
        result = await session.execute(query)
        course: CourseModel = result.scalar_one_or_none()

        if course:
            return course
        else:
            raise HTTPException(detail='Course not found', status_code=status.HTTP_404_NOT_FOUND)

# PUT Course
@router.put('/{course_id}', status_code= status.HTTP_202_ACCEPTED, response_model= CourseModel)
async def put_course(course_id: int, course: CourseModel, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CourseModel).filter(CourseModel.id == course_id)
        result = await session.execute(query)
        course_update: CourseModel = result.scalar_one_or_none()

        if course_update:
            course_update.title = course.title
            course_update.classes = course.classes
            course_update.hours = course.hours
            
            await session.commit()
            return course_update
        else:
            raise HTTPException(detail='Course not found', status_code=status.HTTP_404_NOT_FOUND)

# Delete course
@router.delete('/{course_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CourseModel).filter(CourseModel.id == course_id)
        result = await session.execute(query)
        course_del: CourseModel = result.scalar_one_or_none()

        if course_del:
            await session.delete(course_del)
            
            await session.commit()
            # We need to return this due to a bug in Fast Api
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Course not found', status_code=status.HTTP_404_NOT_FOUND)


