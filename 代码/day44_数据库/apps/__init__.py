from flask import Flask

from apps.views.article_view import article_bp
from apps.views.user_view import blog_bp
from exts import db
from settings import DevelopmentConfig


def create_app():
    app = Flask(__name__,template_folder='../templates')
    app.config.from_object(DevelopmentConfig)
    # 给db对象初始化app
    db.init_app(app)
    # 注册蓝图
    app.register_blueprint(blog_bp)
    app.register_blueprint(article_bp)
    return app
