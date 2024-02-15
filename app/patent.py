from typing import Dict
import statistics
from pydantic import BaseModel

from app.helpers.constants import Constants
from app.helpers.formulas import calculate_decimal_degree
from app.helpers.helpers import convertpatent_dic
from app.services.pointService import PointService

point_service = PointService(host=Constants.HOST, user=Constants.USER, port=Constants.PORT, password=Constants.PASSWORD,
                             database=Constants.DATABASE)
class LevellingData(BaseModel):
    H_levelling_m: float

def read_patent():
    data = convertpatent_dic(point_service.get_all_points())
    print("Patenttttttt")
    print(data)
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



def get_Geoid_Undulation_NLevelling(levelling : Dict[str, LevellingData]):
    Geoid_Undulation_NLevelling = {}
    patent = read_patent()
    for key in levelling:
        Geoid_Undulation_NLevelling[key] = {'Geoid Undulation (NLevelling)': patent[key]['Geodetic Height'] -
                                                                             levelling[key].H_levelling_m}
    return Geoid_Undulation_NLevelling

def get_Geoid_Undulation_NEGM2008(levelling: Dict[str, LevellingData]):
    Geoid_Undulation_NEGM2008 = {}
    patent = read_patent()
    for key in patent:
        Geoid_Undulation_NEGM2008[key] = {
            'Geoid Undulation (NEGM2008)': (patent[key]['Geodetic Height'] - patent[key]['H'])}

    return Geoid_Undulation_NEGM2008



def get_mean_deviation(levelling):
    mean_deviation = {}
    delta_N = {}
    deviation = []
    summation = 0
    Geoid_Undulation_NLevelling = get_Geoid_Undulation_NLevelling(levelling)
    Geoid_Undulation_NEGM2008 = get_Geoid_Undulation_NEGM2008(levelling)
    for key in levelling:
        delta_N[key] = Geoid_Undulation_NLevelling[key]['Geoid Undulation (NLevelling)'] - \
                       Geoid_Undulation_NEGM2008[key]['Geoid Undulation (NEGM2008)']
        summation = summation + delta_N[key]
    for key in delta_N:
        v = delta_N[key] - summation / len(delta_N)
        mean_deviation[key] = {'ΔN': delta_N[key],
                               'V': v,
                                   'V^2': v * v
                               }
    for key in mean_deviation:
        deviation.append(mean_deviation[key]['V^2'])
    mean_deviation['Mean'] = summation / len(mean_deviation)
    mean_deviation['STD DEV'] = statistics.stdev(deviation)
    return mean_deviation
