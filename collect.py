import requests
import json
import os
from datetime import datetime

TOPICS = [
    "artificial-intelligence",
    "llm",
    "agents",
    "machine-learning",
    "rag"
]

all_repos = []

for topic in TOPICS:
    url = f"https://api.github.com/search/repositories?q=topic:{topic}&sort=stars&order=desc&per_page=20"

    try:
        response = requests.get(url, timeout=30)

        if response.status_code != 200:
            print(f"Failed topic: {topic}")
            continue

        data = response.json()

        for repo in data.get("items", []):
            all_repos.append({
                "topic": topic,
                "name": repo["name"],
                "full_name": repo["full_name"],
                "description": repo["description"],
                "stars": repo["stargazers_count"],
                "language": repo["language"],
                "url": repo["html_url"],
                "updated_at": repo["updated_at"]
            })

    except Exception as e:
        print(f"Error collecting {topic}: {e}")

# Remove duplicates
unique = {}

for repo in all_repos:
    unique[repo["full_name"]] = repo

dataset = list(unique.values())

dataset.sort(
    key=lambda x: x["stars"],
    reverse=True
)

os.makedirs("datasets", exist_ok=True)

output = {
    "generated_at": datetime.utcnow().isoformat(),
    "repository_count": len(dataset),
    "repositories": dataset
}

with open(
    "datasets/txb-index.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        output,
        f,
        indent=2,
        ensure_ascii=False
    )

print(f"Collected {len(dataset)} repositories")
print("Saved datasets/txb-index.json")
