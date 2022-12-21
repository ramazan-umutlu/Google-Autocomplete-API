import string
import requests
import pandas as pd
import json
from pathlib import Path
from fake_useragent import UserAgent
from collections import OrderedDict
import timeit

start = timeit.default_timer()


keyword = "your keyword"
language = "en"


def get_random_user_agent():
    ua = UserAgent()
    return ua.random

def auto_complete_collector(query, lang):
    results = []
    headers = {
        "User-Agent": get_random_user_agent()
    }
    params = {
        "q": query,
        "gl": lang,
        "hl": lang,
        "client": "chrome"
    }
    with requests.Session() as session:
        adapter = requests.adapters.HTTPAdapter(max_retries=3)
        session.mount("http://", adapter)
        response = session.get("http://google.com/complete/search", params=params, headers=headers)
        for result in json.loads(response.text, object_pairs_hook=OrderedDict)[1]:
            results.append(result)
            print(result)
    return results


results = []
for letter in string.ascii_lowercase:
    query = f"{keyword} {letter}"
    print(query)
    results.extend(auto_complete_collector(query, language))

df = pd.DataFrame({"Autocomplete": results})
df = df.drop_duplicates()
output_file = Path(f"{keyword}_{language}.xlsx")
with pd.ExcelWriter(output_file) as writer:
    df.to_excel(writer, sheet_name="sheet", index=False)
stop = timeit.default_timer()
print('Time: ', stop - start)  
