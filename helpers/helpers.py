


def get_sum_BS(data):
    sum_bs = 0
    for key, value in data.items():
        sum_bs += value['BS']
    return sum_bs


def get_sum_FS(data):
    sum_fs = 0
    for key, value in data.items():
        sum_fs += value['FS']
    return sum_fs


def get_BS_temp_list(data):
    return [value['TBS°'] for key, value in data.items()]


def get_FS_temp_list(data):
    return [value['TFS°'] for key, value in data.items()]



def format_decimal(value):
    return round(value, 4)

def convertPairPoints_dict(data):
    result = {}
    for row in data:
        point_name = row[0]
        point_data = {
            'BS': float(row[1]),
            'HDBS': float(row[2]),
            'TBS°': float(row[3]),
            'FS': float(row[4]),
            'HDFS': float(row[5]),
            'TFS°': float(row[6])
        }
        result[point_name] = point_data
    return result

def convertpatent_dic(data):
    result = {}
    for item in data:
        name = item[0]
        latitude_degree = item[1]
        latitude_minute = item[2]
        latitude_second = item[3]
        longitude_degree = item[4]
        longitude_minute = item[5]
        longitude_second = item[6]
        geodetic_height = item[7]
        h = item[8]

        result[name] = {
            'Latitude Degree': latitude_degree,
            'Latitude Minute': latitude_minute,
            'Latitude Second': latitude_second,
            'Longitude Degree': longitude_degree,
            'Longitude Minute': longitude_minute,
            'Longitude Second': longitude_second,
            'Geodetic Height': geodetic_height,
            'H': h
        }

    return result
