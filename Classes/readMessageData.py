import pandas as pd
import numpy as np
import cPickle

#  Message class from Jess
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

# Get messages info
messages = np.load('Data/berkeley_message_data.npy')

# Get list of Message attributes
bad_attributes = dir(Messages)
attributes = dir(messages[0])
for ba in bad_attributes: attributes.remove(ba)
print "Attributes to be stored:", attributes

# Put Message objects into a dataframe
df_dict = {}
for a in attributes:
    i = 0
    series_dict = {}
    for message in messages:
        series_dict[i] = eval('message.'+a)
        i+=1
    s = pd.Series(series_dict)
    df_dict[a] = s
message_df = pd.DataFrame(df_dict)

print "Created dataframe of all messages."

with open(r"Data/messageDataFrame.pickle", "wb") as output_file:
    cPickle.dump(message_df, output_file)

