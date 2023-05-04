from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

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
    URL = 'https://hs-consumer-api.espncricinfo.com/v1/pages/matches/live?lang=en'
    TEAM_KEYWORDS = ['INDIA', 'SA', 'AUS', 'PAK', 'NZ', 'ENG', 'BAN', 'WI', 'MI', 'RCB', 'CSK', 'PBKS', 'LSG',
                     'KKR']  # short_name

    def _fetch_and_parse(self):
        resp = req.get(CricketScores.URL)
        if not self.validate_response(resp, self.response_callback):
            raise Exception

        return self._process_data(self.data['matches'])

    def _process_data(self, matches):
        self._set_random_match(matches)
        # individual_scores = self._get_individual_scores(self.match)
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

        batting_score, bowling_score = '{} in {}'.format(batting_team['score'], batting_team['scoreInfo']), \
            bowling_team['score']
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
    URL = 'https://www.fotmob.com/api/matches'
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
    TZ = ZoneInfo('America/Los_Angeles')

    def __init__(self):
        dt = datetime.now(tz=SoccerScores.TZ) + timedelta(days=random.randint(-1, 3))
        resp = req.get(SoccerScores.URL, params={'date': dt.strftime('%Y%m%d'), 'timezone': SoccerScores.TZ.key})
        self.matches = self.validate_response(resp, self.response_callback)

    def get_display_string(self):
        try:
            return self._get_fixtures()
        except:
            return SoccerScores.DEFAULT_SCORELINE

    def _get_fixtures(self):
        self.match = random.choice(self.matches)
        home_team, away_team = self.match['home']['name'], self.match['away']['name']

        return '{} {} {} || {}'.format(home_team, self._get_match_score(), away_team, self._get_match_status())

    def _get_match_score(self):
        match_status = self.match['status']
        if not match_status.get('started', False):
            return "vs."

        return match_status['scoreStr']

    def _get_match_status(self):
        match_status = self.match['status']
        if match_status.get('finished'):
            return 'FT'
        if match_status.get('liveTime'):
            return match_status['liveTime']['short']
        utc_time = match_status['utcTime'].replace('Z', '+00:00')  # "2023-05-03T19:00:00.000Z"
        start_time = datetime.fromisoformat(utc_time)
        local_time = start_time.astimezone(SoccerScores.TZ)
        return local_time.strftime('%I:%M %p')

    def validate_response(self, response, callback):
        return super(SoccerScores, self).validate_response(response, callback)

    def response_callback(self, data):
        matches = []
        for league in data['leagues']:
            if league['id'] in SoccerScores.COMPETITIONS.keys():
                for match in league['matches']:
                    for k in ['home', 'away']:
                        if match[k]['id'] in SoccerScores.TEAMS.keys():
                            matches.append(match)
        return matches


if __name__ == '__main__':
    if random.randint(1, 100) < 10:
        score = CricketScores()
    else:
        score = SoccerScores()
    score_display = score.get_display_string()

    if not score_display:
        print('A.R.S.E.N.A.L')
    else:
        print(score_display)
