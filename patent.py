from helpers.constants import Constants
from helpers.formulas import calculate_decimal_degree
from helpers.helpers import convertpatent_dic
from services.pointService import PointService

point_service = PointService(host=Constants.HOST, user=Constants.USER, port=Constants.PORT, password=Constants.PASSWORD,
                             database=Constants.DATABASE)


def read_patent():
    data = convertpatent_dic(point_service.get_all_points())
    return data



def get_decimal_degrees():
    decimal_degrees = {}
    patent = read_patent()
    for key in patent:
        lat_degree = patent[key]['Latitude Degree']
        lat_minute = patent[key]['Latitude Minute']
        lat_second = patent[key]['Latitude Second']
        long_degree = patent[key]['Longitude Degree']
        long_minute = patent[key]['Longitude Minute']
        long_second = patent[key]['Longitude Second']
        decimal_degrees[key] = {
            'Latitude Decimal Degrees': calculate_decimal_degree(lat_degree, lat_minute, lat_second),
            'Longitude Decimal Degrees': calculate_decimal_degree(long_degree, long_minute, long_second),
            'Geodetic Height (h)': patent[key]['Geodetic Height']}
    print(decimal_degrees)
    return decimal_degrees