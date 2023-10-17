from fastapi import FastAPI

from sandfly.routes import auth, contacts, users

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(contacts.router)


@app.get('/')
def read_root():
    return {'message': 'Welcome to the SandFly API!'}
