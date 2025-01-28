from flask import render_template
from app.models.post import Post

class PostsController ():
    def show (self):
        result = Post.query.get(1)
        print (type(result))

        return render_template('posts/query.html', result=result)