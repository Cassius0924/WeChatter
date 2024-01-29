from pydantic import BaseModel

from wechatter.models.github.base import Reactions, Repository, User


class Issue(BaseModel):
    html_url: str
    number: int
    title: str
    user: User
    state: str
    reactions: Reactions


class GithubIssueWebhook(BaseModel):
    action: str
    issue: Issue
    repository: Repository
    sender: User
