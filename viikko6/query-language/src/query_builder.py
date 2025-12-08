import matchers

class QueryBuilder:
    def __init__(self, matcher=matchers.All()):
        self.matcher = matcher

    def plays_in(self, team):
        return QueryBuilder(matchers.And(self.matcher, matchers.PlaysIn(team)))

    def has_at_least(self, value, attr):
        return QueryBuilder(matchers.And(self.matcher, matchers.HasAtLeast(value, attr)))

    def has_fewer_than(self, value, attr):
        return QueryBuilder(matchers.And(self.matcher, matchers.HasFewerThan(value, attr)))

    def build(self):
        return self.matcher
