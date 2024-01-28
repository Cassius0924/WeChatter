from pydantic import BaseModel

from wechatter.models.github.base import Repository, User


class Hook(BaseModel):
    type: str


class GithubPingWebhook(BaseModel):
    zen: str
    hook: Hook
    repository: Repository
    sender: User
