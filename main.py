from fastapi import FastAPI
from tasks import models, tasks

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/")
async def accept_data(data: models.Person):
    response = await tasks.handle_form_submission(data)
    print(response)
    return response


