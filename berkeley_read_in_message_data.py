import numpy


 #  Clients: Gtalk = 1, Facebook = 2, InstaEDU = 3
 #  Timezones: See pytz.common_timezones
class Messages:
    def __init__(self, message_id, time_sent, tutor_id, client, available, available_now, busy,
                 last_impression_time, last_seen_online_time, timezone, reply_time):
        self.id = message_id
        self.time_sent = time_sent
        self.tutor_id = tutor_id
        self.client = client
        self.available = available
        self.available_now = available_now
        self.busy = busy
        self.last_impression_time = last_impression_time
        self.last_seen_online_time = last_seen_online_time
        self.timezone = timezone
        self.first_reply_time = reply_time


messages = numpy.load('./berkeley_message_data.npy')
