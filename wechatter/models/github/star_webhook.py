from pydantic import BaseModel
from wechatter.models.github.base import User, Repository


class GithubStarWebhook(BaseModel):
    action: str
    repository: Repository
    sender: User
