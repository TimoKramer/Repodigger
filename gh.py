from github import Github

g = Github("timokramer", "gitte_und_huber3")

for repo in g.get_user().get_repos():
    print(repo.name)
    repo.edit(has_wiki=False)
