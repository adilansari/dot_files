import json
import requests as req

match_id = "186881"
URL = "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20cricket.scorecard.summary%20where%20match_id%3D{}&format=json&diagnostics=false&env=store%3A%2F%2F0TxIGQMQbObzvU4Apia0V0&callback=".format(match_id)
resp = req.get(URL)
scorecard = resp.json()["query"]["results"]["Scorecard"]
t1 = scorecard["teams"][0]["sn"]
t2 = scorecard["teams"][1]["sn"]

t1_run = scorecard["past_ings"]["s"]["a"]["r"]
t1_over = scorecard["past_ings"]["s"]["a"]["o"]
t1_wicket = scorecard["past_ings"]["s"]["a"]["w"]

p1_name = scorecard["past_ings"]["d"]["a"]["t"][0]["name"]
p1_run = scorecard["past_ings"]["d"]["a"]["t"][0]["r"]

p2_name = scorecard["past_ings"]["d"]["a"]["t"][1]["name"]
p2_run = scorecard["past_ings"]["d"]["a"]["t"][1]["r"]

print("{}:{}/{} {} ovrs || {}:{}, {}:{} || {}").format(t1, t1_run, t1_wicket, t1_over, p1_name,
        p1_run, p2_name, p2_run, t2)

