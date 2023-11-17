import requests
from dotenv import load_dotenv
import os

def get_github_repo_stats():
    baseAPIUrl = "https://api.github.com/repos"
    load_dotenv()
    repoAPIUrl = baseAPIUrl +  os.getenv("GITHUB_REPO_URL")
    access_token = os.getenv("GITHUB_ACCESS_TOKEN")

    headers = {}
    headers['Authorization'] = f'Token {access_token}'

    # Get contributors and their commit count
    contributors_url = f'{repoAPIUrl}/contributors'
    contributors_data = requests.get(contributors_url, headers=headers).json()

    #? maybe useless, it seems like they are already returned in descending order by num of contributions
    contributors_data = sorted(contributors_data, key=lambda x: x["contributions"], reverse=True)
    
    markdownString = "`Commits per contributor`\n\n"
    for i, contributor in enumerate(contributors_data):
        contributor_name = contributor["login"]
        contributor_commits = contributor["contributions"]
        medal = "  "
        if i == 0:
            medal = "🥇"
        elif i == 1:
            medal = "🥈"
        elif i == 2:
            medal = "🥉"
        markdownString += f"`{medal}" + f"{contributor_name}:".ljust(20) + f"{contributor_commits}`\n"

    return markdownString

if __name__ == "__main__":
    print(get_github_repo_stats())
