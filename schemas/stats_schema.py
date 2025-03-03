from app import ma

class StatsSchema(ma.Schema):
    class Meta:
        fields = ('kills', 'deaths', 'assists', 'wins', 'losses', 'rank', 'user_id', 'user')

profile_schema = StatsSchema()
profiles_schema = StatsSchema(many=True)