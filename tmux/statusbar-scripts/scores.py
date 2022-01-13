from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta

import requests as req
import random
import pytz
import sys


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
    URL = 'https://hs-consumer-api.espncricinfo.com/v1/pages/matches/live?lang=en'
    TEAM_KEYWORDS = ['INDIA', 'SA', 'AUS', 'PAK', 'NZ', 'ENG', 'BAN', 'WI', 'MI', 'RCB', 'CSK', 'PBKS']  # short_name

    def _fetch_and_parse(self):
        resp = req.get(CricketScores.URL)
        if not self.validate_response(resp, self.response_callback):
            raise Exception

        return self._process_data(self.data['matches'])

    def _process_data(self, matches):
        self._set_random_match(matches)
        #individual_scores = self._get_individual_scores(self.match)
        return '{} || {}'.format(self._get_team_display(), self._get_score_text())

    def _get_score_text(self):
        if self.match['stage'] == 'RUNNING' and self.match['state'] == 'LIVE':
            return self._get_team_scores(self.match)
        else:
            return self.match['statusText']

    def _get_team_display(self):
        t1, t2 = self.match['teams'][0]['team'], self.match['teams'][1]['team']
        return '{} vs {} {}'.format(t1['abbreviation'], t2['abbreviation'], self.match['format'])

    @staticmethod
    def _get_team_scores(match):
        team1, team2 = match['teams'][0], match['teams'][1]

        if team1['isLive']:
            batting_team, bowling_team = team1, team2
        elif team2['isLive']:
            batting_team, bowling_team = team2, team1
        else:
            return 'AlgorithmError: No teams live'

        batting_score, bowling_score = '{} in {}'.format(batting_team['score'], batting_team['scoreInfo']), bowling_team['score']
        batting_formatted_score = '{}: {}'.format(batting_team['team']['abbreviation'], batting_score)
        bowling_formatted_score = '{}: {}'.format(bowling_team['team']['abbreviation'], bowling_score)

        return '{} | {}'.format(batting_formatted_score, bowling_formatted_score)

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
        filtered_matches = dict()
        for m in matches:
            for t in m['teams']:
                if t['team']['abbreviation'] in self.TEAM_KEYWORDS:
                    filtered_matches[m['id']] = m
        if not filtered_matches:
            return 'No live Cricket matches'
        self.match = random.choice(list(filtered_matches.values()))

    def validate_response(self, response, callback):
        return super(CricketScores, self).validate_response(response, callback)

    def response_callback(self, data):
        self.data = data['content']
        return len(self.data['matches']) > 0

    def get_display_string(self):
        return self._fetch_and_parse()


class SoccerScores(ScoresAbstract):
    """
    Register at http://football-data.org/ for API key
    """

    URL = 'http://api.football-data.org/v2/matches'
    DEFAULT_SCORELINE = 'A.R.S.E.N.A.L'
    TEAMS = {
        57: 'Arsenal',
        61: 'Chelsea',
        65: 'ManCity',
        66: 'ManUtd',
        73: 'Tottenham',
        81: 'Barcelona',
        86: 'Real Madrid',
        119: 'Juventus',
        524: 'PSG',
        232: 'Bayern',
    }
    COMPETITIONS = {
        'Premier League': '2021',
        'Bundesliga': '2002',
        'Italian Serie A': '2019',
        'Champions League': '2001',
        'Europa League': '2046',
    }

    def __init__(self, _api_key):
        self.headers = {'X-Auth-Token': _api_key, 'X-Response-Control': 'minified'}

    def get_display_string(self):
        try:
            return self._get_fixtures()
        except:
            return SoccerScores.DEFAULT_SCORELINE

    def _get_fixtures(self):
        start_date, end_date = self.get_start_end_dates()
        payload= {
            'dateFrom': start_date,
            'dateTo': end_date,
            'competitions': ','.join(SoccerScores.COMPETITIONS.values())
        }

        resp = req.get(SoccerScores.URL, params=payload, headers=self.headers)
        matches = filter(SoccerScores._matches_filter, self.validate_response(resp, self.response_callback))
        match = random.choice(matches)
        home_team, away_team = match['homeTeam']['name'], match['awayTeam']['name']
        home_team_score, away_team_score = match['score']['fullTime']['homeTeam'] or 0, match['score']['fullTime'][
            'awayTeam'] or 0
        fixture_date = self.get_pdt_date(match['utcDate'])

        return '{}  {}:{}  {} || {}'.format(home_team, home_team_score, away_team_score, away_team, fixture_date)

    @staticmethod
    def _matches_filter(match):
        if match['awayTeam']['id'] in SoccerScores.TEAMS.keys():
            return True
        elif match['homeTeam']['id'] in SoccerScores.TEAMS.keys():
            return True
        return False

    @staticmethod
    def get_start_end_dates():
        start_date = datetime.now() - timedelta(days=2)
        end_date = start_date + timedelta(days=8)
        return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')

    @staticmethod
    def get_pdt_date(date_string):
        dt = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.utc)
        return dt.astimezone(pytz.timezone('US/Pacific')).strftime('%Y-%m-%d %H:%M:%S %Z')

    def validate_response(self, response, callback):
        return super(SoccerScores, self).validate_response(response, callback)

    def response_callback(self, data):
        return data['matches']


if __name__ == '__main__':
    # if random.randint(1, 2) == 1:
    score = CricketScores()
    # else:
    #     score = SoccerScores(sys.argv[1])
    # score = SoccerScores(sys.argv[1])
    score_display = score.get_display_string()

    if not score_display:
        print('A.R.S.E.N.A.L')
    else:
        print(score_display)
