from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import requests as req

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
                     'KKR', 'GT', 'AFG', 'CAN']  # short_name

    def __init__(self):
        resp = req.get(CricketScores.URL, headers={"User-Agent": "Mozilla/5.0"})
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
        return filtered_matches.values()

    def response_callback(self, data):
        self.data = data['content']
        return len(self.data['matches']) > 0

    def get_score_ticker(self) -> list[str]:
        ticker = []
        for match in self.matches:
            ticker.append(self._get_display_score(match))
        if not ticker:
            ticker.append("No live cricket matches!!")
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
        6603: 'SJC Quakes',
        6708: 'Netherlands',
        6723: 'France',
        8204: 'Italy',
        6720: 'Spain',
        8491: 'England',
        8256: 'Brazil'
    }

    def __init__(self):
        self.matches = []
        for day in range(0, 4):
            dt = datetime.now(tz=TZ) + timedelta(days=day)
            resp = req.get(SoccerScores.URL + 'matches', params={'date': dt.strftime('%Y%m%d'), 'timezone': TZ.key})
            self.matches.extend(self.validate_response(resp, SoccerScores.response_callback))

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

    @staticmethod
    def response_callback(data):
        matches = []
        for league in data['leagues']:
            for match in league['matches']:
                if any(map(lambda x: match[x].get('id') in SoccerScores.TEAMS.keys(), ['home', 'away'])):
                    matches.append(match)
        return matches


class MotoGP(ScoresAbstract):
    URL = 'https://api.motogp.pulselive.com/motogp/v1/events?seasonYear={year}'
    NOW = datetime.now(tz=TZ)

    def __init__(self):
        resp = req.get(MotoGP.URL.format(year=MotoGP.NOW.year))
        self.event = self.validate_response(resp, MotoGP.response_callback)

    @staticmethod
    def response_callback(data):
        events_by_date = []
        for d in data:
            start_time = datetime.strptime(d['date_start'], '%Y-%m-%dT%H:%M:%S%z')  # "2023-05-13T10:50:00+0200"
            events_by_date.append((start_time, d))
            local_start_time = start_time.astimezone(TZ)
            if MotoGP.NOW < local_start_time and d['broadcasts']:
                return d

        return {
            'name': 'No MotoGP Race info',
        }

    def get_score_ticker(self) -> list[str]:
        event_name = self.event['name']
        ticker = []
        for b in self.event.get('broadcasts'):
            if b['kind'] in ['QUALIFYING', 'RACE'] and b['category']['acronym'] == 'MGP':
                s_name = b['name']
                start_time = datetime.strptime(b['date_start'], '%Y-%m-%dT%H:%M:%S%z')  # "2023-05-13T10:50:00+0200"
                local_time = start_time.astimezone(TZ)
                ts = local_time.strftime('%b %d %I:%M %p')
                ticker.append(f'{event_name} || {s_name} || {ts}')
        if not ticker:
            ticker.append(event_name)
        return ticker


if __name__ == '__main__':
    score = CricketScores()
    # score = SoccerScores()
    # score = MotoGP()
    score_display = score.get_score_ticker()

    if not score_display:
        print('A.R.S.E.N.A.L')
    else:
        print(score_display)
