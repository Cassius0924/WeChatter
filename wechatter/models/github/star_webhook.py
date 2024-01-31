from pydantic import BaseModel

from wechatter.models.github.base import Repository, User


class GithubStarWebhook(BaseModel):
    action: str
    repository: Repository
    sender: User
