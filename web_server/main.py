import secrets

from fastapi import FastAPI, Response, Request, Depends
from pydantic import BaseModel

app = FastAPI()

SESSION_DB = []


def get_session_id(request: Request, response: Response):
    session_id = request.cookies.get("Authorization")
    # print(f"request request request Authorization !!!!!!!!!!: {session_id}")
    if session_id is None or session_id not in SESSION_DB:
        # print("Create ano ther new sesisinoonnnn")
        session_id = secrets.token_hex(16)
        SESSION_DB.append(session_id)
        response.set_cookie(key="Authorization", value=session_id)
    return session_id


def pass_to_prompt(long_input, session_id):
    # print(f"pass_to_promptpass_to_promptpass_to_promptpass_to_promptpass_to_prompt: long_input={long_input}, session_id={session_id}")
    return f"answer from long_input={long_input}, session_id={session_id}"


class RequestBody(BaseModel):
    user_input: str


@app.post("/ask_question")
async def ask_question(
    request_body: RequestBody, session_id: str = Depends(get_session_id)
):
    # print(f"ask_question: {session_id}")
    long_input = request_body.user_input
    answer = pass_to_prompt(long_input, session_id)
    return {"answer": answer}


@app.post("/new_chat")
async def new_chat(request: Request, response: Response):
    old_session_id = request.cookies.get("Authorization")
    if old_session_id and old_session_id in SESSION_DB:
        SESSION_DB.remove(old_session_id)
    session_id = secrets.token_hex(16)
    SESSION_DB.append(session_id)
    response.set_cookie(key="Authorization", value=session_id)
    return {"session_id": session_id}
