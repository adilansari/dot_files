# -*- coding: utf-8 -*-
import requests as req
from datetime import datetime, timedelta
from sys import argv

"""
supports only premier league on free tier
will look if any matches inpast 2 days for 'ARSENAL' and return scoreline
else will find any fixtures in next 7 days

args = API_KEY from football-api.com
Sample request: http://football-api.com/api/?Action=fixtures&APIKey={}&comp_id={}&match_date={}
"""


class SoccerScores:

    COMP_ID = 1204
    TEAM = 'arsenal'
    URL = 'http://football-api.com/api'
    DEFAULT_SCORELINE = 'A.R.S.E.N.A.L'

    def __init__(self, _api_key):
        self._api_key = _api_key

    def get_display_string(self):
        try:
            return self._get_fixtures(self._get_date(-3), self._get_date(5))
        except Exception as e:
            print e.message
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

        if not self._validate_response(resp):
            raise Exception

        matches = resp.json().get('matches')
        for match in matches:
            if match['match_localteam_name'].lower() == SoccerScores.TEAM or match['match_visitorteam_name'].lower() == SoccerScores.TEAM:
                return self._process_data(match)

    def _validate_response(self, r):
        data = {}
        if r.status_code == req.codes.ok:
            data = r.json()
        return data.get("ERROR") == "OK"

    def _process_data(self, match_data):
        return '[{}] {} {}-{} {} ({})'.format(
            match_data['match_date'],
            match_data['match_localteam_name'],
            match_data['match_localteam_score'],
            match_data['match_visitorteam_score'],
            match_data['match_visitorteam_name'],
            match_data['match_status'])

if __name__ == '__main__':
    obj = SoccerScores(argv[1])
    print obj.get_display_string()
