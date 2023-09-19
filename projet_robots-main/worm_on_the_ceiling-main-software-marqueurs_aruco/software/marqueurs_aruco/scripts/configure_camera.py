import argparse

from yaml import load, dump
from yaml import Loader, Dumper
import time
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config', default='config.yaml')
parser.add_argument('-d', '--device', default='/dev/video2')
parser.add_argument('-i', '--ignore_auto', action='store_true')

args = parser.parse_args()

video_device = args.device

config_stream = open(args.config, "r")
config = load(config_stream, Loader=Loader)

print("Using video device : " + str(video_device))
print("Using config file : " + str(config_stream))

camera_init = config['camera_init']
fx = camera_init['u'] * camera_init['Zc'] / camera_init['Xc']
fy = camera_init['v'] * camera_init['Zc'] / camera_init['Yc']

print("focals fx=%f fy=%f"%(fx, fy))

delay = .2

v4l2 = config['v4l2']
for key in v4l2:
    print("Configuring %s : %s"%(key, v4l2[key]))
    command_line = ['v4l2-ctl', '-d', video_device]
    command_line.append('-c')
    command_line.append("%s=%s"%(key,v4l2[key]))
    process = subprocess.Popen(
        command_line,
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    time.sleep(delay)

print("Auto_white_balance")
if not args.ignore_auto:
    command_line = [
        'v4l2-ctl', '-d', video_device, '-c', 
        'white_balance_temperature_auto=1',
    ]
    process = subprocess.Popen(
        command_line,
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    time.sleep(15)

command_line = [
    'v4l2-ctl', '-d', video_device, '-c', 
    'white_balance_temperature_auto=0',
]
process = subprocess.Popen(
    command_line,
    stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE
)
stdout, stderr = process.communicate()

time.sleep(delay)

print("Auto_exposure")
if not args.ignore_auto:
    command_line = [
        'v4l2-ctl', '-d', video_device, '-c', 
        'exposure_auto_priority=1',
    ]
    process = subprocess.Popen(
        command_line,
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    time.sleep(15)

command_line = [
    'v4l2-ctl', '-d', video_device, '-c', 
    'exposure_auto_priority=0',
]
process = subprocess.Popen(
    command_line,
    stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE
)
stdout, stderr = process.communicate()

time.sleep(delay)

print("Auto focus")
if not args.ignore_auto:
    command_line = [
        'v4l2-ctl', '-d', video_device, '-c', 
        'focus_automatic_continuous=1',
    ]
    process = subprocess.Popen(
        command_line,
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    time.sleep(15)

print("Waiting for auto configuration")
command_line = [
    'v4l2-ctl', '-d', video_device, '-c', 
    'focus_automatic_continuous=0',
]
process = subprocess.Popen(
    command_line,
    stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE
)
stdout, stderr = process.communicate()

time.sleep(delay)

print("Stop auto focus")
