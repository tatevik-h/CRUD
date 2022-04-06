from src.models import Feedback


class FilterQueryBuilder:
    @classmethod
    def create(cls, filters=None):
        filter_query = []
        if filters:
            for filter in filters:
                if type(filter) is bool:
                    filter_query.extend(cls._create_text_entry_response_filter())
                elif type(filter) is list:
                    filter_query.extend(cls._create_score_filter(filter))
        return filter_query

    @staticmethod
    def _create_text_entry_response_filter():
        return [Feedback.comment != None]

    @staticmethod
    def _create_score_filter(filter):
        return [Feedback.score.in_(filter)]
