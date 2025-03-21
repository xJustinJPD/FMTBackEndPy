from app import ma

class MatchSchema(ma.Schema):
    class Meta:
        fields = ('id', 'liker_id', 'liked_id', 'status', 'timestamp', 'liker', 'liked')

match_schema = MatchSchema()
matchess_schema = MatchSchema(many=True)