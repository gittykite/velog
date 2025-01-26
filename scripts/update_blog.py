import feedparser
import git
import os

# RSS feed url of Velog
rss_url = 'https://api.velog.io/rss/@dataiiing'

# path for GitHub repo
repo_path = '.'

# path for 'velog-posts' folder
posts_dir = os.path.join(repo_path, 'velog-posts')
if not os.path.exists(posts_dir):
    os.makedirs(posts_dir)

# load GitHub repo & RSS feed
repo = git.Repo(repo_path)
feed = feedparser.parse(rss_url)

# create article files
for entry in feed.entries:
    # validate filenames
    file_name = entry.title
    file_name = file_name.replace('/', '-')  # slash -> dash
    file_name = file_name.replace('\\', '-')  # backslash -> dash

    # set file path 
    file_name += '.md'
    file_path = os.path.join(posts_dir, file_name)

    # create unexisting files
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(entry.description) 

        # commit files
        repo.git.add(file_path)
        repo.git.commit('-m', f'Add post: {entry.title}')

# push commit
repo.git.push()
