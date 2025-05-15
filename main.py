import random

from flask import Flask, url_for, render_template, redirect
# механизмом разделения приложения API
import blueprints.shop_api as shop_api
import blueprints.catalog_api as catalog_api
import blueprints.basket_api as basket_api
import blueprints.card_api as card_api
import blueprints.user_api as user_api
import blueprints.favorites_api as favorites_api
import blueprints.order_api as order_api
import blueprints.review_api as review_api

# Формы
from forms.registration_form import RegistrationForm
from forms.login_form import LoginForm

# БД и таблицы 
from data.db_session import global_init, create_session
from data.user import User
from data.basket import Basket

# аунтификация
from flask_login import LoginManager, login_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tamironpost_bytecraftstore'


avatars = ['arab.png', 'ino.png', 'coffee.png', 'batman.png', 'cactus.png','sloth.png', 'oblaco.png', 'bear.png', 'zombie.png', 'cat.png']

#Аунтификация
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'first'


@login_manager.user_loader
def load_user(user_id):
    db_sess = create_session()
    return db_sess.query(User).get(user_id)


# НАЧАЛО (Главная страница)
@app.route('/start')
@app.route('/')
def first():
    if current_user.is_authenticated:
        return redirect("/shop/main_page")
    return render_template('start.html')

# Регистрация
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    lst_poles = [form.firstname, form.lastname, form.patronymic, form.email, form.phone, form.password, form.repeat_password, form.remember_me]
    if form.validate_on_submit():
        # успешная регистрация, создание пользователя, передача ему управления, вызов главной страницы
        if form.password.data != form.repeat_password.data:
            return render_template('all_forms.html', lst_poles=lst_poles, title='Зарегистрироваться', hidden=form.hidden_tag(), message="Пароли не совпадают")
        
        ses = create_session()
        if ses.query(User).filter(User.Email == form.email.data).first():
            return render_template('all_forms.html', lst_poles=lst_poles, title='Зарегистрироваться', hidden=form.hidden_tag(), message="Такой пользователь уже есть")
        user = User()
        user.FirstName = form.firstname.data
        user.LastName = form.lastname.data
        user.Patronymic = form.patronymic.data
        user.Email = form.email.data
        user.PhoneNumber = form.phone.data
        user.set_password(form.password.data)
        user.Image_Avatar = random.choice(avatars)
        ses.add(user)
        ses.commit()
        
        # Создание корзины для
        basket = Basket()
        basket.IdUser = user.Id        
        ses.add(basket)
        ses.commit()
        
        login_user(user, remember=form.remember_me.data)
        return redirect("/")
    return render_template('all_forms.html', lst_poles=lst_poles, title='Зарегистрироваться', hidden=form.hidden_tag())

# ВХОД
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    lst_poles = [form.email, form.password, form.remember_me]
    if form.validate_on_submit():
        ses = create_session()
        user = ses.query(User).filter(User.Email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        else:
            return render_template('all_forms.html', lst_poles=lst_poles, title='Войти', hidden=form.hidden_tag(), message="Неправильный email или пароль")
    return render_template('all_forms.html', lst_poles=lst_poles, title='Войти', hidden=form.hidden_tag())


# Проверка БД
@app.route('/users')
def get_all_users():
    ses = create_session()
    users = ses.query(User).all()
    return f'<h1> {','.join([x.FirstName for x in users])}</h1>'


if __name__ == '__main__':
    global_init()
    app.register_blueprint(shop_api.blueprint)
    app.register_blueprint(catalog_api.blueprint)
    app.register_blueprint(basket_api.blueprint)
    app.register_blueprint(card_api.blueprint)
    app.register_blueprint(user_api.blueprint)
    app.register_blueprint(favorites_api.blueprint)
    app.register_blueprint(order_api.blueprint)
    app.register_blueprint(review_api.blueprint)
    app.run(debug=True)