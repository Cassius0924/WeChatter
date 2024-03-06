from pydantic import BaseModel

from wechatter.models.github.base import Repository, User


class Release(BaseModel):
    url: str
    assets_url: str
    upload_url: str
    html_url: str
    author: User
    body: str
    tag_name: str
    target_commitish: str
    name: str
    draft: bool
    prerelease: bool
    created_at: str
    published_at: str
    id: int


class GithubReleaseWebhook(BaseModel):
    action: str
    release: Release
    repository: Repository
    sender: User
