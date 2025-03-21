from app import ma

class StatsSchema(ma.Schema):
    class Meta:
        fields = ('kills', 'deaths', 'assists', 'wins', 'losses', 'rank', 'user_id', 'user')

stats_schema = StatsSchema()
statss_schema = StatsSchema(many=True)