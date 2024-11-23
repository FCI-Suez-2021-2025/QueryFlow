from enum import Enum
import os
import re
import pandas as pd
import csv


class en_bird_part(Enum):
    head = 0
    leg = 1
    wing = 2
    tail = 3


class en_bird_head_pose(Enum):
    center = 0
    right = 1
    left = 2
    none = -1


class en_bird_leg_pose(Enum):
    down = 0
    up = 1
    none = -1


class en_bird_wing_pose(Enum):
    off = 0
    on = 1
    none = -1


class en_bird_tail_pose(Enum):
    center = 0
    right = 1
    left = 2
    none = -1


class cls_motion(object):
    def __init__(self):
        pass

    def process_frames(self, path):
        frames = os.listdir(path)  # A list of the Labeling
        # seconds = []  # A list of the Seconds
        dict_frame_time = {}
        # Extract the second from the img_Name
        for fileName in frames:
            frame_second = re.findall(r"\d+", fileName)
            # fill fileName_withoutTime for all frames
            dict_frame_time[frame_second] = os.path.splitext(fileName)[0].replace(
                frame_second, ""
            )
            """x = (fileName.split(".", 1)[1])
            statusOfHeads.append(x.split('_', 1)[0])
            res = list(map(int, frame_second))
            seconds.append(res)
            """
        self.get_motion_per_time(dict_frame_time)

    def get_motion_per_time(self, dict_frame_time):
        pose_change = False
        for index, cur_time in enumerate(sorted(dict_frame_time)):
            frame_curr = dict_frame_time[cur_time]
            frame_next = dict_frame_time[index + 1]
            birds_curr = self.get_pose(frame_curr)
            birds_next = self.get_pose(frame_next)
            # if there is a diff create a new obj that contain a time
            # change_start_time=time_next
            # pose_change=True
            # obj = (time_next , self.get_difference(birds_curr , bird_next))

    def get_difference(self, first_dict, second_dict):
        """
        i.e. [{head:right , leg:up, tail:left , wing:on }]
        i.e. [{head:left , leg:down, tail:left , wing:on }]
        result will be   [{head:left , leg:down}]
        :param first_dict:
        :param second_dict:
        :return: dict of the differences like [{head:left , leg:down}]
        """
        return {k: second_dict[k] for k in set(second_dict) - set(first_dict)}

    def get_pose(self, fileName_withoutTime_withoutExt):
        """
        return a list of dict
        a dict for each bird in the frame
        if a frame contain one bird then the list contain one dict
        i.e. [{head:right , leg:up, tail:left , wing:on }]
        Parameters:
        fileName_withoutTime_withoutExt: fileName withoutTime withoutExt

        Returns:
        listOfDict : return List of Dict
        """
        dict_bird_pose = {}
        # i.e. [{head:right , leg:up, tail:left , wing:on }]
        # convert the input string into the above format
        json_fileName_withoutTime_withoutExt = (
            fileName_withoutTime_withoutExt.replace(".", ":").replace("_", ",").lower()
        )
        # ('%f+i%f' % (r.real, r.imag))
        json_fileName_withoutTime_withoutExt = (
            "{%s}" % json_fileName_withoutTime_withoutExt
        )
        birds = []
        dict_bird_pose = eval(json_fileName_withoutTime_withoutExt)
        birds.append(dict_bird_pose)
        return birds
