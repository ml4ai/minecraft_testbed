from datetime import datetime
from scipy.spatial import distance
import logging


class ASISTToolsClass(object):

    def __init__(self):
        self.__logging = logging.getLogger(__name__)
        self.client_info = None

    def set_logger(self, logger):
        self.__logging = logger

    def set_logging_level(self, level):
        self.__logging.setLevel(level)

    def get_logger(self):
        return self.__logging

    def date_string_to_timestamp(self, date_string):
        timestamp = None
        # removes the Z to make it correct iso
        iso = date_string
        if iso[-1] == 'Z':
            iso = date_string[:-1]
        if len(iso) > 23:
            iso = iso[0:23]
        try:
            timestamp = datetime.fromisoformat(iso).timestamp()

        except Exception as ex:
            self.__logging.error(ex)
            self.__logging.error('Invalid iso time: ' + date_string)

        if timestamp is None:
            try:
                timestamp = datetime.strptime(iso, '%Y-%m-%dT%H:%M:%S.%f').timestamp()
            except Exception as ex:
                self.__logging.error(ex)
                self.__logging.error('Invalid time: ' + date_string)

        return timestamp

    @staticmethod
    def generate_asist_timestamp():
        return str(datetime.utcnow().isoformat()) + 'Z'

    @staticmethod
    def distance_euclidean(p1, p2):
        coords = [p1, p2]
        dist = distance.cdist(coords, coords, 'euclidean')
        return dist[0][1]

    def set_client_info(self, client_info):
        self.client_info = client_info

    def get_player_callsign(self, data):
        callsign = None
        if data is None:
            return callsign

        if 'callsign' in data.keys():
            return data['callsign'].lower().strip()

        if self.client_info is None:
            return callsign

        playername = data['playername'] if 'playername' in data.keys() else None
        participant_id = data['participant_id'] if 'participant_id' in data.keys() else None

        for client in self.client_info:
            if 'participant_id' in client.keys():
                if participant_id is not None and client['participant_id'] == participant_id:
                    callsign = client['callsign'].lower().strip()
            elif 'participantid' in client.keys():
                if participant_id is not None and client['participantid'] == participant_id:
                    callsign = client['callsign'].lower().strip()
            if callsign is None and playername is not None and 'playername' in client.keys() and client['playername'] == playername:
                callsign = client['callsign'].lower().strip()
        return callsign


ASISTTools = ASISTToolsClass()
