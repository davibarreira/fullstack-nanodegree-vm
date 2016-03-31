#
# Database access functions for the web forum.
# 

import time
import psycopg2 as pg
import bleach

## Database connection
DB = []


## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
#    posts = [{'content': str(row[1]), 'time': str(row[0])} for row in DB]
#    posts.sort(key=lambda row: row['time'], reverse=True)

    db = pg.connect('dbname=forum')
    c  = db.cursor()
    query = "select content,time from posts order by time"
    c.execute(query)
    rows = c.fetchall()
    posts = [{'content': str(row[0]), 'time': str(row[1])} for row in rows]
    db.close()
    return posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    t = time.strftime('%c', time.localtime())
    DB.append((t, content))


    content = bleach.clean(content)

    db = pg.connect('dbname=forum')
    c  = db.cursor()
#    id = 0
#    query = "insert into posts values ('%s', '%s',%d)" % (content,t,id)
#    query = "insert into posts (content) values ('%s')" % (content)
    c.execute("insert into posts (content) values (%s)", (content,))
    db.commit()
    db.close()
