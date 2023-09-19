import argparse
import cv2
import numpy as np
from cv2 import aruco
import aruco_map_loader

import solve_linear_equation as sle

parser = argparse.ArgumentParser(
    description='Detect Aruco markers in video.'
)


parser.add_argument(
    '--ci',
    help='camera devices',
    nargs="+",
    type=int
)
parser.add_argument(
    '-c',
    nargs="+",
    help='camera intrinsinc parameters.'
)
parser.add_argument(
    '-v',
    nargs="+",
    help=(
        "Input from video file, if ommited, input comes from camera (see --ci)"
    ),
)
parser.add_argument(
    '-s',
    nargs="+",
    help='save camera streams into video files.'
)
parser.add_argument(
    '-m',
    help="the aruco map file.",
)

parser.add_argument(
    '--width',
    default=960,
    help="displaying image widht. (default:%(default)s)",
    type=int
)

parser.add_argument(
    '--height',
    default=540,
    help="displaying image widht. (height:%(default)s)",
    type=int
)

parser.add_argument(
    '--ncols',
    default=3,
    help="Parameter for the method that estimate the camera frame."
         "--ncols=1: use only aruco position to estimate the camera frame. "
         "--ncols=2: use aruco position and the first column (X) of the "
         "matrix rotation of the aruco markers. "
         "--ncols=3: use aruco position and the first and second column "
         "(X and Y) of the matrix rotation of the aruco markers. "
         "--ncols=4: use the position and the rotation of the aruco markers "
         "     (default=%(default)s).",
    type=int
)

refine_ids = {
    "CORNER_REFINE_NONE": aruco.CORNER_REFINE_NONE,
    "CORNER_REFINE_SUBPIX": aruco.CORNER_REFINE_SUBPIX,
    "CORNER_REFINE_CONTOUR": aruco.CORNER_REFINE_CONTOUR,
    "CORNER_REFINE_APRILTAG": aruco.CORNER_REFINE_APRILTAG,
}


def dict_to_help(dic):
    res = ""
    for key in dic:
        res += (key + '=' + str(dic[key]) + ', ')
    return res


refine_help_text = "Corner refinement : " + dict_to_help(refine_ids)
parser.add_argument('--refine', help=refine_help_text, type=int)
parser.add_argument('--dp', help="File of marker detector parameters")

args = parser.parse_args()

if not(1 <= args.ncols <= 4):
    print("--ncols should be an integer from 1 to 4.")
    quit()

if args.ci is None and args.v is None:
    print("Camera device (--ci) or video file (-v) is missing.")
    quit()

if args.ci is not None:
    use_camera = True
    nb_stream = len(args.ci)
else:
    use_camera = False
    nb_stream = len(args.v)

if use_camera and args.s is not None:
    if nb_stream != len(args.s) :
        print("There is no enought video file names in -s.")
        quit()
    save_camera_stream = True


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

all_camera_parameters = []
for file_path in args.c:
    fs = cv2.FileStorage(file_path, cv2.FILE_STORAGE_READ)
    all_camera_parameters.append({
        "camera_matrix": fs.getNode("camera_matrix").mat(),
        "camera_distortion": fs.getNode("camera_distortion").mat(),
    })


if args.m is None:
    print("A aruco map file is required (-m)?")
    quit()

map_data = aruco_map_loader.load_aruco_map(args.m)
for aruco_map in map_data:
    aruco_map['aruco_dictionary'] = aruco.getPredefinedDictionary(
        aruco_map['aruco_dictionary_id']
    )
    map_of_aruco_markers = {}
    for aruco_marker in aruco_map['map_of_aruco_markers']:
        map_of_aruco_markers[aruco_marker['id']] = [
            aruco_marker['position'], aruco_marker['rotation']
        ]
    aruco_map['map_of_aruco_markers'] = map_of_aruco_markers

green = (0, 255, 0)

if args.v is not None:
    video_captures = [cv2.VideoCapture(video_file) for video_file in args.v]
    wait_time = 10  # ms
