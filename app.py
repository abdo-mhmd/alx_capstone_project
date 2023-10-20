from datetime import date, timedelta
from webapp import create_app
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from webapp.models import User, Task, TaskCategory
from webapp.forms import LoginForm, RegistrationForm, AddTaskForm, ChangePassword, AddTaskCategoryForm
from webapp import login_manager, db, bcrypt


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


app = create_app()


@app.route('/')
@app.route('/home')
def home():
    if current_user:
        tasks = Task.query.all()
        user = User.query.get(current_user.get_id())
        return render_template('home.html', tasks=tasks, user=user, date=date.today())
    return redirect(url_for('login'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if request.method == 'POST':
        email = form.email.data
        password = form.password.data
        remember = form.remember.data

        user = User.query.filter_by(email=email).first()

        if user:
            if bcrypt.check_password_hash(user.password, password):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=remember)
                flash('Login Successful', 'success')
                return redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check password', 'danger')
        else:
            flash('Login Unsuccessful. Please check email', 'danger')

    return render_template('login.html', form=form)


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User(
            email=form.email.data,
            username=form.username.data,
            password=bcrypt.generate_password_hash(form.password.data)
        )
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {user.username}!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    """Logout the logged in user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))


@app.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    if request.method == 'POST':
        search = request.form['search']
        tasks = Task.query.filter_by(user_id=current_user.get_id()).filter(
            Task.title.contains(search)
        ).all()
    else:
        tasks = Task.query.filter_by(user_id=current_user.get_id()).all()
    categories = TaskCategory.query.all()
    return render_template('tasks.html', tasks=tasks, categories=categories)


@app.route("/addtask", methods=['GET', 'POST'])
@login_required
def add_task():
    form = AddTaskForm()
    if request.method == 'POST':
        task = Task(
            title=form.title.data,
            description=form.description.data,
            due_date=form.due_date.data,
            priority=form.priority.data,
            user_id=current_user.get_id(),
            category_id=form.category.data,
        )
        db.session.add(task)
        db.session.commit()
        flash('Task added successfully', 'success')
        return redirect(url_for('tasks'))
    categories = TaskCategory.query.all()
    form.category.choices = [(category.id, category.name)
                             for category in categories]
    return render_template('addtask.html', form=form)


@app.route('/updatetask/<int:id>', methods=['GET', 'POST'])
@login_required
def update_task(id):
    form = AddTaskForm()
    task = Task.query.filter_by(id=id).first()
    category = TaskCategory.query.filter_by(id=task.category_id).first()
    if request.method == 'POST':
        task.title = form.title.data
        task.description = form.description.data
        task.due_date = form.due_date.data
        task.priority = form.priority.data
        task.category_id = form.category.data
        db.session.commit()
        flash('Task updated successfully', 'success')
        return redirect(url_for('tasks'))
    form.title.data = task.title
    form.description.data = task.description
    form.due_date.data = task.due_date
    form.priority.data = task.priority
    form.category.data = category.name
    categories = TaskCategory.query.all()
    form.category.choices = [(category.id, category.name)
                             for category in categories]
    return render_template('updatetask.html', form=form, id=id)


@app.route('/deletetask/<int:id>')
@login_required
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully', 'success')
    return redirect(url_for('tasks'))


@app.route('/completetask/<int:id>')
@login_required
def complete_task(id):
    render = request.args.get('render')
    task = Task.query.get_or_404(id)
    task.status = True
    db.session.commit()
    flash('Task completed successfully', 'success')
    return redirect(url_for(render))

@app.route('/addcategory', methods=['GET', 'POST'])
@login_required
def add_category():
    form = AddTaskCategoryForm()
    categories = TaskCategory.query.all()
    if request.method == 'POST':
        category = TaskCategory(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash('Category added successfully', 'success')
        return redirect(url_for('add_category'))
    return render_template('category.html', form=form, categories=categories)

@app.route('/deletecategory/<int:id>')
@login_required
def delete_category(id):
    category = TaskCategory.query.get(id)
    db.session.delete(category)
    db.session.commit()
    flash('Category deleted successfully', 'success')
    return redirect(url_for('add_category'))

@app.route('/completedtasks')
@login_required
def completed_tasks():
    tasks = Task.query.filter_by(
        user_id=current_user.get_id(), status=True).all()
    return render_template('tasks.html', tasks=tasks)
# search by date


@app.route('/searchbydate', methods=['GET', 'POST'])
@login_required
def search_by_date():
    if request.method == "POST":
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        if not (start_date and end_date):
            flash('Please enter both start and end dates', 'danger')
            return redirect(url_for('tasks'))
        else:
            tasks = Task.query.filter_by(user_id=current_user.get_id()).filter(
                Task.due_date.between(start_date, end_date)
            ).all()
    return render_template('tasks.html', tasks=tasks)


@app.route('/todaytasks')
@login_required
def today_tasks():
    today = date.today()
    tomorrow = today + timedelta(days=1)
    tasks = Task.query.filter_by(user_id=current_user.get_id()).filter(
        Task.due_date.between(today, tomorrow)
    ).all()

    return render_template('tasks.html', tasks=tasks)


@app.route('/tomorrowtasks')
@login_required
def tomorrow_tasks():
    today = date.today()
    tomorrow = today + timedelta(days=1)
    after_tomorrow = today + timedelta(days=2)

    tasks = Task.query.filter_by(user_id=current_user.get_id()).filter(
        Task.due_date.between(tomorrow, after_tomorrow)
    ).all()

    return render_template('tasks.html', tasks=tasks)


@app.route('/weektasks')
@login_required
def week_tasks():
    start_date = date.today()
    end_date = start_date + timedelta(days=7)
    tasks = Task.query.filter_by(user_id=current_user.get_id()).filter(
        Task.due_date.between(start_date, end_date)
    ).all()
    return render_template('tasks.html', tasks=tasks)


@app.route('/monthlytasks')
@login_required
def monthly_tasks():
    end_date = date.today() + timedelta(days=30)
    start_date = date.today()

    tasks = Task.query.filter(
        Task.user_id == current_user.get_id(),
        Task.due_date.between(start_date, end_date)
    ).all()
    return render_template('tasks.html', tasks=tasks)

# function to filter by priority


@app.route('/priority_tasks/<string:priority>', methods=['GET', 'POST'])
@login_required
def priority_tasks(priority):
    user_id = current_user.get_id()
    tasks = Task.query.filter_by(user_id=user_id, priority=priority).all()
    return render_template('tasks.html', tasks=tasks)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = User.query.get(current_user.get_id())
    change_form = ChangePassword()
    user_form = LoginForm()
    if request.method == 'POST':

        if change_form.validate_on_submit():
            old_password = change_form.old_password.data
            new_password = change_form.new_password.data
            confirm_password = change_form.confirm_password.data
            if not bcrypt.check_password_hash(user.password, old_password):
                flash('Old password does not match', 'danger')
                return redirect(url_for('change_password'))
            if new_password != confirm_password:
                flash('Passwords do not match', 'danger')
                return redirect(url_for('profile'))
            user.password = bcrypt.generate_password_hash(new_password)
            db.session.commit()
            flash('Password changed successfully', 'success')
            return redirect(url_for('profile'))
        elif user_form.is_submitted():
            user.email = request.form['email']
            user.username = request.form['username']
            db.session.commit()
            flash('Profile updated successfully', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Something went wrong', 'danger')
            return redirect(url_for('profile'))
    user_form.email.data = user.email
    user_form.username.data = user.username
    return render_template('profile.html', title='Profile', user_form=user_form, change_form=change_form)


if __name__ == '__main__':
    app.run(debug=True)
