import cv2
import numpy as np
import yaml
import argparse

parser = argparse.ArgumentParser(
    description=(
        "Generate a map of aruco marker to test pose estimation of a "
        "frameing grids in 3D"
    )
)

parser.add_argument(
    '-o', '--output',
    help="the output file containing the map (default: %(default)s).",
    default="map_of_aruco_markers.yaml",
)

args = parser.parse_args()

if args.output is None:
    print("Output ragument are missing (-o)")
file_path = args.output

aruco_map = []

N = 4
marker_id = 0

real_type = np.float64

ii = np.array([1, 0, 0], dtype=real_type)
jj = np.array([0, 1, 0], dtype=real_type)
kk = np.array([0, 0, 1], dtype=real_type)


def generate_marker_position(
    translation, axis, orientation, N, marker_id, aruco_informations
):
    for j in range(N):
        for i in range(N):
            position = translation + i * axis[0] + j * axis[1]
            aruco_informations.append({
                'id': marker_id,
                'position': list(map(float, list(position))),
                'rotation': list(map(float, list(orientation)))
            })
            marker_id += 1
    return marker_id


marker_id = 0
aruco_informations = []

cm = 0.01
size = 10 * cm
translation = np.array([3*cm, -3*cm, 0], dtype=real_type)
axis = [ii * size, -jj * size]
orientation = cv2.Rodrigues(np.eye(3, dtype=real_type))[0].reshape((3))
marker_id = generate_marker_position(
    translation, axis, orientation, N, marker_id, aruco_informations
)

translation = np.array([3*cm, 0, 3*cm], dtype=real_type)
axis = [kk * size, ii * size]
orientation = cv2.Rodrigues(
    np.array([
        [0, -1,  0],
        [0,  0, -1],
        [1,  0,  0],
    ], dtype=real_type)
)[0].reshape((3))
marker_id = generate_marker_position(
    translation, axis, orientation, N, marker_id, aruco_informations
)

translation = np.array([0, -3*cm, 3*cm], dtype=real_type)
axis = [-jj * size, kk * size]
orientation = cv2.Rodrigues(
    np.array([
        [ 0,  0, 1],
        [-1,  0, 0],
        [ 0, -1, 0],
    ], dtype=real_type)
)[0].reshape((3))
marker_id = generate_marker_position(
    translation, axis, orientation, N, marker_id, aruco_informations
)

aruco_dictionary_id = 0
aruco_size = 3*cm
data = [{
    'name': '3D Grid',
    'map_of_aruco_markers': aruco_informations,
    'aruco_dictionary_id': 0,
    'aruco_size': aruco_size
}]
output = yaml.dump(data, Dumper=yaml.Dumper)
file_stream = open(file_path, 'w')
file_stream.write(output)
file_stream.close()
