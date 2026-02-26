import csv
from pathlib import Path
import re

from bs4 import BeautifulSoup as bs
import requests

URL = "https://scale-player.vercel.app/scale_type"
PAT = re.compile(r"([\d]){1,2}")

res = requests.get(URL)

soup = bs(res.content, "html.parser")

h3_tags = soup.find_all("h3")
scales = []
for h3 in h3_tags:
    try:
        scales.append(h3["id"])
    except KeyError:
        pass

with Path("../data/scales.csv").open("w") as f:
    fieldnames = ("idx", "scaleName", "notes")
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    idx = 1
    for scale in scales:
        h3 = soup.find("h3", id=scale)
        parent = h3.parent
        dl = parent.css.select("dl > dd")
        for elem in dl:
            detail = elem.find("p").get_text("\n").split("\n")[0]
            notes = detail.replace("構成音：", "")
            notes_list = [int(note) for note in notes.split(",")]
            semitones  = [note - 1 for note in notes_list]
            scale_name = elem.find("img")["alt"]
            scale_name = scale_name.replace("-1", "")
            writer.writerow({
                "idx": f"{idx:02d}",
                "scaleName": scale_name,
                "notes": ",".join(str(semitone) for semitone in semitones)
            })
            idx += 1
