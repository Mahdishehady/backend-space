from fastapi import FastAPI, Query
from starlette.middleware.cors import CORSMiddleware

from constants import Constants
from model.database import Database
from pointClass.PointClass import Point
from services.pointService import PointService

app = FastAPI()
# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
db = Database(Constants.HOST, Constants.USER, Constants.PORT, Constants.PASSWORD, Constants.DATABASE)
point_service = PointService(host=Constants.HOST, user=Constants.USER, port=Constants.PORT, password=Constants.PASSWORD,
                             database=Constants.DATABASE)


@app.on_event("startup")
async def startup_event():
    db.connect()
    print("connected")


@app.on_event("shutdown")
async def shutdown_event():
    db.disconnect()
@app.get("/")
def hello():
    return {"Welcomee"}

@app.get("/api/save-point")
async def save_point(
        Name: str = Query(...),
        latdegree: float = Query(...),
        latminute: float = Query(...),
        latsecond: float = Query(...),
        longdegree: float = Query(...),
        longminute: float = Query(...),
        longsecond: float = Query(...),
        geodeticheight: float = Query(...),
        h: float = Query(...)
):
    point: any = {
        "Name": Name,
        "latdegree": latdegree,
        "latminute": latminute,
        "latsecond": latsecond,
        "longdegree": longdegree,
        "longminute": longminute,
        "longsecond": longsecond,
        "geodeticheight": geodeticheight,
        "h": h
    }
    object =point_service.save_point(point)
    return {
        object
    }


@app.get("/fetch_data")
def fetch_data():
    try:
        query = f"SELECT * FROM {Constants.TABLE}"
        data = db.execute_query(query)
        return data
    except Exception as e:
        return {"error": str(e)}


@app.post("/insert_data")
def insert_data(data: dict):
    try:
        query = f"INSERT INTO {Constants.TABLE} (column1, column2, ...) VALUES (%s, %s, ...)"
        db.execute_insert(query, (data["value1"], data["value2"], ...))
        return {"message": "Data inserted successfully"}
    except Exception as e:
        return {"error": str(e)}
