from flask import(
    Flask,render_template, Blueprint, flash, g, redirect, request, session, url_for
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import functools
from os import error
from operator import pos

import os



app = Flask(__name__)
# app.config['SECRET_KEY'] = 'clave_secreta'


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/blog_python'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@db/blog_python'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flask:slimdingo85@flask/blog_python'
# app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://flask:slimdingo85@localhost/blog_python'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flask:slimdingo85@flask/blog_python'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(
#     os.getenv('DB_USER', 'root'),
#     os.getenv('DB_PASSWORD', ''),
#     os.getenv('DB_HOST', 'mysql'),
#     os.getenv('DB_NAME', 'blog_python')
# )
db=SQLAlchemy(app)



class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100))
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, author, title, body) -> None:
        self.author = author
        self.title = title
        self.body = body

    def __repr__(self) -> str:
        return f'Post: {self.title}'
    
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.Text)

    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password

    def __repr__(self) -> str:
        return f'User: {self.username}'

#Registrar un usuario 
@app.route('/register', methods=('GET','POST'))
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        conf_password = request.form.get('conf_password')
        user = User(username, generate_password_hash(password))
        error = None
        if not username :
            error = 'Usuario Incorrecto'
        elif not password:
            error = 'Se requiere contraseña'
        
        user_name = User.query.filter_by(username = username).first()
        if user_name == None:
            if ' ' in username:
                error = 'El usuario ingresado no es valido'
            elif password != conf_password:
                error = 'Las contraseñas no coinciden'
            elif len(password) < 8:
                error = 'La contraseña debe tener al menos 8 caracteres'
            else:  
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))
       
        else:
            error = f'El usuario {username} ya esta registrado'
        flash(error, 'danger')
      
    # return redirect(url_for('login '))  
    return render_template('register.html')

#Iniciar Sesión
@app.route('/login', methods=('GET','POST'))
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        error = None
        
        user = User.query.filter_by(username = username).first()

        if user == None:
            error = 'Nombre de usuario incorrecto'
        elif not check_password_hash(user.password, password):
            error = 'Contraseña incorrecta'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('index'))
        
        flash(error)
        
    return render_template('login.html')

#Obtener usuario actual
@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get_or_404(user_id)


#Crerrar sesion
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

#Decorador para verificar si el usuario esta logueado
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view




#Obtner un ususario
def get_user(id):
    user = User.query.get_or_404(id)
    return user

@app.route("/")
def index():
    posts = Post.query.all()
    posts = list(reversed(posts))
    db.session.commit()
    return render_template('index.html', posts = posts, get_user=get_user)

#Registrar un post 
@app.route('/blog/create', methods=('GET','POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')
        post = Post(g.user.id, title, body)
        error = None
        if not title:
            error = 'Debe ingresar un título válido'
        if error is not None:
            flash(error)
        else:
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('index'))
        flash(error)
        
    return render_template('create.html')


#Chequear si el usuario es el autor del post
def get_post(id, check_author=True):
    post = Post.query.get(id)

    if post is None:
        flash(404, f'Id {id} de la publicación no existe.')

    if check_author and post.author != g.user.id:
        flash(404)
    
    return post

#Update post 
@app.route('/blog/update/<int:id>', methods=('GET','POST'))
@login_required
def update(id):
    post = get_post(id) 
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.body = request.form.get('body')
        error = None
        if not post.title:
            error = 'Se requiere un título'
        if error is not None:
            flash(error)
        else:
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('index'))
        flash(error)
    return render_template('update.html', post=post)

#Eliminar un post 
@app.route('/blog/delete/<int:id>')
@login_required
def delete(id):
    post = get_post(id)
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('index'))


if __name__ == '__main__':
     # app.run(debug=True)
    app.run(debug=True,host='0.0.0.0')
    #app.run(debug=True, port=8000)
    # app.run(host='0.0.0.0', port=8000)