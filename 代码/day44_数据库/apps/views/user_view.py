import hashlib

from flask import Blueprint, render_template, request, redirect, url_for, make_response,session
from sqlalchemy import or_

from apps.models.blog_model import User, Article
from exts import db

blog_bp = Blueprint('blog', __name__, url_prefix='/blog')


# 首页
@blog_bp.route('/', endpoint='index')
def index():
    articles = Article.query.all()
    # uname = request.cookies.get('uname')
    # print(uname)
    uname = session.get('uname')
    print(uname)
    return render_template('index.html', articles=articles)


# 用户更新
@blog_bp.route('/update', endpoint='update', methods=['GET', 'POST'])
def user_update():
    if request.method == 'GET':
        id = request.args.get('id')
        user = User.query.get(id)  # 要更新的用户对象
        return render_template('update.html', user=user)
    else:
        id = request.form.get('id')
        username = request.form.get('username')
        phone = request.form.get('phone')
        isdelete = request.form.get('isdelete')

        user = User.query.get(id)  # 要更新的用户对象
        user.username = username
        user.phone = phone
        # isdelete添加判断

        db.session.commit()
        return redirect(url_for('blog.uall'))


# 用户删除
@blog_bp.route('/delete/<id>', endpoint='delete')
def user_delete(id):
    user = User.query.get(id)  # 根据主键查找对象
    # print(user)
    db.session.delete(user)  # 物理删除
    # user.isdelete = True
    db.session.commit()
    return redirect(url_for('blog.uall'))


# 用户检索
@blog_bp.route('/search', endpoint='search', methods=['POST'])
def user_search():
    search = request.form.get('search')
    if search:
        # users = User.query.filter(or_(User.username==search,
        #                       User.phone == search)).all()  # select * from user where username=search or phone=search
        # number = User.query.filter(or_(User.username==search,
        #                       User.phone == search)).count()
        users = User.query.filter(or_(User.username.like('%' + search + '%'), User.phone == search)).all()
        number = User.query.filter(or_(User.username.like(search), User.phone == search)).count()
        return render_template('user_all.html', users=users, number=number)
    else:
        return redirect(url_for('blog.index'))


# 显示所有用户
@blog_bp.route('/userall', endpoint='uall')
def user_all():
    # users = User.query.filter_by(isdelete=False).all()
    # users = User.query.filter(User.isdelete == False, User.phone.startswith('150')).order_by(-User.rdatetime)
    users = User.query.all()
    number = User.query.count()
    return render_template('user_all.html', users=users, number=number)


# 用户退出
@blog_bp.route('/exit', endpoint='exit')
def user_exit():
    # cookie 的退出方式
    # response = redirect(url_for('blog.index'))
    # response.delete_cookie('uname')
    # response.delete_cookie('test')
    # response.set_cookie()
    # return response

    # session 的退出方式
    session.clear()
    return redirect(url_for('blog.index'))



# 用户登录
@blog_bp.route('/login', endpoint='login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form.get('username')
        pwd1 = request.form.get('password1')
        pwd = hashlib.sha1(pwd1.encode('utf-8')).hexdigest()
        # 查询
        user = User.query.filter_by(username=username).first()  # select * from user where username=xxxx
        if pwd == user.password:
            # cookie 记录在客户端的一种方式
            # 写cookie要通过response对象完成
            # response = make_response('用户登录成功！')
            # response.set_cookie('uname', username)
            # response.set_cookie('test', '123')
            # response = redirect(url_for('blog.index'))
            # response.set_cookie('uname', username)
            # return response

            # session 机制  记录登录状态
            session['uname']=username

            return redirect(url_for('blog.index'))

        else:
            return render_template('login.html', msg='用户名或者密码有误！')

    return render_template('login.html')


# 用户注册
@blog_bp.route('/register', endpoint='register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        # 获取表单提交的内容
        username = request.form.get('username')
        pwd1 = request.form.get('password1')
        pwd2 = request.form.get('password2')
        phone = request.form.get('phone')
        if pwd1 == pwd2:
            # 存放到数据库
            pwd = hashlib.sha1(pwd1.encode('utf-8')).hexdigest()
            print(pwd)
            # 添加数据步骤:
            # 1. 创建模型对象
            user = User()
            # 2. 给对象赋值
            user.username = username
            user.password = pwd
            user.phone = phone
            # 3. 向数据库提交数据
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('blog.index'))

        else:
            return render_template('register.html', msg=' 密码不一致')

    return render_template('register.html')
