from email import message
from urllib import response
from fastapi import FastAPI, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import null
from database import Base, engine, User
from pydantic import BaseModel
from sqlalchemy.orm import Session

# Create Base Model Req


class RegisterRequest(BaseModel):
    email: str
    fullname: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class UserRequest(BaseModel):
    email: str
    fullname: str
    password: str


# Create the database
Base.metadata.create_all(engine)

# Customize the response


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


# Initialize app
app = FastAPI()


@app.post("/register", status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest):

    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # create an instance of the database model
    user = User(email=data.email, password=data.password, fullname=data.email)

    # add it to the session and commit it
    session.add(user)
    session.commit()

    # close the session
    session.close()

    if not user:
        return JSONResponse(
            status_code=500,
            content={
                "status": 500,
                "success": False,
                "message": f"Failed fo Register"
            }
        )
    else:
        return JSONResponse(
            status_code=201,
            content={
                "status": 201,
                "success": True,
                "message": f"Successfully created"
            }
        )


@app.post("/login")
def login(data: LoginRequest):

    session = Session(bind=engine, expire_on_commit=False)

    result = session.query(User).where(
        User.email == data.email, User.password == data.password).first()

    session.close()

    if not result:
        return JSONResponse(
            status_code=400,
            content={
                "status": 400,
                "success": False,
                "message": f"User Not Found",
                "result": {}
            }
        )
    else:
        return JSONResponse(
            status_code=200,
            content={
                "status": 200,
                "success": True,
                "message": f"User Found",
                "result": {
                    "token": "random token",
                    "userId": f"{result.id}",
                    "email": result.email,
                    "fullname": result.fullname
                }
            }
        )


@app.get("/user/{id}")
def get_by_id(id: int):

    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the todo item with the given id
    result = session.query(User).get(id)

    # close the session
    session.close()

    if not result:
        return JSONResponse(
            status_code=400,
            content={
                "status": 400,
                "success": False,
                "message": f"User Not Found",
                "result": {}
            }
        )
    else:
        return {
            "status": 200,
            "success": True,
            "message": f"User Found",
            "result": {
                result
            }
        }


@app.get('/users')
def get_all():
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    users = session.query(User).all()

    session.close()

    if not users:
        return JSONResponse(
            status_code=200,
            content={
                "status": 200,
                "success": False,
                "message": f"Failed",
                "result": {}
            }
        )
    else:
        return {
            "status": 200,
            "success": True,
            "message": f"Successfully",
            "result":  users
        }


@app.put('/user/{id}')
def user_update(id: int, data: UserRequest):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    user = session.query(User).get(id)

    if user:
        user = data
        session.commit()

    session.close()

    if not user:
        return JSONResponse(
            status_code=400,
            content={
                "status": 400,
                "success": False,
                "message": f"Update Failed",
                "result": {}
            }
        )
    else:
        return {
            "status": 200,
            "success": True,
            "message": f"Update was Successfully",
            "result":  user
        }


@app.delete('/user/{id}')
def user_delete(id: int):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    user = session.query(User).get(id)

    if user:
        session.delete(user)
        session.commit()
        session.close()
    else:
        return JSONResponse(
            status_code=404,
            content={
                "status": 404,
                "success": True,
                "message": f"User id {id} not found"
            }
        )

    return JSONResponse(
        status_code=200,
        content={
            "status": 200,
            "success": True,
            "message": f"Successfully delete user"
        }
    )
