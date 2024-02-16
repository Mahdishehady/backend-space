from fastapi import FastAPI, Query, HTTPException
from starlette.middleware.cors import CORSMiddleware

from model.database import Database
from services.pairPointService import pairPointService
from Аномалиявысоты import calc_add_more
from patent import *


class LevellingData(BaseModel):
    H_levelling_m: float


class CalcDataTableParams(BaseModel):
    levelling: Dict[str, LevellingData]
    startPoint: str
    endPoint: str


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
    return {"Welcome To Аномалия высоты API's"}


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
    point = {
        "Name": Name.upper(),
        "latdegree": latdegree,
        "latminute": latminute,
        "latsecond": latsecond,
        "longdegree": longdegree,
        "longminute": longminute,
        "longsecond": longsecond,
        "geodeticheight": geodeticheight,
        "h": h
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
            pair_name = pair_name1.upper()
            if pair_name != first_pair_name:
                result_pair_values = pairPointService.save_pair_values(first_pair_name, pair_name, point_data)
    else:
        raise HTTPException(status_code=404, detail="No points found")

    return {"message": "Pair points and their values saved successfully!"}


class PairPointsResponse(BaseModel):
    points: dict


# API endpoint to get data about a pair name
@app.post("/api/get-data-table")
def get_pair_points(DataTableParams: CalcDataTableParams):
    datatable = calc_add_more(DataTableParams.levelling, DataTableParams.startPoint, DataTableParams.endPoint)
    print("final table")
    print( datatable)
    return {"data": datatable}


@app.post("/api/getNLevelling")
def get_NLevelling(levelling: Dict[str, LevellingData]):
    getNLevelling= get_Geoid_Undulation_NLevelling(levelling)
    return getNLevelling
@app.post("/api/getNEGM2008")
def get_NEGM2008(levelling: Dict[str, LevellingData]):
    getNEGM2008= get_Geoid_Undulation_NEGM2008(levelling)
    return getNEGM2008

@app.post("/api/getmeandeviation")
def getMeanDeviation(levelling: Dict[str, LevellingData]):
    getmeandeviationdata= get_mean_deviation(levelling)
    return getmeandeviationdata
