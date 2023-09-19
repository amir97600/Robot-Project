import argparse
import cv2
import numpy as np
from cv2 import aruco

parser = argparse.ArgumentParser(
    description='Detec Aruco markers in video.'
)

dictionary_ids = {
    "DICT_4X4_50": aruco.DICT_4X4_50,
    "DICT_4X4_100": aruco.DICT_4X4_100,
    "DICT_4X4_250": aruco.DICT_4X4_250,
    "DICT_4X4_1000": aruco.DICT_4X4_1000,
    "DICT_5X5_50": aruco.DICT_5X5_50,
    "DICT_5X5_100": aruco.DICT_5X5_100,
    "DICT_5X5_250": aruco.DICT_5X5_250,
    "DICT_5X5_1000": aruco.DICT_5X5_1000,
    "DICT_6X6_50": aruco.DICT_6X6_50,
    "DICT_6X6_100": aruco.DICT_6X6_100,
    "DICT_6X6_250": aruco.DICT_6X6_250,
    "DICT_6X6_1000": aruco.DICT_6X6_1000,
    "DICT_7X7_50": aruco.DICT_7X7_50,
    "DICT_7X7_100": aruco.DICT_7X7_100,
    "DICT_7X7_250": aruco.DICT_7X7_250,
    "DICT_7X7_1000": aruco.DICT_7X7_1000,
    "DICT_ARUCO_ORIGINAL": aruco.DICT_ARUCO_ORIGINAL,
    "DICT_APRILTAG_16h5": aruco.DICT_APRILTAG_16h5,
    "DICT_APRILTAG_25h9": aruco.DICT_APRILTAG_25h9,
    "DICT_APRILTAG_36h10": aruco.DICT_APRILTAG_36h10,
    "DICT_APRILTAG_36h11": aruco.DICT_APRILTAG_36h11,
}


def dict_to_help(dic):
    res = ""
    for key in dic:
        res += (key + '=' + str(dic[key]) + ', ')
    return res


dictionary_help_text = "dictionary : " + dict_to_help(dictionary_ids)
parser.add_argument(
    '-d', '--dictionary',
    help=dictionary_help_text,
    type=int
)
parser.add_argument(
    '--ci',
    help='camera device',
    type=int
)
parser.add_argument(
    '-c',
    help='camera intrinsinc parameters.'
)
parser.add_argument(
    '-l',
    help=(
        "Marker side length (in meters). Needed for correct scale in camera "
        "pose."
    ),
    default=0.1,
    type=float
)
parser.add_argument(
    '-v',
    help=(
        "Input from video file, if ommited, input comes from camera (see --ci)"
    ),
)

refine_ids = {
    "CORNER_REFINE_NONE": aruco.CORNER_REFINE_NONE,
    "CORNER_REFINE_SUBPIX": aruco.CORNER_REFINE_SUBPIX,
    "CORNER_REFINE_CONTOUR": aruco.CORNER_REFINE_CONTOUR,
    "CORNER_REFINE_APRILTAG": aruco.CORNER_REFINE_APRILTAG,
}

refine_help_text = "Corner refinement : " + dict_to_help(refine_ids)
parser.add_argument('--refine', help=refine_help_text, type=int)
parser.add_argument('--dp', help="File of marker detector parameters")

args = parser.parse_args()

if args.ci is None and args.v is None:
    print("Camera device (--ci) or video file (-v) is missing.")
    quit()


def get_vector(positions, i1, i2):
    if not(
        i1 in positions and
        i2 in positions
    ):
        return None
    A1 = positions[i1][0]
    A2 = positions[i2][0]
    v = A2 - A1
    return v


def get_2vectors(positions, i1, i2, j1, j2):
    u = get_vector(positions, i1, i2)
    v = get_vector(positions, j1, j2)
    if not(u is not None and v is not None):
        return None
    return (u, v)


def print_orthogonality(positions, i1, i2, j1, j2):
    res = get_2vectors(positions, i1, i2, j1, j2)
    if res is None:
        return None
    u, v = res
    res = (u @ v.T)[0, 0]
    nu = np.linalg.norm(u)
    nv = np.linalg.norm(v)
    cos = np.abs(res)/(nu*nv)
    theta = np.arccos(cos)
    print(
        "< P[%d]-P[%d] | P[%d]-P[%d] > = %s" % (
            i2, i1, j2, j1, res
        )
    )
    print("theta = %s °" % (theta*360/(2*np.pi)))
    return res

def print_parallel(positions, i1, i2, j1, j2):
    res = get_2vectors(positions, i1, i2, j1, j2)
    if res is None:
        return None
    u, v = res
    res = np.norm( np.linalg.vect(u, v) )
    nu = np.linalg.norm(u)
    nv = np.linalg.norm(v)
    sin = np.abs(res)/(nu*nv)
    theta = np.abs(np.arcsin(sin))
    print(
        "|| P[%d]-P[%d] ^ P[%d]-P[%d] || = %s" % (
            i2, i1, j2, j1, res
        )
    )
    print("theta = %s °" % (theta*360/(2*np.pi)))
    return res


def print_norm(positions, i1, i2):
    u = get_vector(positions, i1, i2)
    if u is None:
        return None
    res = np.linalg.norm(u)
    print(
        "|| P[%d]-P[%d] || = %s" % (
            i2, i1, res
        )
    )
    return u


def print_vectorial_info(positions, i1, i2, j1, j2, type):
    print_norm(positions, i1, i2)
    print_norm(positions, j1, j2)
    if type == 'orthogonal':
        print_orthogonality(positions, i1, i2, j1, j2)
    else:
        print_parallel(positions, i1, i2, j1, j2)


