import numpy


class MessagesOld:
    def __init__(self, message_id, time_sent, tutor_id, read_at, message_length,
                 search_term, reply_time):
        self.id = message_id
        self.time_sent = time_sent
        self.tutor_id = tutor_id
        self.read_at = read_at
        self.message_length = message_length
        self.search_term = search_term
        self.reply_time = reply_time


messages = numpy.load('./berkeley_old_message_data.npy')
