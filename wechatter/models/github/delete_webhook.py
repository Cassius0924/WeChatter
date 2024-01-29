from pydantic import BaseModel

from wechatter.models.github.base import Repository, User


class GithubDeleteWebhook(BaseModel):
    ref: str
    ref_type: str
    pusher_type: str
    repository: Repository
    sender: User
