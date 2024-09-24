#!/usr/bin/env python3

"""
IHMC Interdependence Analytic Component

author: Roger Carff
email: rcarff@ihmc.org

author: Micael Vignati
email: mvignati@ihmc.org
"""

__author__ = 'mvignati'

import argparse
import logging
from datetime import datetime

from .agents import joint_activity_monitor as jam

FORMATTER = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s — %(message)s\n")

STREAM_HANDLER = logging.StreamHandler()
STREAM_HANDLER.setFormatter(FORMATTER)
STREAM_HANDLER.setLevel(logging.INFO)

FILE_HANDLER = logging.FileHandler(f"{datetime.now().strftime('%Y%m%dT%H%M%S')}.log")
FILE_HANDLER.setFormatter(FORMATTER)
FILE_HANDLER.setLevel(logging.DEBUG)


def arguments():
    ap = argparse.ArgumentParser()
    ap.add_argument('--visualizer', help='starts the trial visualizer', action='store_true', default=False)
    return ap.parse_args()


def init_logging():
    # configures the root logger
    logger = logging.getLogger()
    logger.setLevel(logging.NOTSET)
    logger.addHandler(STREAM_HANDLER)
    logger.addHandler(FILE_HANDLER)


def start_agent(visualizer=False):
    joint_activity_monitor = jam.JointActivityMonitor()
    joint_activity_monitor.start()

    if visualizer:
        from .views import map_view
        visualizer = map_view.MapView(joint_activity_monitor)
        visualizer.start_rendering_loop()


args = arguments()
init_logging()
start_agent(args.visualizer)
