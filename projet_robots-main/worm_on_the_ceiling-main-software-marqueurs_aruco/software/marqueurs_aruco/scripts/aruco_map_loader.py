import numpy as np
import yaml

def load_aruco_map(file_path):
    file_stream = open(file_path, 'r')
    map_data = yaml.load(file_stream, Loader=yaml.Loader)
    file_stream.close()
    print(map_data)
    for aruco_map in map_data:
        map_of_aruco_markers = aruco_map['map_of_aruco_markers']
        for aruco in map_of_aruco_markers:
            aruco['position'] = np.array(aruco['position']).reshape((3, 1))
            aruco['rotation'] = np.array(aruco['rotation']).reshape((3, 1))
    return map_data

