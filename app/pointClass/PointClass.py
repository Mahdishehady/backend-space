class Point:
    def __init__(self, Name: str, latdegree: float, latminute: float, latsecond: float,
                 longdegree: float, longminute: float, longsecond: float,
                 geodeticheight: float, h: float):
        self.Name = Name
        self.latdegree = latdegree
        self.latminute = latminute
        self.latsecond = latsecond
        self.longdegree = longdegree
        self.longminute = longminute
        self.longsecond = longsecond
        self.geodeticheight = geodeticheight
        self.h = h