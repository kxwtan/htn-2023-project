import time
from flask import Flask, Response, render_template
import pandas as pd
import math
from csv import writer
from threading import Thread
import adhawkapi
import adhawkapi.frontend
from pygame import mixer
from textGen import generateWarning

notification_threshhold = 4
start_time = time.time()

close_counter = 0 # notifies user that there is a warning

far_counter = 0 # resets close counter after 1/2 * notification_threshhold
zvec_g = 0

xvec_g = 0

yvec_g = 0

message_sent = False



df = pd.DataFrame()

class FrontendData:
    ''' BLE Frontend '''

    def __init__(self):
        # Instantiate an API object
        # TODO: Update the device name to match your device
        self._api = adhawkapi.frontend.FrontendApi(ble_device_name='ADHAWK MINDLINK-302')

        # Tell the api that we wish to receive eye tracking data stream
        # with self._handle_et_data as the handler
        self._api.register_stream_handler(adhawkapi.PacketType.EYETRACKING_STREAM, self._handle_et_data)

        # Tell the api that we wish to tap into the EVENTS stream
        # with self._handle_events as the handler
        self._api.register_stream_handler(adhawkapi.PacketType.EVENTS, self._handle_events)

        # Start the api and set its connection callback to self._handle_tracker_connect/disconnect.
        # When the api detects a connection to a MindLink, this function will be run.
        self._api.start(tracker_connect_cb=self._handle_tracker_connect,
                        tracker_disconnect_cb=self._handle_tracker_disconnect)

    def shutdown(self):
        '''Shutdown the api and terminate the bluetooth connection'''
        self._api.shutdown()

    @staticmethod
    def _handle_et_data(et_data: adhawkapi.EyeTrackingStreamData):
        ''' Handles the latest et data '''
        if et_data.gaze is not None:
            xvec, yvec, zvec, vergence = et_data.gaze

            global close_counter
            global far_counter
            global notification_threshhold
            global xvec_g
            global yvec_g
            global zvec_g
            global message_sent

            xvec_g = xvec
            yvec_g = yvec
            zvec_g = zvec

            distance = math.sqrt(zvec**2 + xvec**2)

            if close_counter >= notification_threshhold:
                mixer.init()
                sound=mixer.Sound("ping.mp3")
                sound.play()
                close_counter = 0
                far_counter = 0
                distance = 0
                if message_sent == False:
                    print("SENT!")
                    generateWarning()
                    message_sent = True
            elif far_counter >= notification_threshhold:
                close_counter = 0
                far_counter = 0

            if distance <= 5:
                close_counter += 1
            elif zvec <= -10:
                far_counter += 1

            # print(f'Close_counter={close_counter}')
            # print(f'Far_counter={far_counter}')
            # print(f'Z-Gaze={zvec:.2f}')
            # print(f'Distance={distance}')

            # print(f'Gaze:x={xvec:.2f},y={yvec:.2f},z={zvec:.2f},vergence={vergence:.2f}')

            end_time = time.time()

            with open("data.csv", mode = 'a', newline='') as file:
                    # Pass this file object to csv.writer()
                # and get a writer object
                writer_object = writer(file)
            
                # Pass the list as an argument into
                # the writerow()
                writer_object.writerow([round(xvec, 2), round(yvec, 2), round(zvec, 2), round(vergence, 2), end_time-start_time])
            
                # Close the file object
                file.close()
            

            
        # if et_data.eye_center is not None:
        #     if et_data.eye_mask == adhawkapi.EyeMask.BINOCULAR:
        #         rxvec, ryvec, rzvec, lxvec, lyvec, lzvec = et_data.eye_center
        #         print(f'Eye center: Left=(x={lxvec:.2f},y={lyvec:.2f},z={lzvec:.2f}) '
        #               f'Right=(x={rxvec:.2f},y={ryvec:.2f},z={rzvec:.2f})')

        # if et_data.pupil_diameter is not None:
        #     if et_data.eye_mask == adhawkapi.EyeMask.BINOCULAR:
        #         rdiameter, ldiameter = et_data.pupil_diameter
        #         print(f'Pupil diameter: Left={ldiameter:.2f} Right={rdiameter:.2f}')

        # if et_data.imu_quaternion is not None:
        #     if et_data.eye_mask == adhawkapi.EyeMask.BINOCULAR:
        #         x, y, z, w = et_data.imu_quaternion
        #         print(f'IMU: x={x:.2f},y={y:.2f},z={z:.2f},w={w:.2f}')

    @staticmethod
    def _handle_events(event_type, timestamp, *args):
        if event_type == adhawkapi.Events.BLINK:
            duration = args[0]
            print(f'Got blink: {timestamp} {duration}')
        if event_type == adhawkapi.Events.EYE_CLOSED:
            eye_idx = args[0]
            print(f'Eye Close: {timestamp} {eye_idx}')
        if event_type == adhawkapi.Events.EYE_OPENED:
            eye_idx = args[0]
            print(f'Eye Open: {timestamp} {eye_idx}')

    def _handle_tracker_connect(self):
        print("Tracker connected")
        self._api.set_et_stream_rate(60, callback=lambda *args: None)

        self._api.set_et_stream_control([
            adhawkapi.EyeTrackingStreamTypes.GAZE,
            adhawkapi.EyeTrackingStreamTypes.EYE_CENTER,
            adhawkapi.EyeTrackingStreamTypes.PUPIL_DIAMETER,
            adhawkapi.EyeTrackingStreamTypes.IMU_QUATERNION,
        ], True, callback=lambda *args: None)

        self._api.set_event_control(adhawkapi.EventControlBit.BLINK, 1, callback=lambda *args: None)
        self._api.set_event_control(adhawkapi.EventControlBit.EYE_CLOSE_OPEN, 1, callback=lambda *args: None)

    def _handle_tracker_disconnect(self):
        print("Tracker disconnected")

def get_close_counter():
    global close_counter
    return close_counter

def get_far_counter():
    global far_counter
    return far_counter

def get_zvec():
    global zvec_g
    return zvec_g

def get_yvec():
    global yvec_g
    return yvec_g

def get_xvec():
    global xvec_g
    return xvec_g


def main():
    f = open("data.csv", "w")
    f.truncate()
    f.close()
    ''' App entrypoint '''

    print("seperate thread")
    frontend = FrontendData()
    # App Entry Point
    print("Entry: main()")

    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        frontend.shutdown()
main()