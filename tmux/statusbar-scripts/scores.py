from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import requests as req
import random

TZ = ZoneInfo('America/Los_Angeles')


class ScoresAbstract:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_score_ticker(self) -> list[str]:
        pass

    @abstractmethod
    def validate_response(self, response, callback):
        data = {}
        if response.status_code == req.codes.ok:
            data = response.json()

        return callback(data)


class CricketScores(ScoresAbstract):
    URL = 'https://hs-consumer-api.espncricinfo.com/v1/pages/matches/live?lang=en'
    TEAM_KEYWORDS = ['INDIA', 'SA', 'AUS', 'PAK', 'NZ', 'ENG', 'BAN', 'WI', 'MI', 'RCB', 'CSK', 'PBKS', 'LSG',
                     'KKR']  # short_name

    def __init__(self):
        resp = req.get(CricketScores.URL)
        if not self.validate_response(resp, self.response_callback):
            raise Exception
        self.matches = self._filtered_matches(self.data['matches'])

    def _get_display_score(self, match):
        return '{} || {}'.format(self._get_team_display(match), self._get_score_text(match))

    @staticmethod
    def _get_score_text(match):
        if match['stage'] == 'RUNNING' and match['state'] == 'LIVE':
            return CricketScores._get_team_scores(match)
        else:
            utc_time = match['startTime'].replace('Z', '+00:00')  # "2023-05-03T19:00:00.000Z"
            start_time = datetime.fromisoformat(utc_time)
            local_time = start_time.astimezone(TZ)
            return local_time.strftime('%a %I:%M %p')

    @staticmethod
    def _get_team_display(match):
        t1, t2 = match['teams'][0]['team'], match['teams'][1]['team']
        return '{} vs {} {}'.format(t1['abbreviation'], t2['abbreviation'], match['format'])

    @staticmethod
    def _get_team_scores(match):
        team1, team2 = match['teams'][0], match['teams'][1]

        if team1['isLive']:
            batting_team, bowling_team = team1, team2
        elif team2['isLive']:
            batting_team, bowling_team = team2, team1
        else:
            return 'AlgorithmError: No teams live'

        batting_score, bowling_score = '{} in {}'.format(batting_team['score'], batting_team['scoreInfo']), \
            bowling_team['score']
        batting_formatted_score = '{}: {}'.format(batting_team['team']['abbreviation'], batting_score)
        bowling_formatted_score = '{}: {}'.format(bowling_team['team']['abbreviation'], bowling_score)

        return '{} | {}'.format(batting_formatted_score, bowling_formatted_score)

    def _filtered_matches(self, matches):
        filtered_matches = dict()
        for m in matches:
            for t in m['teams']:
                if t['team']['abbreviation'] in self.TEAM_KEYWORDS:
                    filtered_matches[m['id']] = m
        if not filtered_matches:
            return 'No live Cricket matches'
        return filtered_matches.values()

    def validate_response(self, response, callback):
        return super(CricketScores, self).validate_response(response, callback)

    def response_callback(self, data):
        self.data = data['content']
        return len(self.data['matches']) > 0

    def get_score_ticker(self) -> list[str]:
        ticker = []
        for match in self.matches:
            ticker.append(self._get_display_score(match))
        return ticker


class SoccerScores(ScoresAbstract):
    """
    Register at http://football-data.org/ for API key
    """
    URL = 'https://www.fotmob.com/api/'
    DEFAULT_SCORELINE = 'A.R.S.E.N.A.L'
    TEAMS = {
        9825: 'Arsenal',
        8455: 'Chelsea',
        8456: 'Man City',
        10260: 'Man Utd',
        8586: 'Tottenham',
        8650: 'Liverpool',
        8634: 'Barcelona',
        8633: 'Real Madrid',
        9885: 'Juventus',
        9847: 'PSG',
        9823: 'Bayern',
        6603: 'SJC Quakes'
    }
    COMPETITIONS = {
        47: 'Premier League',
        87: 'Spanish La Liga',
        53: 'French Ligue 1',
        55: 'Serie A',
        42: 'Champions League',
        54: 'Bundesliga',
        10000002: 'MLS'
    }

    def __init__(self):
        dt = datetime.now(tz=TZ)
        resp = req.get(SoccerScores.URL + 'matches', params={'date': dt.strftime('%Y%m%d'), 'timezone': TZ.key})
        self.matches = self.validate_response(resp, SoccerScores.response_callback) or []
        if not self.matches:
            for team_id in SoccerScores.TEAMS.keys():
                resp = req.get(SoccerScores.URL + 'teams', params={'id': team_id}).json()
                self.matches.append(resp['fixtures']['allFixtures']['nextMatch'])

    def get_score_ticker(self) -> list[str]:
        ticker = []
        for match in self.matches:
            try:
                home_team, away_team = match['home']['name'], match['away']['name']
                t = '{} {} {} || {}'.format(home_team, self._get_match_score(match), away_team,
                                            self._get_match_status(match))
                ticker.append(t)
            except:
                ticker.append(SoccerScores.DEFAULT_SCORELINE)
        return ticker

    @staticmethod
    def _get_match_score(match):
        match_status = match['status']
        if not match_status.get('started', False):
            return "vs."

        return match_status['scoreStr']

    @staticmethod
    def _get_match_status(match):
        match_status = match['status']
        if match_status.get('finished'):
            return 'FT'
        if match_status.get('liveTime'):
            return match_status['liveTime']['short']
        utc_time = match_status['utcTime'].replace('Z', '+00:00')  # "2023-05-03T19:00:00.000Z"
        start_time = datetime.fromisoformat(utc_time)
        local_time = start_time.astimezone(TZ)
        return local_time.strftime('%a %I:%M %p')

    def validate_response(self, response, callback):
        return super(SoccerScores, self).validate_response(response, callback)

    @staticmethod
    def response_callback(data):
        matches = []
        for league in data['leagues']:
            if any(map(lambda x: league.get(x) in SoccerScores.COMPETITIONS.keys(), ['id', 'primaryId'])):
                for match in league['matches']:
                    if any(map(lambda x: match[x].get('id') in SoccerScores.TEAMS.keys(), ['home', 'away'])):
                        matches.append(match)
        return matches


if __name__ == '__main__':
    if random.randint(1, 100) < 30:
        score = CricketScores()
    else:
        score = SoccerScores()
    score_display = score.get_score_ticker()

    if not score_display:
        print('A.R.S.E.N.A.L')
    else:
        print(score_display)
