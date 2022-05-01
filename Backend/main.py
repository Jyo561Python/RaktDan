from fastapi import FastAPI, Body, status, HTTPException
from func import functions
from func.auth.model import UserSchema
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello"}

@app.get("/user/check")
async def check(email: str):
    return functions.user.check(email)

@app.post("/user/signup")
async def user_sign(user: UserSchema = Body(default = None)):
    stat = functions.user.signup(user.fullname, user.email, user.gender, user.dob, user.blood_group, user.aadhar, user.userid)
    if stat == 201:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Registered"})
    elif stat == 400:
        return JSONResponse(status_code=400, detail="Already Exists")

@app.get("/user/signin")
async def user_signin(userid: str):
    return functions.user.signin(userid)