else:
    video_captures = [
        cv2.VideoCapture(camera_device) for camera_device in args.ci
    ]
    wait_time = 10  # ms


def detects_free_and_static_aruco_of_a_map_in_image(
    image, camera_parameters, aruco_map, objects, detected_arucos
):
    camera_matrix = camera_parameters['camera_matrix']
    camera_distortion = camera_parameters['camera_distortion']
    aruco_dictionary = aruco_map['aruco_dictionary']
    aruco_dictionary_id = aruco_map['aruco_dictionary_id']
    marker_length = aruco_map['aruco_size']
    corners, ids, rejectedImgPoints = aruco.detectMarkers(
        image, aruco_dictionary, parameters=detector_parameters,
        cameraMatrix=camera_matrix, distCoeff=camera_distortion
    )
    detected_arucos[aruco_dictionary_id] = {}
    detected_arucos[aruco_dictionary_id]['corners'] = corners
    detected_arucos[aruco_dictionary_id]['ids'] = ids
    detected_arucos[aruco_dictionary_id]['rvecs'] = None
    detected_arucos[aruco_dictionary_id]['tvecs'] = None
    detected_arucos[aruco_dictionary_id]['marker_length'] = marker_length

    if (ids is not None) and (len(ids) > 0):
        rvecs, tvecs, _objPoints = aruco.estimatePoseSingleMarkers(
            corners, marker_length, camera_matrix, camera_distortion
        )
        detected_arucos[aruco_dictionary_id]['rvecs'] = rvecs
        detected_arucos[aruco_dictionary_id]['tvecs'] = tvecs
        for i in range(len(ids)):
            aruco_id = ids[i][0]
            if aruco_id in aruco_map['map_of_aruco_markers']:
                objects['static_camera'][
                    (aruco_dictionary_id, aruco_id)
                ] = [
                    tvecs[i].reshape((-1, 1)),
                    rvecs[i].reshape((-1, 1))
                ]
                objects['static_absolute_theoric'][
                    (aruco_dictionary_id, aruco_id)
                ] = aruco_map['map_of_aruco_markers'][aruco_id]
            else:
                objects['free_camera'][
                    (aruco_dictionary_id, aruco_id)
                ] = [
                    tvecs[i].reshape((-1, 1)),
                    rvecs[i].reshape((-1, 1))
                ]


