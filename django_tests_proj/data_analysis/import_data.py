import pandas as pd
from django.contrib.auth.models import User
from data_analysis.models import BehaviorADC

csv_file_path = "./data_analysis/data/behavior_ADC.csv"
df = pd.read_csv(csv_file_path, sep=";")


for index, row in df.iterrows():
    behaviorADC = BehaviorADC(
        date = row["Date"],
        tournament = row["Tournament"],
        matchId = row["MatchId"],
        summonnerName = row["SummonnerName"],
        seriesId = row["SeriesId"],
        xpd15 = row["XPD@15"],
        gd15 = row["GD@15"],
        csMin = row["CS/Min"],
        kills = row["Kills"],
        deaths = row["Deaths"],
        assists = row["Assists"],
        kp = row["KP%"],
        dpm = row["Damage/Min"],
        jungleProximity = row["JungleProximity"],
        botLanePresence = row["botLanePresence"],
        riverBotPresence = row["riverBotPresence"],
    )
    behaviorADC.save()

print("CSV data has been loaded into the Django database.")