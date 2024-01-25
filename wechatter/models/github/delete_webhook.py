from pydantic import BaseModel
from wechatter.models.github.base import User, Repository


class GithubDeleteWebhook(BaseModel):
    ref: str
    ref_type: str
    pusher_type: str
    repository: Repository
    sender: User
