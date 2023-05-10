from fastapi import FastAPI, Request, status, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from Database import models, database as db
from Routes import authorize, admin, profile, tournament
from Backend import Schema, Authenticate as Auth
from fastapi.middleware.cors import CORSMiddleware


models.db.Base.metadata.create_all(db.engine)
template = Jinja2Templates(directory="Views")
app = FastAPI(
    title="Euphoria Sports",
    description="18CSL58 DBMS Laboratory Mini Project on Sports Management System",
    version="2.1.0",
    contact={
        "Developer 1": {
            "Name" : "Anurag Bhatt Master",
            "USN"  : "1HK20CS028",
            "Mail" : "1hk20cs028@hkbk.edu.in",
            "Role" : "Backend Engineer"
        },
        "Developer 2": {
            "Name" : "Catherine Chandni",
            "USN"  : "1HK20CS037",
            "Mail" : "1hk20cs037@hkbk.edu.in",
            "Role" : "Frontend Designer"
        },
        "Developer 3": {
            "Name" : "Aniket Kumar Pandey",
            "USN"  : "1HK20CS026",
            "Mail" : "1hk20cs026@hkbk.edu.in"
        }
    }
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(authorize.router)
app.include_router(admin.router)
app.include_router(profile.router)
app.include_router(tournament.router)

@app.get('/home', tags=['Home'], status_code=status.HTTP_200_OK)
def redirect_to_homepage(request:Request):
    return RedirectResponse("/", status_code=status.HTTP_200_OK)

@app.get('/', tags=['Home'], status_code=status.HTTP_200_OK)
def homepage(request:Request):
    return template.TemplateResponse("homepage.html", {"request":request})

@app.get('/about', tags=['Home'], status_code=status.HTTP_200_OK)
def homepage(request:Request):
    return template.TemplateResponse("about.html", {"request":request})
