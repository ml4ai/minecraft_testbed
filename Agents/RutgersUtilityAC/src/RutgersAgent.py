#!/usr/bin/env python3

"""
Rutgers-Utility Agent

This file makes use of template and helper library developed by Roger Carff, email:rcarff@ihmc.us
    * https://gitlab.com/ihmc-asist/python-agent-helper
    * https://gitlab.com/artificialsocialintelligence/study3/-/tree/main/ReferenceAgents/IHMCPythonAgentStarter
"""
import logging

from RutgersAgentHelper import PlayerUtility, on_message

# Agent Initialization
helper = PlayerUtility(on_message)


# Set the helper's logging level to INFO
LOG_HANDLER = logging.StreamHandler()
LOG_HANDLER.setFormatter(
    logging.Formatter("%(asctime)s | %(name)s | %(lineno)d | %(levelname)s — %(message)s")
)
helper.get_logger().setLevel(logging.INFO)
helper.get_logger().addHandler(LOG_HANDLER)

# Rutgers Agent Logger
logger = logging.getLogger("RutgersAgent")
logger.setLevel(logging.INFO)
logger.addHandler(LOG_HANDLER)


# Set the agents status to 'up' and start the agent loop on a separate thread
helper.set_agent_status(helper.STATUS_UP)
logger.info("Starting Agent Heartbeat Loop on a separate thread.")
helper.start_agent_loop_thread()
helper.start_belief_diff_publish_loop_thread()
# logger.info("Starting Agent Publish Loop on a separate thread.")
# helper.start_agent_publish_loop_thread()
# logger.info("Agent is now running...")
