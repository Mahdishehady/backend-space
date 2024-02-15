from app.helpers.constants import Constants
from app.services.pointService import PointService
from app.services.pairPointService import pairPointService
from app.helpers.formulas import *
from app.helpers.helpers import *

pairPointService = pairPointService(host=Constants.HOST, user=Constants.USER, port=Constants.PORT,
                                    password=Constants.PASSWORD,
                                    database=Constants.DATABASE)
point_service = PointService(host=Constants.HOST, user=Constants.USER, port=Constants.PORT, password=Constants.PASSWORD,
                             database=Constants.DATABASE)


def enter_data(pairname: str):
    points = convertPairPoints_dict(pairPointService.get_points_by_pairname(pairname))
    print(points)
    return points

def elevation(data):
    curvature_dict = {}
    rod_temp_corr_dict = {}
    misclosure_dict = {}
    elevation_difference = 100
    for point, value in data.items():
        bs_curvature = get_curvature(value['BS'], value['HDBS'])
        fs_curvature = get_curvature(value['FS'], value['HDFS'])
        bs_collimation = get_collimation(bs_curvature, value['HDBS'])
        fs_collimation = get_collimation(fs_curvature, value['HDFS'])
        elevation_difference = get_elevation_difference(elevation_difference, bs_collimation, fs_collimation)
        curvature_dict[point] = {'Curvature BS': round(bs_curvature, 9),
                                 'Curvature FS': round(fs_curvature, 9),
                                 'Collimation BS': round(bs_collimation, 9),
                                 'Collimation FS': round(fs_collimation, 9),
                                 'Elevation Difference': round(elevation_difference, 8)}

    print('-----------------------------------------------------------------------------------------------------')
    mean_temp = get_mean_temp(get_BS_temp_list(data), get_FS_temp_list(data))
    keys_list = list(curvature_dict.keys())  # Convert the keys to a list
    main_elev_diff = 100 - curvature_dict[keys_list[int(len(curvature_dict) / 2) - 1]]['Elevation Difference']
    temp_error = get_temp_error(mean_temp, main_elev_diff)
    adj_elev_diff = get_temp_adj_diff_in_elevation(temp_error, main_elev_diff)
    rod_temp_corr_dict['Rod Temp Corr Baseline'] = {'Mean Temp': round(mean_temp, 7),
                                                    'Stand Temp': STANDARD_TEMP,
                                                    'Diff in Elev': round(main_elev_diff, 8),
                                                    'Thermal Expansion coefficient': THERMAL_EXPANSION_COEFFICIENT,
                                                    'Temp-Error': temp_error,
                                                    'Adj Temp Diff in Elev': round(adj_elev_diff, 8)}

    print('-----------------------------------------------------------------------------------------------------')
    misclosure_error = get_misclosure_error(get_sum_BS(data), get_sum_FS(data))
    corrected_adj_diff_in_elev = get_misclosure_adj_diff_in_elevation(adj_elev_diff, misclosure_error)
    misclosure_dict['Misclosure Baseline'] = {'Adj Temp Diff in Elev': round(adj_elev_diff, 8),
                                              'Error': misclosure_error,
                                              'Adj Diff in Elev': round(corrected_adj_diff_in_elev, 8)}

    print('-----------------------------------------------------------------------------------------------------')
    return misclosure_dict['Misclosure Baseline']['Adj Diff in Elev'], rod_temp_corr_dict, misclosure_dict