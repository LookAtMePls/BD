from flask import Flask, render_template, request, url_for, redirect
from pony.flask import Pony
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from forms import *

app = Flask(__name__)
app.secret_key = 'asd&*$VNkhvrhk*V#__w3vqlbq;1'
pony = Pony(app)
manager = LoginManager(app)
manager.login_view = 'login'

@manager.user_loader
def load_user(user_id):
    return User.get(id=user_id)


@app.route('/')
def index():
    return redirect(url_for('store'))


@app.route('/reg', methods=['POST', 'GET'])
def reg():
    form = RegForm(request.form)
    if request.method == 'POST' and form.validate():
        User(login=form.data['login'], email=form.data['email'], pwd=form.data['pwd1'], is_compiler=False)
        return redirect(url_for('login'))
    return render_template('reg.html', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.get(login=form.data['login'])
        pwd = form.data['pwd']
        if user.pwd != pwd:
            return 'Incorrect password'
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout')
@app.route('/com/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@app.route('/order')
@login_required
def order():
   dish = select(g for g in Dish if g in current_user.dish_in_order).order_by(Dish.title)
   return render_template('order.html', user=current_user, dishes=dish)

@app.route('/store')
def store():
    dish = Dish.select().order_by(Dish.title)
    return render_template('store.html', user=current_user, dishes=dish)

@app.route('/dish/<int:id>')
@login_required
def dish(id):
    dish = Dish.get(id=id)
    scores = select(s for s in Score if s.dish == dish).order_by(Score.dt)
    if dish is None:
        return redirect(page_not_found)
    return render_template('dish.html', user=current_user, dish=dish, scores=scores)

@app.route('/post_score', methods=['POST'])
@login_required
def post_score():
    dish_id = request.form['id']
    score = request.form['score']
    text = request.form['text']
    dish = Dish.get(id=dish_id)
    print(dish_id)
    if dish is not None:
        Score(dish=dish, value=int(score), text=text, user=current_user, dt=datetime.now())
    return redirect(url_for('dish', id=dish_id))

@app.route('/purchase/<int:id>')
@login_required
def purchase(id):
    dish = Dish.get(id=id)
    user = current_user
    if dish not in user.dish_in_order:
        if user.money >= dish.price:
            Transaction(type='Buy', value=-dish.price, user=user, description=dish.title, dt=datetime.now())
            user.money -= dish.price
            user.dish_in_order.add(dish)
    return redirect(url_for('dish', id=id))

@app.route('/add_money', methods=['POST', 'GET'])
@login_required
def add_money():
    if request.method == 'POST':
        money = request.form['money']
        try:
            money = int(money)
        except:
            money = 0
        t = Transaction(type='Add', value=money, user=current_user, dt=datetime.now())
        current_user.money += money
        return redirect(url_for('index'))
    return render_template('add_money.html', user=current_user)



@app.route('/com/reg', methods=['POST', 'GET'])
def com_reg():
    form = comRegForm(request.form)
    if request.method == 'POST' and form.validate():
        User(login=form.data['login'], email=form.data['email'], pwd=form.data['pwd1'], is_compiler=True)
        return redirect(url_for('com_login'))
    return render_template('com_reg.html', form=form)

@app.route('/com/login', methods=['POST', 'GET'])
def com_login():
    form = comLoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.get(login=form.data['title'], pwd=form.data['pwd'])
        login_user(user)
        return redirect(url_for('index'))
    return render_template('com_login.html', form=form)

@app.route('/com/dishes_created')
@login_required
def created():
    if not current_user.is_compiler:
        return redirect(url_for('index'))

    dishes = select(g for g in Dish if g.compiler == current_user).prefetch(Score)[:]
    return render_template('com_created.html', user=current_user, dishes=dishes)

@app.route('/com/dish/new', methods=['POST', 'GET'])
@login_required
def com_dish_new():
    if not current_user.is_compiler:
        return redirect('index')

    form = comNewDishForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.data['title']
        desc = form.data['description']
        type_of_food = form.data['type_of_food']
        price = form.data['price']
        small = form.data['small'] or None
        cover = form.data['cover'] or None
        Dish(title=title, description=desc, type_of_food=type_of_food, price=price, compiler=current_user, small=small, cover=cover)
        return redirect(url_for('created'))
    return render_template('com_dish_new.html', user=current_user, form=form)

@app.route('/com/dish/<int:id>', methods=['POST', 'GET'])
@login_required
def com_dish(id):
    if not current_user.is_compiler:
        return redirect('index')
    dish = select(g for g in Dish if g.id == id).prefetch(Score, Dish.compiler).first()
    if dish is None:
        return redirect(page_not_found)
    if dish.compiler.id != current_user.id:
        return redirect(url_for('dish', id=id))

    if request.method == 'POST':
        dish.title = request.form['title']
        dish.desc = request.form['description']
        dish.type_of_food = request.form['type_of_food']
        dish.price = request.form['price']
        dish.small = request.form['small'] or None
        dish.cover = request.form['cover'] or None
    return render_template('com_dish.html', user=current_user, dish=dish)

@app.route('/com/delete_score/<int:dish_id>/<int:score_id>')
@login_required
def com_delete_score(dish_id, score_id):
    dish = Dish.get(id=dish_id)
    if dish is None or dish.compiler.id != current_user.id:
        return redirect(url_for('dish', id=dish_id))
    delete(s for s in Score if s.id == score_id)
    return redirect(url_for('dish', id=dish_id))

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

