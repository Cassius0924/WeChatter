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


"""
{
  "ref": "refs/heads/master",
  "repository": {
    "id": 739787387,
    "node_id": "R_kgDOLBhCew",
    "name": ".dotfiles",
    "full_name": "Cassius0924/.dotfiles",
    "private": true,
    "owner": {
      "name": "Cassius0924",
      "email": "2670226747@qq.com",
      "login": "Cassius0924",
      "id": 62874592,
      "node_id": "MDQ6VXNlcjYyODc0NTky",
      "avatar_url": "https://avatars.githubusercontent.com/u/62874592?v=4",
      "gravatar_id": "",
      "url": "https://api.github.com/users/Cassius0924",
      "html_url": "https://github.com/Cassius0924",
      "followers_url": "https://api.github.com/users/Cassius0924/followers",
      "following_url": "https://api.github.com/users/Cassius0924/following{/other_user}",
      "gists_url": "https://api.github.com/users/Cassius0924/gists{/gist_id}",
      "starred_url": "https://api.github.com/users/Cassius0924/starred{/owner}{/repo}",
      "subscriptions_url": "https://api.github.com/users/Cassius0924/subscriptions",
      "organizations_url": "https://api.github.com/users/Cassius0924/orgs",
      "repos_url": "https://api.github.com/users/Cassius0924/repos",
      "events_url": "https://api.github.com/users/Cassius0924/events{/privacy}",
      "received_events_url": "https://api.github.com/users/Cassius0924/received_events",
      "type": "User",
      "site_admin": false
    },
    "html_url": "https://github.com/Cassius0924/.dotfiles",
    "description": null,
    "fork": false,
    "url": "https://github.com/Cassius0924/.dotfiles",
    "created_at": 1704552321,
    "updated_at": "2024-01-06T14:50:57Z",
    "pushed_at": 1705905499,
    "git_url": "git://github.com/Cassius0924/.dotfiles.git",
    "ssh_url": "git@github.com:Cassius0924/.dotfiles.git",
    "clone_url": "https://github.com/Cassius0924/.dotfiles.git",
    "size": 4,
    "stargazers_count": 0,
    "watchers_count": 0,
    "language": "Lua",
    "allow_forking": true,
    "is_template": false,
    "web_commit_signoff_required": false,
    "topics": [

    ],
    "visibility": "private",
    "forks": 0,
    "open_issues": 1,
    "watchers": 0,
    "default_branch": "master",
    "stargazers": 0,
    "master_branch": "master"
  },
  "pusher": {
    "name": "Cassius0924",
    "email": "2670226747@qq.com"
  },
  "sender": {
    "login": "Cassius0924",
    "id": 62874592,
    "url": "https://api.github.com/users/Cassius0924",
    "html_url": "https://github.com/Cassius0924",
    "followers_url": "https://api.github.com/users/Cassius0924/followers",
    "following_url": "https://api.github.com/users/Cassius0924/following{/other_user}",
    "gists_url": "https://api.github.com/users/Cassius0924/gists{/gist_id}",
    "starred_url": "https://api.github.com/users/Cassius0924/starred{/owner}{/repo}",
    "subscriptions_url": "https://api.github.com/users/Cassius0924/subscriptions",
    "organizations_url": "https://api.github.com/users/Cassius0924/orgs",
    "repos_url": "https://api.github.com/users/Cassius0924/repos",
    "events_url": "https://api.github.com/users/Cassius0924/events{/privacy}",
    "received_events_url": "https://api.github.com/users/Cassius0924/received_events",
    "type": "User",
    "site_admin": false
  },
  "created": false,
  "deleted": false,
  "forced": false,
  "base_ref": null,
  "compare": "https://github.com/Cassius0924/.dotfiles/compare/ec347564b925...a4fb7a681242",
  "commits": [
    {
      "id": "a4fb7a6812424ac7d19a6c7f548d492c0bea6e85",
      "tree_id": "bf97c5f5ea3d3c0cc71a88db0225850506367480",
      "distinct": true,
      "message": "update lvim config",
      "timestamp": "2024-01-22T14:38:06+08:00",
      "url": "https://github.com/Cassius0924/.dotfiles/commit/a4fb7a6812424ac7d19a6c7f548d492c0bea6e85",
      "author": {
        "name": "Cassius0924",
        "email": "2670226747@qq.com",
        "username": "Cassius0924"
      },
      "committer": {
        "name": "Cassius0924",
        "email": "2670226747@qq.com",
        "username": "Cassius0924"
      },
      "added": [

      ],
      "removed": [

      ],
      "modified": [
        ".config/lvim/config.lua"
      ]
    }
  ],
  "head_commit": {
    "id": "a4fb7a6812424ac7d19a6c7f548d492c0bea6e85",
    "tree_id": "bf97c5f5ea3d3c0cc71a88db0225850506367480",
    "distinct": true,
    "message": "update lvim config",
    "timestamp": "2024-01-22T14:38:06+08:00",
    "url": "https://github.com/Cassius0924/.dotfiles/commit/a4fb7a6812424ac7d19a6c7f548d492c0bea6e85",
    "author": {
      "name": "Cassius0924",
      "email": "2670226747@qq.com",
      "username": "Cassius0924"
    },
    "committer": {
      "name": "Cassius0924",
      "email": "2670226747@qq.com",
      "username": "Cassius0924"
    },
    "added": [

    ],
    "removed": [

    ],
    "modified": [
      ".config/lvim/config.lua"
    ]
  }
}
"""
