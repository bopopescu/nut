from applications.schema import ma
from applications.models.searchhistory import SearchHistory


class SearchHistorySchema(ma.ModelSchema):

    class Meta:
        model           = SearchHistory
        fields          = ['user_id', 'keyword', 'user_agent', 'created_at']