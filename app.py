import os
import env
from flask import Flask, render_template, redirect, request, url_for, flash,  session, make_response, current_app, abort
from flask_login import LoginManager 
from flask_user import login_required, UserManager, UserMixin
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash




app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'project_manager'
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config['SECRET_KEY'] = 'the random string'   

mongo = PyMongo(app)


@app.route('/')
def index():
    return render_template('index.html')
    

@app.route('/login', methods=["POST", "GET"])
def login():
    users = mongo.db.users
    login_user = users.find_one({"username" : request.form.get("username", False)})
    if login_user:
        if (request.form['pass']) == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('get_tasks'))
        flash('Invalid username/password combination')

    return render_template('login.html')

@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        users = mongo.db.users
        existing_user = users.find_one({"username" : request.form['username']})
        if existing_user is None:
            users.insert({'username' : request.form['username'],
                            'password' : request.form['pass'],
                            'email' : request.form['email']
            })
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        flash("Username already exist! Try again!")
    return render_template('register.html')

@app.route('/add_task')
def add_task():
    the_task =  mongo.db.tasks.find_one({"_id": ObjectId()})
    return render_template('addtask.html',task=the_task,)

    
@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    the_task =  mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    all_categories =  mongo.db.categories.find()
    return render_template('edittask.html', task=the_task,
    categories=all_categories)

@app.route('/get_tasks')
def get_tasks():
    return render_template("tasks.html", tasks=mongo.db.tasks.find())    



@app.route('/insert_task', methods=['POST'])
def insert_task():
    tasks =  mongo.db.tasks
    tasks.insert_one(request.form.to_dict())
    authors = mongo.db.authors
    authors.insert_one({"author" : request.form.get("author")})
    return redirect(url_for('get_tasks'),tasks=mongo.db.tasks.find())


@app.route('/update_task/<task_id>', methods=["POST"])
def update_task(task_id):
    tasks = mongo.db.tasks
    tasks.update( {'_id': ObjectId(task_id)},
    {
        'recipe_name':request.form.get('recipe_name'),
        'ingredients':request.form.get('ingredients'),
        'task_description': request.form.get('task_description'),
        'allergens': request.form.get('allergens'),
        'author': request.form.get('username'),
        'country':request.form.get('country'),
        'imageURL':request.form.get('imageURL')
    })
    authors = mongo.db.authors
    authors.insert_one({"author" : request.form.get("author")})
    return redirect(url_for('get_tasks'),tasks=mongo.db.tasks.find(task_id))

@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    mongo.db.tasks.remove({'_id': ObjectId(task_id)}, )
    return redirect(url_for('get_tasks'))
    
@app.route('/get_categories')
def get_categories():
    return render_template('categories.html',
    categories=mongo.db.categories.find())
                           
@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    return render_template('editcategory.html',
    category=mongo.db.categories.find_one({'_id': ObjectId(category_id)}))
    
@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    mongo.db.categories.update(
        {'_id': ObjectId(category_id)},
        {'category_name': request.form.get('category_name')})
    return redirect(url_for('get_categories'))

@app.route('/delete_category/<category_id>')
def delete_category(category_id):
    mongo.db.categories.remove({'_id': ObjectId(category_id)})
    return redirect(url_for('get_categories'))
    
@app.route('/insert_category', methods=['POST'])
def insert_category():
    category_doc = {'category_name': request.form.get('category_name')}
    mongo.db.categories.insert_one(category_doc)
    return redirect(url_for('get_categories'))
    
@app.route('/add_category')
def add_category():
    return render_template('addcategory.html')

@app.route('/logout')
def logout():
    session.pop('username')
    flash("Successfully logged out ...")
    return redirect(url_for('index')) 
    
@app.route('/search', methods=['POST','GET'])
def search(): 
    return render_template('search.html', tasks=mongo.db.tasks.find_one({'_id':ObjectId()}))


@app.route('/search_recipes', methods=['POST','GET'])
def search_recipes():
    if request.method == "POST":
        recipes=list(mongo.db.recipes.find({"name": {"$regex":request.form['search']}}))
        print(recipes,request.form.get('search'))
        if recipes:
            return render_template('search_recipes.html', tasks=mongo.db.tasks.find_one({'_id':ObjectId()}),recipes=recipes)
        else:
            return render_template('404.html', tasks=mongo.db.tasks.find_one({'_id':ObjectId()}), recipes=recipes,message='No recipes found')
    return render_template('search.html', tasks=mongo.db.tasks.find_one({'_id':ObjectId()}),recipes=recipes)        
    

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)