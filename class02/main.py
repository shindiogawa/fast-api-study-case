from imp import reload
from re import L
from fastapi import FastAPI, HTTPException, status, Response, Path, Query, Header, Depends
from typing import List, Optional, Any, Dict

from time import sleep

# At this moment, this is returning wrong message, not use yet. Use Response instead
from fastapi.responses import JSONResponse
from models import Course, courses

def fake_db():
    try:
        print('Open connection with DB')
        sleep(1)
    finally:
        print('Closing connection with DB')
        sleep(1)
    

app = FastAPI(
    title='Courses API of Rodrigo',
    version='0.0.1',
    description='Study case of fastapi'
)


@app.get(
        '/courses', 
        description='Returns all the courses or an empty list',
        summary='return the courses',
        response_model=List[Course],
        response_description='Courses found with success')
async def get_courses(db: Any = Depends(fake_db)):
    return courses

# @app.get('/courses/{course_id}')
# async def get_course(course_id: int):

#     try:
#         course = courses[course_id]
#         return course
#     except KeyError:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Course not found.')

##  Path parameters
@app.get('/courses/{course_id}')
async def get_course(course_id: int =  Path(default=None, title='Course ID', description='Should be between 1 and 2', gt=0, lt=3), db: Any = Depends(fake_db)):

    try:
        course = courses[course_id]
        return course
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Course not found.')

@app.post('/courses', status_code = status.HTTP_201_CREATED,response_model = Course)
async def post_course(course: Course,db: Any = Depends(fake_db) ):
    next_id: int = len(courses) + 1    
    course.id = next_id
    courses.append(course)
    del course.id
    return course

@app.put('/courses/{course_id}')
async def put_course(course_id: int, course: Course, db: Any = Depends(fake_db)):
    if course_id in courses:
        courses[course_id] = course
        return course
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="We didn't find any course with this id")


@app.delete('/courses/{course_id}')
async def delete_course(course_id: int, db: Any = Depends(fake_db)):
    if course_id in courses:
        del courses[course_id]
        # return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="We didn't find any course with this id")

## Query Parameter + Header Parameter
@app.get('/calculator')
async def calculate(a: int = Query(default=None, gt=5), b: int = Query(default=None, gt=10), x_geek: str = Header(default = None), c: Optional[int] = None):
    sum: int = a + b
    if c:
        sum += c
    print(f'X-GEEK:', x_geek)
    return {"result": sum}

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, debug=True, reload=True)