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


# Create the database
Base.metadata.create_all(engine)

# Customize the response


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


# Initialize app
app = FastAPI()


@app.get("/")
def root():
    return "hello world"


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

    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the user item with the given email and password
    result = session.query(User).where(
        User.email == data.email, User.password == data.password).first()

    # close the session
    session.close()

    # check if todo item with given id exists. If not, raise exception and return 404 not found response

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
