from fastapi import FastAPI, Query
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()
# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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
    return {
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
