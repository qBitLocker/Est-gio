from flask import render_template
from app.models.post import Post

class PostsController():
    def show (self):
        print ('Processando requisicao POST')
        #print (product_id)
        #result = Post.query.get(int(product_id))

        return render_template('posts/query.html', result=None)