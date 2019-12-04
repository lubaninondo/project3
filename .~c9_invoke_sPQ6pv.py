import os
import env
from flask import Flask, render_template, flash, redirect, request, url_for, session, make_response, current_app
from flask_login import current_user, login_user, logout_user, login_required
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'project_manager'
app.config['MONGO_URI'] = os.getenv("MONGO_URI")

mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('login.html', register=mongo.db.register.find_one())

"""
Register form action firsly, method must be post and we going to insert in database by given details from input in register.html 
and then It will redirect to get recipes
"""
@app.route('/register',methods=['POST','GET'])
def register():
    if request.method == 'POST':
        register = mongo.db.register
        reg_id = register.insert_one(request.form.to_dict())
        # print(register)
        object_id = reg_id.inserted_id
        return redirect(url_for('get_task'))
    return render_template('register.html')

"""
Login page action. Firstly, method must be post and we will find the given password and username if it match we will
redirect to get recipes if not redirect to register and if password only incorrect we will show password is incorrect
"""
@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == 'POST':
        login_user = mongo.db.register.find_one({'username': request.form['username']})
        form = request.form
        if login_user:
            if(form["password"] == login_user["password"]): # if password correct
                session['username'] = login_user["username"]
                return redirect(url_for('get_recipe',register_id = login_user["_id"]))
            else: # and if password is not correct
               flash("Incorrect password") 
        else:# if not exist
            flash("User does not exist")
            return redirect(url_for('register'))
    return render_template('login.html')
            
"""
Delete page action If user want to delete their account the information will remove from database
"""
@app.route('/delete_register/<register_id>',methods=["GET","POST"] )
def delete_register(register_id):

    mongo.db.register.remove({'_id':ObjectId(register_id)})
    return redirect(url_for('login'))

@app.route('/')
@app.route('/get_tasks')
@login_required
def get_tasks():
    return render_template("tasks.html", 
                           tasks=mongo.db.tasks.find())


@app.route('/add_task')
@login_required
def add_task():
    return render_template('addtask.html',
    categories= mongo.db.categories.find())


@app.route('/insert_task', methods=['POST'])
@login_required
def insert_task():
    tasks =  mongo.db.tasks
    tasks.insert_one(request.form.to_dict())
    return redirect(url_for('get_tasks'))


@app.route('/edit_task/<task_id>')
@login_required
def edit_task(task_id):
    the_task =  mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    all_categories =  mongo.db.categories.find()
    return render_template('edittask.html', task=the_task,
    categories=all_categories)

@app.route('/update_task/<task_id>', methods=["POST"])
@login_required
def update_task(task_id):
    tasks = mongo.db.tasks
    tasks.update( {'_id': ObjectId(task_id)},
    {
        'recipe_name':request.form.get('recipe_name'),
        'ingredients':request.form.get('ingredients'),
        'task_description': request.form.get('task_description'),
        'allergens': request.form.get('allergens'),
        'author': request.form.get('author'),
        'country':request.form.get('country')
    })
    return redirect(url_for('get_tasks'))

@app.route('/delete_task/<task_id>')
@login_required
def delete_task(task_id):
    mongo.db.tasks.remove({'_id': ObjectId(task_id)})
    return redirect(url_for('get_tasks'))
    
@app.route('/get_categories')
def get_categories():
    return render_template('categories.html',
    categories=mongo.db.categories.find())
                           
@app.route('/edit_category/<category_id>')
@login_required
def edit_category(category_id):
    return render_template('editcategory.html',
    category=mongo.db.categories.find_one({'_id': ObjectId(category_id)}))
    
@app.route('/update_category/<category_id>', methods=['POST'])
@login_required
def update_category(category_id):
    mongo.db.categories.update(
        {'_id': ObjectId(category_id)},
        {'category_name': request.form.get('category_name')})
    return redirect(url_for('get_categories'))

@app.route('/delete_category/<category_id>')
@login_required
def delete_category(category_id):
    mongo.db.categories.remove({'_id': ObjectId(category_id)})
    return redirect(url_for('get_categories'))
    
@app.route('/insert_category', methods=['POST'])
@login_required
def insert_category():
    category_doc = {'category_name': request.form.get('category_name')}
    mongo.db.categories.insert_one(category_doc)
    return redirect(url_for('get_categories'))
    
@app.route('/add_category')
@login_required
def add_category():
    return render_template('addcategory.html')
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
    

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=False)