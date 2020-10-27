from gps3.agps3threaded import AGPS3mechanism
agps_thread = AGPS3mechanism()  # Instantiate AGPS3 Mechanisms
agps_thread.stream_data()  # From localhost (), or other hosts, by example, (host='gps.ddns.net')
agps_thread.run_thread()  # Throttle time to sleep after an empty lookup, default '()' 0.2 two tenths of a second

class GpsData(object):

    def __init__(self):
        self.lat = agps_thread.data_stream.lat
        self.lon = agps_thread.data_stream.lon
        self.speed = agps_thread.data_stream.speed
        self.course = agps_thread.data_stream.track

    def get_speed(self):
        self.speed = agps_thread.data_stream.speed
        return self.speed
    
    def get_lat(self):
        self.lat = agps_thread.data_stream.lat
        return self.lat
    
    def get_lon(self):
        self.lon = agps_thread.data_stream.lon
        return self.lon
