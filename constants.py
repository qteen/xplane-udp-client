from enum import Enum

class MessageData(Enum):
    PITCH_DATA = ("pitch", "deg")
    ROLL_DATA = ("roll", "deg")
    TRUE_HEADING_DATA = ("true_heading", "deg")
    HEADING_DATA = ("heading", "deg")
    LATITUDE_DATA = ("latitude", "deg")
    LONGITUDE_DATA = ("longitude", "deg")
    SEA_ALTITUDE_DATA = ("sea_altitude", "ft")
    GROUND_ALTITUDE_DATA = ("ground_altitude", "ft")
    INDICATED_AIRSPEED_DATA = ("indicated_airspeed", "knots")
    EQUIVALENT_AIRSPEED_DATA = ("equivalent_airspeed", "knots")
    TRUE_AIRSPEED_DATA = ("true_airspeed", "knots")
    TRUE_GROUNDSPEED_DATA = ("ground_airspeed", "knots")
    SKIP = ("-", "-")

    def __init__(self, msg_label, msg_unit):
        self.msg_label = msg_label       
        self.msg_unit = msg_unit   

MESSAGE_INDEX17_TEMPLATE = [MessageData.PITCH_DATA, MessageData.ROLL_DATA, MessageData.TRUE_HEADING_DATA, MessageData.HEADING_DATA, MessageData.SKIP, MessageData.SKIP, MessageData.SKIP, MessageData.SKIP]
MESSAGE_INDEX20_TEMPLATE = [MessageData.LATITUDE_DATA, MessageData.LONGITUDE_DATA, MessageData.SEA_ALTITUDE_DATA, MessageData.GROUND_ALTITUDE_DATA, MessageData.SKIP, MessageData.SKIP, MessageData.SKIP, MessageData.SKIP]
MESSAGE_INDEX03_TEMPLATE = [MessageData.INDICATED_AIRSPEED_DATA, MessageData.EQUIVALENT_AIRSPEED_DATA, MessageData.TRUE_AIRSPEED_DATA, MessageData.TRUE_GROUNDSPEED_DATA, MessageData.SKIP, MessageData.SKIP, MessageData.SKIP, MessageData.SKIP]
MESSAGE_OTHER_TEMPLATE = [MessageData.SKIP, MessageData.SKIP, MessageData.SKIP, MessageData.SKIP, MessageData.SKIP, MessageData.SKIP, MessageData.SKIP, MessageData.SKIP]