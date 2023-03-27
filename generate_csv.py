import pandas as pd
from github import Github
import os

g = Github(os.getenv('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'))

repo = g.get_repo("saahilpratap/testreport")

pull_requests = repo.get_pulls(state="all")

pull_request_data = pd.DataFrame(columns=["Raise Date", "Closed Date", "Number", "PR Title", "State", "Source Branch", "Target Branch", "Mergeable", "Merged By", "PR Created By", "Reviewer", "Commits", "Additions", "Deletions", "Changed Files",])

for pull_request in pull_requests:
    pull_request_data = pd.concat([
        pull_request_data, 
        pd.DataFrame({
            "Raise Date": pull_request.created_at,"Closed Date": pull_request.closed_at,"Number": pull_request.number,"PR Title": pull_request.title,"State": pull_request.state,"Source Branch": pull_request.head.ref,"Target Branch": pull_request.base.ref,"Mergeable": pull_request.mergeable,"Merged By": pull_request.merged_by.login if pull_request.merged_by else None,"PR Created By": pull_request.user.login,"Reviewer": [", ".join([reviewer.login for reviewer in pull_request.requested_reviewers])],"Commits": pull_request.commits,"Additions": pull_request.additions,"Deletions": pull_request.deletions,"Changed Files": pull_request.changed_files, }, index=[0])], ignore_index=True)
        
pull_request_data["Rebase Status"] = ""

pull_request_data.loc[pull_request_data["Mergeable"] == True, "Rebase Status"] = "Rebased"
pull_request_data.loc[pull_request_data["Mergeable"] == False, "Rebase Status"] = "Not Rebasing"

pull_request_data.to_csv("yup.csv", index=False)
