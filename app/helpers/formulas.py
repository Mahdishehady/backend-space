from app.helpers.constants import *


def get_curvature(sight, horizontal_distance):
    horizontal_distance_in_km = horizontal_distance / 1000
    curvature = sight - CURVATURE * horizontal_distance_in_km ** 2
    return curvature


def get_collimation(curvature, horizontal_distance):
    horizontal_distance_in_km = horizontal_distance / 1000
    collimation = curvature - (COLLIMATION * horizontal_distance_in_km)
    return collimation


def get_elevation_difference(previous_elevation, collimationBS, collimationFS):
    elevation_difference = previous_elevation + collimationBS - collimationFS
    return elevation_difference


def get_mean_temp(temp_BS_ist, temp_FS_list):
    total_temp = 0
    for temp in temp_BS_ist:
        total_temp = total_temp + temp
    for temp in temp_FS_list:
        total_temp = total_temp + temp
    count = len(temp_BS_ist) + len(temp_FS_list)
    average_temperature = total_temp / count
    return average_temperature


def get_diff_in_elevation(elevation_diff):
    return 100 - elevation_diff


def get_temp_error(mean_temp, diff_in_elevation):
    temp_error = (mean_temp - STANDARD_TEMP) * diff_in_elevation * THERMAL_EXPANSION_COEFFICIENT
    return temp_error


def get_temp_adj_diff_in_elevation(temp_error, diff_in_elevation):
    adj_diff_in_elev = diff_in_elevation + temp_error
    return adj_diff_in_elev


def get_misclosure_error(sum_BS, sumFS):
    return sum_BS - sumFS


def get_misclosure_adj_diff_in_elevation(temp_adj_diff_in_elevation, misclosure_error):
    return temp_adj_diff_in_elevation - misclosure_error


def get_levelling(start_point, adj_diff_in_elevation):
    return start_point - adj_diff_in_elevation


def calculate_decimal_degree(degree, minutes, seconds):
    return degree + (minutes / 60) + (seconds / 3600)
