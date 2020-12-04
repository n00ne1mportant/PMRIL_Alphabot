import configparser
from typing import List, Tuple

from cv2 import createTrackbar, namedWindow, setMouseCallback, imshow
from cv2.cv2 import putText
from numpy import ndarray

from detector.automatic_filter_tuner import AutomaticFilterTuner
from detector.tracker import Tracker
from models.hsv_filter import HSVFilter
from models.object import Object
from presentation.drawer import Drawer


class PresentationManager:
    def __init__(self, config: configparser.ConfigParser, filter_tuner: AutomaticFilterTuner):
        self.__filter_tuner = filter_tuner
        self.__config = config
        self.__tracker = Tracker(config)
        self.__drawer = Drawer(config)

        self.__initialize()

    """Redraws the image based on camera feed with any objects that might appear"""
    def refresh(self, camera_feed, filtered_objects: List[Tuple[List[Object], List[ndarray], ndarray]]) -> None:
        for (objects, contours, hierarchy) in filtered_objects:
            self.__drawer.mark_objects(objects, camera_feed, contours, hierarchy)

        self.__refresh(camera_feed)

    def display_error(self, camera_feed, message: str) -> None:
        putText(camera_feed, message, (0, 50), 1, 2, (255, 0, 0), 2)
        self.__refresh(camera_feed)

    def display_message(self, camera_feed, message: str) -> None:
        putText(camera_feed, message, (0, 50), 1, 2, (0, 0, 255), 2)
        self.__refresh(camera_feed)

    def __refresh(self, camera_feed):
        # TODO: Make this configurable
        # imshow(config['window']['name2'], compound_threshold_matrix if compound_threshold_matrix is not None else blank_image)
        # imshow(config['window']['name1'], hsv_matrix)
        # imshow('morphed', morphed_matrix)

        imshow(self.__config['window']['original'], camera_feed)

        # imshow(config['window']['thresholded'], threshold_matrix)
        # imshow(config['window']['name1'], hsv_matrix)
        # imshow('morphed', morphed_matrix)

    def __initialize(self) -> None:
        if self.__config.getboolean('other', 'calibration_mode'):
            self.__create_trackbars(HSVFilter(0, 255, 0, 255, 0, 255))

        namedWindow(self.__config['window']['original'])
        setMouseCallback(self.__config['window']['original'], self.__filter_tuner.clickAndDrag_Rectangle)

    def __create_trackbars(self, hsv_filter: HSVFilter) -> None:
        namedWindow(self.__config['window']['trackbar'], 0)

        createTrackbar('H_MIN', self.__config['window']['trackbar'], hsv_filter.H_MIN, hsv_filter.H_MAX,
                       lambda x: hsv_filter.set_H_MAX(x))
        createTrackbar('H_MAX', self.__config['window']['trackbar'], hsv_filter.H_MAX, hsv_filter.H_MAX,
                       lambda x: hsv_filter.set_H_MAX(x))
        createTrackbar('S_MIN', self.__config['window']['trackbar'], hsv_filter.S_MIN, hsv_filter.S_MAX,
                       lambda x: hsv_filter.set_S_MIN(x))
        createTrackbar('S_MAX', self.__config['window']['trackbar'], hsv_filter.S_MAX, hsv_filter.S_MAX,
                       lambda x: hsv_filter.set_S_MAX(x))
        createTrackbar('V_MIN', self.__config['window']['trackbar'], hsv_filter.V_MIN, hsv_filter.V_MAX,
                       lambda x: hsv_filter.set_V_MIN(x))
        createTrackbar('V_MAX', self.__config['window']['trackbar'], hsv_filter.V_MAX, hsv_filter.V_MAX,
                       lambda x: hsv_filter.set_V_MAX(x))