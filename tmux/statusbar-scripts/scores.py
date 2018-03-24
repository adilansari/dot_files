from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta

import requests as req
import random


class ScoresAbstract:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_display_string(self):
        pass

    @abstractmethod
    def validate_response(self, response, callback):
        data = {}
        if response.status_code == req.codes.ok:
            data = response.json()

        return callback(data)


class CricketScores(ScoresAbstract):
    URL = 'http://www.cricbuzz.com/match-api/livematches.json'
    SERIES_KEYWORDS = ['IND', 'RSA', 'AUS', 'PAK', 'NZ', 'ENG', 'IPL']  # short_name

    def _fetch_and_parse(self):
        resp = req.get(CricketScores.URL)
        if not self.validate_response(resp, self.response_callback):
            raise Exception

        return self._process_data(self.data['matches'])

    def _process_data(self, matches):
        self._set_random_match(matches)
        batting_score, bowling_score = self._get_team_scores(self.match)
        individual_scores = self._get_individual_scores(self.match)
        return '{} | {} | {}'.format(batting_score, individual_scores, bowling_score)

    @staticmethod
    def _get_team_scores(match):
        if match['score']['batting']['id'] == match['team1']['id']:
            batting_team, bowling_team = (match['team1'], match['team2'])
        else:
            batting_team, bowling_team = (match['team2'], match['team1'])

        batting_score, bowling_score = match['score']['batting']['score'], match['score']['bowling']['score']
        batting_formatted_score = '{}: {}'.format(batting_team['s_name'], batting_score)
        bowling_formatted_score = '{}: {}'.format(bowling_team['s_name'], bowling_score)

        return batting_formatted_score, bowling_formatted_score

    @staticmethod
    def _get_individual_scores(match):
        batsmen = {}
        for player in match['players']:
            batsmen[player['id']] = player['name']

        batsmen_scores = []
        for batsman in match['score']['batsman']:
            batsmen_scores.append('{}: {}'.format(batsmen[batsman['id']], batsman['r']))

        return ', '.join(batsmen_scores)

    def _set_random_match(self, matches):
        matches = {id: match_data for id, match_data in matches.items() if self._display_this_match(match_data)}
        self.match = random.choice(matches.values())

    @staticmethod
    def _display_this_match(match):
        keys = filter(lambda key: key in match['series']['short_name'], CricketScores.SERIES_KEYWORDS)
        return bool(keys) and 'score' in match  # needs to be a live match

    def validate_response(self, response, callback):
        return super(CricketScores, self).validate_response(response, callback)

    def response_callback(self, data):
        self.data = data
        return len(data['matches']) > 0

    def get_display_string(self):
        return self._fetch_and_parse()


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
            if match['match_localteam_name'].lower() == SoccerScores.TEAM or match[
                'match_visitorteam_name'].lower() == SoccerScores.TEAM:
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
    cricket_score = CricketScores()
    score_display = cricket_score.get_display_string()

    print score_display