def construct_scene_with_camera_free_and_static_aruco(
    image, camera_parameters, map_data, nb_of_columns
):
    assert(1 <= nb_of_columns <= 4)
    objects = {
        'camera': None, 'static_absolute': {}, 'static_camera': {}, 'static_absolute_theoric': {},
        'free_camera': {}, 'free_absolute': {}
    }
    detected_arucos = {}

    for aruco_map in map_data:
        detects_free_and_static_aruco_of_a_map_in_image(
            image, camera_parameters, aruco_map, objects, detected_arucos
        )

    absolute = []
    camera = []

    for aruco_inf in objects['static_absolute_theoric']:
        absolute += [
            objects['static_absolute_theoric'][aruco_inf][0],
            cv2.Rodrigues(objects['static_absolute_theoric'][aruco_inf][1])[0][
                :, :nb_of_columns - 1
            ]
        ]
        camera += [
            objects['static_camera'][aruco_inf][0],
            cv2.Rodrigues(objects['static_camera'][aruco_inf][1])[0][
                :, :nb_of_columns - 1
            ]
        ]
    if len(absolute) != 0:
        absolute = np.hstack(absolute)
        camera = np.hstack(camera)

        One_Zero = np.hstack([
            np.array([[1.0] + [0.0 for i in range(nb_of_columns - 1)]])
            for id_ in range(camera.shape[1] // nb_of_columns)
        ])

        def camera_frame_to_absolute(L1, L2):
            Q, C = L2
            return Q @ camera + C @ One_Zero

        res_S, res_M, det = sle.solve_linear_equation(
            absolute, camera_frame_to_absolute, [], [(3, 3), (3, 1)]
        )
        Q, C = res_M
        objects['camera'] = [C, Q]
        for aruco_inf in objects['free_camera']:
            position = objects['free_camera'][aruco_inf][0]
            rotation = objects['free_camera'][aruco_inf][1]
            objects['free_absolute'][aruco_inf] = [
                Q @ position + C,
                cv2.Rodrigues(Q @ cv2.Rodrigues(rotation)[0])[0]
            ]
        for aruco_inf in objects['static_camera']:
            position = objects['static_camera'][aruco_inf][0]
            rotation = objects['static_camera'][aruco_inf][1]
            objects['static_absolute'][aruco_inf] = [
                Q @ position + C,
                cv2.Rodrigues(Q @ cv2.Rodrigues(rotation)[0])[0]
            ]
    return objects, detected_arucos


def draw_aruco_and_axis_on_image(image, detected_arucos, camera_parameters):
    camera_matrix = camera_parameters['camera_matrix']
    camera_distortion = camera_parameters['camera_distortion']
    for dictionary_id in detected_arucos:
        corners = detected_arucos[dictionary_id]['corners']
        ids = detected_arucos[dictionary_id]['ids']
        rvecs = detected_arucos[dictionary_id]['rvecs']
        tvecs = detected_arucos[dictionary_id]['tvecs']
        marker_length = detected_arucos[dictionary_id]['marker_length']

        borderColor = green
        image = cv2.aruco.drawDetectedMarkers(
            image, corners, ids, borderColor
        )

        if ids is not None:
            for i in range(len(ids)):
                aruco.drawAxis(
                    image, camera_matrix, camera_distortion,
                    rvecs[i], tvecs[i],
                    marker_length * 0.5
                )


def print_scene_and_free_markers(scene, camera_id):
    print("### camera %d ###" % camera_id)
    camera_position = scene['camera'][0]
    print(camera_position)
    for aruco_inf in scene['free_camera']:
        print("Free aruco marker : %s " % (str(aruco_inf)))
        print("position : ")
        print(scene['free_absolute'][aruco_inf][0])
        print("rotation : ")
        print(scene['free_absolute'][aruco_inf][1])

    #print("@@@@@@@@@@@@@@@")
    #print(scene)
    #print("@@@@@@@@@@@@@@@")

    
def display_images_in_mosaic(images):
    width = args.width
    height = args.height
    N_images = len(images)
    for id_img in range(N_images):
        images[id_img] = cv2.resize(
            images[id_img], (width//N_images, height//N_images))
    if len(images) > 0:
        screen = np.hstack(images)
        cv2.imshow('all cameras', screen)


images_for_video_copy = [[] for i in range(nb_stream)]
while(True):
    images_to_display = []
    scene_by_camera = []
    for camera_id in range(len(video_captures)):
        retval, image = video_captures[camera_id].read()
        if not retval:
            break

        (
            scene, all_detected_arucos
        ) = construct_scene_with_camera_free_and_static_aruco(
            image, all_camera_parameters[camera_id], map_data, args.ncols
        )
        scene_by_camera.append(scene)

        print_scene_and_free_markers(scene, camera_id)

        if args.s is not None:
            images_for_video_copy[camera_id].append(image.copy())

        draw_aruco_and_axis_on_image(
            image, all_detected_arucos, all_camera_parameters[camera_id]
        )

        images_to_display.append(image)

    display_images_in_mosaic(images_to_display)

    esc_key = 27
    key = cv2.waitKey(wait_time)
    if key == esc_key:
        break


def save_images_inside_a_video(video_path, images, frame_per_second):
    video_writer = cv2.VideoWriter(
        args.s[i],
        cv2.VideoWriter_fourcc('F', 'F', 'V', '1'),
        # cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
        frame_per_second, (images[0].shape[1], images[0].shape[0])
    )
    for image in images:
        video_writer.write(image)
    video_writer.release()


if args.s is not None:
    for i in range(len(args.s)):
        save_images_inside_a_video(
            args.s[i], images_for_video_copy[i], frame_per_second=20
        )
