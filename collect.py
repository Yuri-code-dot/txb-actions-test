import requests

url = "https://api.github.com/search/repositories?q=topic:artificial-intelligence&sort=stars&order=desc&per_page=10"

response = requests.get(url)
data = response.json()

print("Top AI Repositories:")

for repo in data["items"]:
    print(f"- {repo['full_name']} ({repo['stargazers_count']} stars)")
