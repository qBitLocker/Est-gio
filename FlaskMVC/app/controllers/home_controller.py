from flask import render_template
from app.models.post import Post

class HomeController():
    def index(self):
        # return "Hello, World"
        posts = Post.query.all()
        # Não há necessidade de configurar a pasta views 
        return render_template('posts/index.html', posts=posts)
