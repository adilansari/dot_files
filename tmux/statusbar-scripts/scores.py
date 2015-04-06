from abc import ABCMeta, abstractmethod
import requests as req
from datetime import datetime, timedelta
from sys import argv
import traceback


class ScoresAbstract:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_display_string(self):
        pass

    @abstractmethod
    def validate_response(self, request, callback):
        data = {}
        if request.status_code == req.codes.ok:
            data = request.json()

        return callback(data)


class CricketScores(ScoresAbstract):

    URL = 'https://query.yahooapis.com/v1/public/yql'

    def get_display_string(self):
        try:
            return self._fetch_and_parse()
        except:
            # print traceback.format_exc()
            return False

    def _fetch_and_parse(self):
        params = {
            'q': 'select * from cricket.scorecard.live.summary',
            'format': 'json',
            'diagnostics': 'false',
            'env': 'store://0TxIGQMQbObzvU4Apia0V0'
        }

        resp = req.get(CricketScores.URL, params=params)

        if not self.validate_response(resp):
            raise Exception

        scorecard = resp.json()['query']['results']['Scorecard']
        t1_score, t2_score, player_scores = self._process_data(scorecard)

        return '{} | {} | {}'.format(t1_score, player_scores, t2_score)

    def _process_data(self, data):
        teams = {}
        for x in [0, 1]:
            teams[data['teams'][x]['i']] = data['teams'][x]['sn']

        innings = 1
        if isinstance(data['past_ings'], list) and len(data['past_ings']) == 2:
            batting_innings = data['past_ings'][0]
            bowling_innings = data['past_ings'][1]
            innings = 2
        else:
            batting_innings = data['past_ings']

        batting_team = teams.pop(batting_innings['s']['a']['i'])
        batting_team_score = '{}:{}/{} {} ovrs'.format(
            batting_team,
            batting_innings["s"]["a"]["r"],
            batting_innings["s"]["a"]["w"],
            batting_innings["s"]["a"]["o"]
        )

        bowling_team = teams.popitem()[1]
        if innings == 2:
            bowling_team_score = '{}:{}/{}'.format(
                bowling_team,
                bowling_innings["s"]["a"]["r"],
                bowling_innings["s"]["a"]["w"]
            )
        else:
            bowling_team_score = '{}'.format(bowling_team)

        player_scores = self._get_player_scores(batting_innings)

        return batting_team_score, bowling_team_score, player_scores

    def _get_player_scores(self, data):
        p1 = '{}:{}'.format(data["d"]["a"]["t"][0]["name"], data["d"]["a"]["t"][0]["r"])
        p2 = '{}:{}'.format(data["d"]["a"]["t"][1]["name"], data["d"]["a"]["t"][1]["r"])

        return '{}, {}'.format(p1, p2)

    def validate_response(self, r):
        return super(CricketScores, self).validate_response(r, self.response_callback)

    def response_callback(self, data):
        return data['query'].get('count') > 0


class SoccerScores(ScoresAbstract):

    """
    supports only premier league on free tier
    will look if any matches inpast 2 days for 'ARSENAL' and return scoreline
    else will find any fixtures in next 7 days

    args = API_KEY from football-api.com
    Sample request: http://football-api.com/api/?Action=fixtures&APIKey={}&comp_id={}&match_date={}
    """

    COMP_ID = 1204
    TEAM = 'arsenal'
    URL = 'http://football-api.com/api'
    DEFAULT_SCORELINE = 'A.R.S.E.N.A.L'

    def __init__(self, _api_key):
        self._api_key = _api_key

    def get_display_string(self):
        try:
            return self._get_fixtures(self._get_date(-3), self._get_date(5))
        except:
            # print traceback.format_exc()
            return SoccerScores.DEFAULT_SCORELINE

    def _get_date(self, delta):
        date = datetime.now() + timedelta(days=delta)
        return date.strftime('%d.%m.%Y')

    def _get_fixtures(self, from_date, to_date):
        params = {
            'Action': 'fixtures',
            'from_date': from_date,
            'to_date': to_date,
            'APIKey': self._api_key,
            'comp_id': SoccerScores.COMP_ID
        }
        resp = req.get(SoccerScores.URL, params=params)

        if not self.validate_response(resp):
            raise Exception

        matches = resp.json().get('matches')
        for match in matches:
            if match['match_localteam_name'].lower() == SoccerScores.TEAM or match['match_visitorteam_name'].lower() == SoccerScores.TEAM:
                return self._process_data(match)

        raise Exception

    def validate_response(self, r):
        return super(SoccerScores, self).validate_response(r, self.response_callback)

    def response_callback(self, data):
        return data.get("ERROR") == "OK"

    def _process_data(self, match_data):
        return '[{}] {} {}-{} {} ({})'.format(
            match_data['match_date'],
            match_data['match_localteam_name'],
            match_data['match_localteam_score'],
            match_data['match_visitorteam_score'],
            match_data['match_visitorteam_name'],
            match_data['match_status']
        )


if __name__ == '__main__':
    obj = CricketScores().get_display_string()

    if not obj:
        arg = argv[1]
        obj = SoccerScores(arg).get_display_string()

    print obj
