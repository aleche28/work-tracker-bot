import requests
import os
from dotenv import load_dotenv
from collections import defaultdict 

def get_time_spent_per_user():
    load_dotenv()

    auth_token = os.getenv("YOUTRACK_PERM_TOKEN")

    headers = {}
    headers['Authorization'] = f'Bearer {auth_token}'

    api_url = os.getenv("YOUTRACK_API_URL")
    project = os.getenv("YOUTRACK_PROJECT")
    entity = "workItems"
    fields = "creator(name),duration(minutes)"
    query = f"project:{project}"
    
    req_url = f'{api_url}/{entity}?fields={fields}&query={query}'
    
    response = requests.get(req_url, headers=headers).json()

    time_map = defaultdict(int)
    for work_item in response:
        user = work_item["creator"]["name"]
        time_spent = work_item["duration"]["minutes"]
        time_map[user] += time_spent
    
    time_map_sorted = sorted(time_map, key=lambda u: time_map[u], reverse=True)

    ranking = "`Time spent per team member`\n\n"
    for user in time_map_sorted:
        time_spent = time_map[user]
        hours = time_spent // 60
        minutes = time_spent % 60
        ranking += f'`{user}:'.ljust(20, ' ') + f'{hours}h {str(minutes).zfill(2)}m`\n'

    return ranking


if __name__ == "__main__":
    print(get_time_spent_per_user())