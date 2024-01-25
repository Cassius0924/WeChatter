from typing import Optional
from pydantic import BaseModel
from wechatter.models.github.base import User, Repository


class PrRepository(Repository):
    allow_squash_merge: bool
    allow_merge_commit: bool
    allow_rebase_merge: bool
    allow_auto_merge: bool
    delete_branch_on_merge: bool
    allow_update_branch: bool
    use_squash_pr_title_as_default: bool
    squash_merge_commit_message: str
    squash_merge_commit_title: str
    merge_commit_message: str
    merge_commit_title: str


class PrBranch(BaseModel):
    label: str
    ref: str
    sha: str
    user: User
    repo: PrRepository


class PullRequest(BaseModel):
    html_url: str
    issue_url: str
    number: int
    state: str
    title: str
    user: User
    body: Optional[str]
    base: PrBranch
    head: PrBranch
    merged: bool
    merged_by: Optional[User]


class GithubPrWebhook(BaseModel):
    action: str
    number: int
    pull_request: PullRequest
    repository: Repository
    sender: User
