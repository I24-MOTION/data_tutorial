import numpy as np
import ijson
import pandas as pd
import datetime
import pytz

def convert_to_cst_unix(date_string):
    """
    Convert a date string in the format 'YYYY-MM-DD HH:MM' to a Unix timestamp in CST timezone (Nashville local time).

    :param date_string: The date string in the format of 'YYYY-MM-DD HH:MM'
    :type string
    :return: Unix timestamp in CST
    :rtype: float
    """
    # Parse the date string to a datetime object
    date_obj = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M')

    # Convert to CST timezone
    cst_timezone = pytz.timezone('America/Chicago')
    date_obj_cst = cst_timezone.localize(date_obj)

    # Convert to Unix timestamp
    unix_timestamp = int(date_obj_cst.timestamp())
    return unix_timestamp


def get_array(decimal_list):
    """
    Converts a list of decimal numbers into a NumPy array of floats.

    This function takes a list of numbers (integers or floats) and converts
    each number into a float, ultimately returning a NumPy array of these floating-point numbers.

    :param decimal_list: A list of numbers (integers or floats).
    :type decimal_list: list
    :return: A NumPy array containing the elements of decimal_list as floats.
    :rtype: numpy.ndarray
    """
    float_list = [float(d) for d in decimal_list]
    return np.array(float_list)


def matrix_to_coordinates(matrix):
    """
    Converts a 2D matrix (numpy.array) into a list of coordinates with values.

    This function iterates through each element of a 2D matrix and
    creates a list of coordinates, where each coordinate is represented
    as a list containing the row index, column index, and the value at
    that position in the matrix.

    :param matrix: A numpy.array where each sublist represents a row in the matrix.
    :type matrix: numpy.array filled with float
    :return: A list of coordinates, where each coordinate is a list of [row_index, column_index, value].
    :rtype: list of list of float

    Example:
        matrix = np.array([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ])

        coords = matrix_to_coordinates(matrix)
        print(coords)  # Output: [[0, 0, 1], [0, 1, 2], [0, 2, 3], [1, 0, 4], [1, 1, 5], [1, 2, 6], [2, 0, 7], [2, 1, 8], [2, 2, 9]]
    """
    coordinates = []
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            coordinates.append([i, j, matrix[i][j]])
    return coordinates



def get_speed_mean_field(input_filename, dx, dt, starttime, endtime, lane_number, min_milemarker = 58.7, testbed_mile = 4):
    """
    Calculate the speed mean field based on input data.

    This function calculates the speed mean field from the provided input data file and parameters.
    It reads data from the file, processes it, and returns the result as a pandas DataFrame.

    The input data file should contain JSON records from MOTION system with fields 'last_timestamp', 'first_timestamp',
    'direction', 'length', 'timestamp', 'x_position', and 'y_position'.

    The speed mean field is calculated by dividing the sum of total travel distance (TTD) and total travel time (TTT)
    for each spatial and temporal bin (Edie's box).

    :param input_filename: The path to the input data file.
    :type input_filename: str
    :param dx: The spatial resolution (the spatial size for the Edie's box).
    :type dx: float
    :param dt: The temporal resolution (the temporal size for the Edie's box).
    :type dt: float
    :param starttime: The start time for calculation (unix time).
    :type starttime: int
    :param endtime: The end time for calculation (unix time).
    :type endtime: int
    :param lane_number: the number of lane to be processed, lane1 is HOV lane, left most, lane 4 is the right most...
    :type lane_number: int

    :return: A DataFrame containing the speed mean field with columns ['t', 'x', 'speed'], representing time, space, and the estimated speed
    mean field. The speed is quantified with the unit of miles per hour (mph), with the columns ['t','x','speed'], time, space and the
    estimated speed
    :rtype: pandas.DataFrame

    Example:
        speed_mean_field = get_speed_mean_field('input_data.json', 0.1, 0.01, 0, 10)
    """
    time_range = endtime - starttime
    TTT_matrix = np.zeros((int(time_range / dt), int( testbed_mile / dx)))
    TTD_matrix = np.zeros((int(time_range / dt), int( testbed_mile / dx)))
    with open(input_filename, 'r') as input_file:
        # Create an ijson parser for items in the input file
        parser = ijson.items(input_file, 'item')
        for doc in parser:
            if ((float(doc['last_timestamp']) >= starttime)
                    & (float(doc['first_timestamp']) <= endtime)
                    & (int(doc['direction']) == -1)
                    & (int(doc['length']) > 0)):
                timestamp = get_array(doc.get("timestamp", None)) - starttime
                x_position = get_array(doc.get("x_position", None)) / 5280 - min_milemarker
                y_position = get_array(doc.get("y_position", None))
                data_index = pd.DataFrame(np.column_stack((timestamp, x_position, y_position)))
                data_index.columns = ['time', 'x', 'y']
                data_index['space_index'] = (data_index['x'] // dx)
                data_index['time_index'] = (data_index['time'] // dt)
                if(lane_number == 1):
                    data_index = data_index[(data_index.y >= 12) & (data_index.y < 24)]
                if(lane_number == 2):
                    data_index = data_index[(data_index.y >= 24) & (data_index.y < 36)]
                if(lane_number == 3):
                    data_index = data_index[(data_index.y >= 36) & (data_index.y < 48)]
                if(lane_number == 4):
                    data_index = data_index[(data_index.y >= 48) & (data_index.y < 60)]
                grouped = data_index.groupby(['space_index', 'time_index'])
                for (space, time), group_df in grouped:
                    if (time >= 0 and time < (int(time_range / dt)) and space >= 0 and space < (int(testbed_mile / dx))):
                        TTD_matrix[int(time)][int(space)] += (group_df.x.max() - group_df.x.min())
                        TTT_matrix[int(time)][int(space)] += (group_df.time.max() - group_df.time.min())
    speed_raw = pd.DataFrame(matrix_to_coordinates(3600 * TTD_matrix / TTT_matrix))
    speed_raw.columns = ['t', 'x', 'speed']
    return speed_raw