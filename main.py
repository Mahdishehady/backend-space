from fastapi import FastAPI, Query ,HTTPException
from starlette.middleware.cors import CORSMiddleware

from constants import Constants
from model.database import Database
from pointClass.PointClass import Point
from services.pointService import PointService
from typing import Dict , List
from pydantic import BaseModel


class DataPoint(BaseModel):
    bs: str
    hdbs: str
    tbs: str
    fs: str
    hdfs: str
    tfs: str


class DataRequest(BaseModel):
    points: Dict[str, DataPoint]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with your frontend domain
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
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
        h: float = Query(...),
        bs: float = Query(...),
        hdbs: float = Query(...),
        tbs: float = Query(...),
        fs: float = Query(...),
        hdfs: float = Query(...),
        tfs: float = Query(...),
):
    point = {
        "Name": Name.upper(),
        "latdegree": latdegree,
        "latminute": latminute,
        "latsecond": latsecond,
        "longdegree": longdegree,
        "longminute": longminute,
        "longsecond": longsecond,
        "geodeticheight": geodeticheight,
        "h": h,
        "bs": bs,
        "hdbs": hdbs,
        "tbs": tbs,
        "fs": fs,
        "hdfs": hdfs,
        "tfs": tfs
    }
    result = point_service.save_point(point)
    if "already exists" in result:
        raise HTTPException(status_code=409, detail=result)  # Conflict
    else:
        return {"message": result}

@app.post("/api/savepairpoint")
def save_pair_point(items: DataRequest):
    return {"message": "Data received successfully"}





















# @app.get("/fetch_data")
# def fetch_data():
#     try:
#         query = f"SELECT * FROM {Constants.TABLE}"
#         data = db.execute_query(query)
#         return data
#     except Exception as e:
#         return {"error": str(e)}
#
#
# @app.post("/insert_data")
# def insert_data(data: dict):
#     try:
#         query = f"INSERT INTO {Constants.TABLE} (column1, column2, ...) VALUES (%s, %s, ...)"
#         db.execute_insert(query, (data["value1"], data["value2"], ...))
#         return {"message": "Data inserted successfully"}
#     except Exception as e:
#         return {"error": str(e)}
