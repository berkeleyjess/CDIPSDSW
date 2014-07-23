import numpy


class TutorRedux:
    def __init__(self, tutor_id, timezone, lessons_completed, questions_answered,
                 reviewable_questions, reviewable_lessons, thumbs_down_questions,
                 thumbs_down_lessons):
        self.tutor_id = tutor_id
        self.timezone = timezone
        self.lessons_taught = (lessons_completed + questions_answered)
        self.negative_review_rate = (1.0 * (thumbs_down_questions + thumbs_down_lessons) /
                                     (self.lessons_taught + 1 ** -10))


messages = numpy.load('./berkeley_tutor_data.npy')
