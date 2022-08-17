from re import sub
from typing import List, Optional, Any
from urllib import response

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from models.user_model import UserModel
from schemas.user_schema import UserSchemaBase, UserSchemaArticles, UserSchemaCreate, UserSchemaUpdate
from core.deps import get_session, get_current_user
from core.security import generate_password_hash
from core.auth import authenticate, create_access_token


router  = APIRouter()

# GET User Logged
@router.get('/logged', response_model=UserSchemaBase)
def get_user_logged(logged_user: UserModel = Depends(get_current_user)):
    return logged_user

# POST / SIGNUP 
@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserSchemaBase)
async def post_user(user: UserSchemaCreate, db: AsyncSession = Depends(get_session)):
    new_user: UserModel = UserModel(name= user.name, lastname= user.lastname, email=user.email, password = generate_password_hash(user.password), is_admin = user.is_admin)

    async with db as session:
        try:
            session.add(new_user)
            await session.commit()

            return new_user
        except IntegrityError:
            raise  HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='There are already an user with this email')

# GET Users
@router.get('/', response_model=List[UserSchemaBase])
async def get_users(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel)
        result = await session.execute(query)
        users: List[UserSchemaBase] = result.scalars().unique().all()

        return users

# Get User
@router.get('/{user_id}', response_model=UserSchemaArticles, status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user: UserSchemaArticles = result.scalars().unique().one_or_none()

        if user:
            return user
        else:
            raise HTTPException(detail='User not found', status_code=status.HTTP_404_NOT_FOUND)


# PUT User
@router.put('/{user_id}', response_model=UserSchemaBase, status_code=status.HTTP_202_ACCEPTED)
async def put_user(user_id: int, user: UserSchemaUpdate, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user_up: UserSchemaBase = result.scalars().unique().one_or_none()

        if user_up:
            if user.name:
                user_up.name = user.name
            if user.lastname:
                user_up.lastname = user.lastname
            if user.email:
                user_up.email = user.email
            if user.is_admin:
                user_up.password = generate_password_hash(user.password)
            
            await session.commit()

            return user_up
        else:
            raise HTTPException(detail='User not found', status_code=status.HTTP_404_NOT_FOUND)


# Delete User
@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user_del: UserSchemaArticles = result.scalars().unique().one_or_none()

        if user_del:
            await session.delete(user_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='User not found', status_code=status.HTTP_404_NOT_FOUND)


# POST Login
@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    user = await authenticate(email = form_data.username, password= form_data.password, db=db)

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect data.')

    return JSONResponse(content={"access_token": create_access_token(subject=user.id), "token_type": "bearer"}, status_code=status.HTTP_200_OK)
