from fastapi import FastAPI, Query, HTTPException
from starlette.middleware.cors import CORSMiddleware

from constants import Constants
from model.database import Database
from pointClass.PointClass import Point
from services.pointService import PointService
from services.pairPointService import pairPointService

from typing import Dict, List
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
pairPointService = pairPointService(host=Constants.HOST, user=Constants.USER, port=Constants.PORT,
                                    password=Constants.PASSWORD,
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
    print("hi")
    first_pair_name = (next(iter(items.points.keys()), None)).upper()
    if first_pair_name:
        result = pairPointService.save_pair_point(first_pair_name)
        if result != "Pair point inserted successfully!":
            return {"error": f"Error while saving pair point {first_pair_name}: {result}"}
            # Iterate over remaining keys and save them with the first pairName
        for pair_name1, point_data in items.points.items():
            pair_name=pair_name1.upper()
            if pair_name != first_pair_name:
                result_pair_values = pairPointService.save_pair_values(first_pair_name, pair_name, point_data)
                # if result_pair_values != "Points inserted successfully!":
                #     return {"error": f"Error while saving points for pair point values {pair_name}: {result_pair_values}"}

    else:
        raise HTTPException(status_code=404, detail="No points found")

    return {"message": "Pair points and their values saved successfully!"}
