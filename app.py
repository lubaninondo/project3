import os
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
            return redirect(url_for('get_recipes'))
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
            return redirect(url_for('get_recipes'))
        flash("Username already exist! Try again!")
    return render_template('register.html')

@app.route('/add_recipe')
def add_recipe():
    the_recipe =  mongo.db.recipes.find_one({"_id": ObjectId()})
    return render_template('addrecipe.html',recipe=the_recipe,)

    
@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe =  mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    all_categories =  mongo.db.categories.find()
    return render_template('editrecipe.html', recipe=the_recipe,
    categories=all_categories)

@app.route('/get_recipes')
def get_recipes():
    return render_template("recipes.html", recipes=mongo.db.recipes.find())    



@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes =  mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    authors = mongo.db.authors
    authors.insert_one({"author" : request.form.get("author")})
    return redirect(url_for('get_recipes'))


@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    recipes = mongo.db.recipes
    recipes.update( {'_id': ObjectId(recipe_id)},
    {
        'recipe_name':request.form.get('recipe_name'),
        'ingredients':request.form.get('ingredients'),
        'recipe_description': request.form.get('recipe_description'),
        'allergens': request.form.get('allergens'),
        'author': request.form.get('username')
    })
    authors = mongo.db.authors
    authors.insert_one({"author" : request.form.get("author")})
    return redirect(url_for('get_recipes'))

@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)}, )
    return redirect(url_for('get_recipes'))
    
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
      
    

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=False)