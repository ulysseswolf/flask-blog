import sys
import re
import datetime


class Post:
    def __init__(self, database):
        self.db = database
        self.posts = database.posts

    def get_posts(self, limit, skip, tag=None):
        cond = {}
        if tag is not None:
            cond = {'tags': tag}
        print skip, limit
        cursor = self.posts.find(cond).sort('date', direction=-1).skip(skip).limit(limit)
        l = []

        for post in cursor:
            post['date'] = post['date'].strftime("%a, %d %b %Y")
            if 'tags' not in post:
                post['tags'] = []
            if 'comments' not in post:
                post['comments'] = []

            l.append({'title': post['title'], 'body': post['body'], 'post_date': post['date'],
                      'permalink': post['permalink'],
                      'tags': post['tags'],
                      'author': post['author'],
                      'comments': post['comments']})

        return l

    def get_post_by_permalink(self, permalink):
        post = self.posts.find_one({'permalink': permalink})
        if post is not None:
            post['date'] = post['date'].strftime("%a, %d %b %Y")

        return post

    def get_total_count(self, tag=None):
        if tag is not None:
            return self.posts.find({'tags': tag}).count()
        else:
            return self.posts.count()