def print_tests(aruco_positions):
    print("#######")
    print_vectorial_info(aruco_positions, 1, 5, 1, 2, 'orthogonal')
    print_vectorial_info(aruco_positions, 32, 33, 16, 20, 'orthogonal')


def read_detector_parameters(filename, detector_parameters):
    fs = cv2.FileStorage(filename, cv2.FILE_STORAGE_READ)
    if not fs.isOpened():
        return False

    node = fs.getNode("adaptiveThreshWinSizeMin")
    detector_parameters.adaptiveThreshWinSizeMin = int(node.real())

    node = fs.getNode("adaptiveThreshWinSizeMax")
    detector_parameters.adaptiveThreshWinSizeMax = int(node.real())

    node = fs.getNode("adaptiveThreshWinSizeStep")
    detector_parameters.adaptiveThreshWinSizeStep = int(node.real())

    node = fs.getNode("adaptiveThreshConstant")
    detector_parameters.adaptiveThreshConstant = node.real()

    node = fs.getNode("minMarkerPerimeterRate")
    detector_parameters.minMarkerPerimeterRate = node.real()

    node = fs.getNode("maxMarkerPerimeterRate")
    detector_parameters.maxMarkerPerimeterRate = node.real()

    node = fs.getNode("polygonalApproxAccuracyRate")
    detector_parameters.polygonalApproxAccuracyRate = node.real()

    node = fs.getNode("minCornerDistanceRate")
    detector_parameters.minCornerDistanceRate = node.real()

    node = fs.getNode("minDistanceToBorder")
    detector_parameters.minDistanceToBorder = int(node.real())

    node = fs.getNode("minMarkerDistanceRate")
    detector_parameters.minMarkerDistanceRate = node.real()

    node = fs.getNode("cornerRefinementMethod")
    detector_parameters.cornerRefinementMethod = int(node.real())

    node = fs.getNode("cornerRefinementWinSize")
    detector_parameters.cornerRefinementWinSize = int(node.real())

    node = fs.getNode("cornerRefinementMaxIterations")
    detector_parameters.cornerRefinementMaxIterations = int(node.real())

    node = fs.getNode("cornerRefinementMinAccuracy")
    detector_parameters.cornerRefinementMinAccuracy = node.real()

    node = fs.getNode("markerBorderBits")
    detector_parameters.markerBorderBits = int(node.real())

    node = fs.getNode("perspectiveRemovePixelPerCell")
    detector_parameters.perspectiveRemovePixelPerCell = int(node.real())

    node = fs.getNode("perspectiveRemoveIgnoredMarginPerCell")
    detector_parameters.perspectiveRemoveIgnoredMarginPerCell = node.real()

    node = fs.getNode("maxErroneousBitsInBorderRate")
    detector_parameters.maxErroneousBitsInBorderRate = node.real()

    node = fs.getNode("minOtsuStdDev")
    detector_parameters.minOtsuStdDev = node.real()

    node = fs.getNode("errorCorrectionRate")
    detector_parameters.errorCorrectionRate = node.real()
    return True


detector_parameters = aruco.DetectorParameters_create()
if args.dp is not None:
    read_detector_parameters(args.dp, detector_parameters)

if args.refine is not None:
    detector_parameters.cornerRefinementMethod = args.refine

fs = cv2.FileStorage(args.c, cv2.FILE_STORAGE_READ)
camera_matrix = fs.getNode("camera_matrix").mat()
camera_distortion = fs.getNode("distortion_coefficients").mat()

estimate_pos = False
if args.l is not None:
    estimate_pos = True
    marker_length = args.l

aruco_dictionary = aruco.getPredefinedDictionary(args.dictionary)

green = (0, 255, 0)

if args.v is not None:
    video_capture = cv2.VideoCapture(args.v)
    wait_time = 10  # ms
else:
    video_capture = cv2.VideoCapture(args.ci)
    wait_time = 10  # ms

aruco_positions_average = {}
while(True):
    retval, image = video_capture.read()
    if not retval:
        break

    corners, ids, rejectedImgPoints = aruco.detectMarkers(
        image, aruco_dictionary, parameters=detector_parameters,
        cameraMatrix=camera_matrix, distCoeff=camera_distortion
    )
    borderColor = green

    if(estimate_pos and ids is not None and len(ids) > 0):
        rvecs, tvecs, _objPoints = aruco.estimatePoseSingleMarkers(
            corners, marker_length, camera_matrix, camera_distortion
        )

    image = cv2.aruco.drawDetectedMarkers(image, corners, ids, borderColor)

    if estimate_pos and ids is not None:
        for i in range(len(ids)):
            aruco.drawAxis(
                image, camera_matrix, camera_distortion,
                rvecs[i], tvecs[i],
                marker_length * 0.5
            )
        aruco_positions = {}
        N = 30
        for i in range(len(ids)):
            aruco_id = ids[i][0]
            aruco_positions[aruco_id] = [tvecs[i], rvecs[i]]

            if aruco_id not in aruco_positions_average:
                aruco_positions_average[aruco_id] = [
                    np.array([[100, 0, 0]]),
                    np.array([[100, 0, 0]])
                ]
            tr = (
                (aruco_positions_average[aruco_id][0] * ((N-1)/N)) +
                (tvecs[i] * (1/N))
            )
            rot = (
                (aruco_positions_average[aruco_id][1] * ((N-1)/N)) +
                (rvecs[i] * (1/N))
            )
            aruco_positions_average[aruco_id] = [tr, rot]
        print("Averages :")
        print_tests(aruco_positions_average)
        print("Instant :")
        print_tests(aruco_positions)
    cv2.imshow('frame', image)
    esc_key = 27
    key = cv2.waitKey(wait_time)
    if key == esc_key:
        break

video_capture.release()
