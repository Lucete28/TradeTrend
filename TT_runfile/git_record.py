import requests
import pandas as pd
from airflow.models.variable import Variable

git_token = Variable.get("git_token")
df7 = pd.read_csv("/opt/airflow/src/005930/005930_Accuracy_7.csv")
df30 = pd.read_csv("/opt/airflow/src/005930/005930_Accuracy_30.csv")
table7 = df7.to_markdown(index=False)
table30 = df30.to_markdown(index=False)

def create_github_issue_comment(repo_owner, repo_name, issue_number, body):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{issue_number}/comments"
    headers = {
        "Authorization": f"Bearer {git_token}",
        "Accept": "application/vnd.github+json"
    }
    payload = {
        "body": body
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 201:
        print("Comment created successfully!")
    else:
        print(f"Failed to create comment. Response: {response.json()}")



# 사용 예시
repo_owner = "Lucete28"
repo_name = "TradeTrend"
issue_number = 10
body = f"7day \n\n{table7} \n\n---\n\n30day \n\n{table30}"

create_github_issue_comment(repo_owner, repo_name, issue_number, body)
