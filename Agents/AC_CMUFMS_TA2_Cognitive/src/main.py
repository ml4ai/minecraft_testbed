#!/usr/bin/env python3

"""
CMUFMS Cognitive Analytic Component

author: Don Morrison
email: dfm2@cmu.edu
"""

__author__ = 'dfm2'

import logging
import argparse

import iac

LOGGER = "IHMCInterdependenceAC"
LOG_HANDLER = logging.StreamHandler()
LOG_HANDLER.setFormatter(logging.Formatter("%(asctime)s | %(name)s | %(levelname)s — %(message)s"))


def arguments():
    ap = argparse.ArgumentParser()
    return ap.parse_args()


def init_logging():
    logger = logging.getLogger(LOGGER)
    logger.setLevel(logging.INFO)
    logger.addHandler(LOG_HANDLER)


def start_agent(visualizer=False):
    logger = logging.getLogger(LOGGER)
    logger.info("CMUFMS Cognitive Agent")
    ac = iac.InterdependenceAC()
    ac.start()


if __name__ == "__main__":
    args = arguments()
    init_logging()
    start_agent()
