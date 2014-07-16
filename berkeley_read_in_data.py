import numpy


 #  Clients: Gtalk = 1, Facebook = 2, InstaEDU = 3
 #  Timezones: See pytz.common_timezones
class Ping:
    def __init__(self, ping_id, lesson_id, lesson_subject, tutor_id, client, available,
                 available_now, last_impression_time, last_seen_online_time, timezone,
                 time_clicked, time_sent_success, time_clicked_score):
        self.id = ping_id
        self.lesson_id = lesson_id
        self.lesson_subject = lesson_subject
        self.tutor_id = tutor_id
        self.client = client
        self.available = available
        self.available_now = available_now
        self.last_impression_time = last_impression_time
        self.last_seen_online_time = last_seen_online_time
        self.timezone = timezone

        self.time_clicked = time_clicked
        self.time_sent_success = time_sent_success
        self.time_clicked_score = time_clicked_score


pings = numpy.load('./berkeley_ping_data.npy')
