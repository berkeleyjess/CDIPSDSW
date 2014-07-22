import pandas as pd
import numpy as np
import cPickle

# Goal is to make dataframe indexed by ping_id with all attributes included. Do not break into test and train.

#  Ping class from Jess
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

# Get Ping objects
pings = np.load('Data/berkeley_ping_data.npy')

# Get list of Ping attributes
bad_attributes = dir(Ping)
attributes = dir(pings[0])
for ba in bad_attributes: attributes.remove(ba)
print "Attributes to be stored:", attributes

# Put Ping objects into a dataframe
df_dict = {}
for a in attributes:
    i = 0
    series_dict = {}
    for ping in pings:
        series_dict[i] = eval('ping.'+a)
        i+=1
    s = pd.Series(series_dict)
    df_dict[a] = s
ping_df = pd.DataFrame(df_dict)

print "Created dataframe of all pings."

with open(r"Data/pingDataFrame.pickle", "wb") as output_file:
    cPickle.dump(ping_df, output_file)

