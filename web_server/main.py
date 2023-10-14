import secrets

from fastapi import FastAPI, Response, Request, HTTPException, Depends
from pydantic import BaseModel

app = FastAPI()

SESSION_DB = ['f16566cea7c61ab0c953ce494684c016']


def get_session_id(request: Request):
    session_id = request.cookies.get("Authorization")
    print(f"request request request Authorization !!!!!!!!!!: {session_id}")
    if session_id is None or session_id not in SESSION_DB:
        print("Create ano ther new sesisinoonnnn")
        session_id = secrets.token_hex(16)
        SESSION_DB.append(session_id)
    return session_id


def pass_to_prompt(long_input, session_id):
    # print(f"pass_to_promptpass_to_promptpass_to_promptpass_to_promptpass_to_prompt: long_input={long_input}, session_id={session_id}")
    return f"answer from long_input={long_input}, session_id={session_id}"


class RequestBody(BaseModel):
    session_id: str
    user_input: str


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/question")
async def ask_question(request_body: RequestBody, session_id: str = Depends(get_session_id)):
    print(f"ask_question: {session_id}")
    long_input = request_body.user_input
    answer = pass_to_prompt(long_input, session_id)
    return {"answer": answer}

@app.post("/new_chat")
async def new_chat(request: Request, response: Response):
    old_session_id = request.cookies.get('Authorization')
    if old_session_id and old_session_id in SESSION_DB:
        SESSION_DB.remove(old_session_id)
    session_id = secrets.token_hex(16)
    SESSION_DB.append(session_id)
    response.set_cookie(key="Authorization", value=session_id)
    return {"session_id": session_id}


# @app.get("/testsession")
# def get_auth_user(request: Request):
#     """verify that user has a valid session"""
#     session_id = request.cookies.get("Authorization")
#     if not session_id:
#         raise HTTPException(status_code=401)
#     if session_id not in SESSION_DB:
#         raise HTTPException(status_code=403)
#     return True


# from fastapi import Request, Depends, HTTPException, Response
# from fastapi.responses import RedirectResponse

# # This must be randomly generated
# RANDON_SESSION_ID = "iskksioskassyidd"

# # This must be a lookup on user database
# USER_CORRECT = ("admin", "admin")

# # This must be Redis, Memcached, SQLite, KV, etc...
# SESSION_DB = {}


# @app.post("/login")
# async def session_login(username: str, password: str):
#     """/login?username=ssss&password=1234234234"""
#     allow = (username, password) == USER_CORRECT
#     if allow is False:
#         raise HTTPException(status_code=401)
#     response = RedirectResponse("/", status_code=302)
#     response.set_cookie(key="Authorization", value=RANDON_SESSION_ID)
#     SESSION_DB[RANDON_SESSION_ID] = username
#     return response


# @app.post("/logout")
# async def session_logout(response: Response):
#     response.delete_cookie(key="Authorization")
#     SESSION_DB.pop(RANDON_SESSION_ID, None)
#     return {"status": "logged out"}


# def get_auth_user(request: Request):
#     """verify that user has a valid session"""
#     session_id = request.cookies.get("Authorization")
#     if not session_id:
#         raise HTTPException(status_code=401)
#     if session_id not in SESSION_DB:
#         raise HTTPException(status_code=403)
#     return True


# @app.get("/", dependencies=[Depends(get_auth_user)])
# async def secret():
#     return {"secret": "info"}