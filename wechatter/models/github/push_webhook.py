from typing import List
from pydantic import BaseModel
from wechatter.models.github.base import Author, Committer, User, Pusher, Repository


class Commit(BaseModel):
    id: str
    message: str
    timestamp: str
    url: str
    author: Author
    committer: Committer
    added: List[str]
    removed: List[str]
    modified: List[str]


class GithubPushWebhook(BaseModel):
    ref: str
    repository: Repository
    pusher: Pusher
    sender: User
    forced: bool
    commits: List[Commit]
