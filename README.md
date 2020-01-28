# **Project 3- Data- Centric (C.R.U.D)**

The project allows for online cookbooks to be submitted online by hotel managers/ chefs of an International hote;. A user can add the name of the recipe, the author of the recipes and describe how to prepare the meal. Allergens should be mentioned if there available or not. If there are available there can be mentioned. 
The user also has the ability to edit his/her recipe before and after submission. 

# **UX**

The website is ideal for individuals and chefs who like to share recipes and improve their cooking. The website was designed in such a way that the user can delete or edit the recipe they created but cannot change the ones created by other users. Anyone who visits the website can view all the recipes

First time users have to register using the email, username and password.

Registered users can simple login and use the website

Admin can delete, edit the recipes and users in the database

# **Features**

   Project 3 has the following features:
   
   ## **Registration** :
   
   New Users can register by filling the registration form. Email address, Username and password are needed to register an account
   
   ## **Login**
   
   Registered users can login by filling the login form and use the website. Username and password are needed for loging in.
   
   ## **Create/Add recipe**
   
   Only registered users can create a recipe by clicking the new task button and fill the form
   
   ## **Delete**
   
   Only the creator of the recipe can delete it by clicking del in front of her recipe
   
   ## **Edit Recipe**
    
   Only the creator of the recipe can edit it by clicking edit in front of her recipe and fill in the edit task form
 
   ## **Read**
 
 Only registered users have access to view recipes created by them and other users
 
 
 The following features are yet to be implemented:
 
   ## **Comment**
 
   Allow users to comment on the recipes and give further suggestions
 
   ## **Like**
 
 Allow the users to click the like button for the recipe that they like
    
    
**#Technology Used**


  [HTML5](https://html.spec.whatwg.org/multipage/) for structuring the page

  [CSS](https://www.w3schools.com/css/) for styling the project
  

  [Bson](http://bsonspec.org/)  was used for encoding
    
  [Python 3](https://www.python.org/)  The language used to run the model is python3
    
  
  [MongoDB](https://www.mongodb.com/) was the database used
    
  
  [Flask](http://flask.palletsprojects.com/en/1.1.x/) framework for building a useful websitek
   
    
  [Materialize](https://materializecss.com/)  frame work to provide a better UX
    
# **Testing**

## **Registration**:

Fill in the registration form. Email address, password and username are needed


1. If a registered username is used then a message saying username already exist appears


2. Correctly filling of the registration form and submitting will create an account and direct the user to the homepage

## **Log In**:

A registered user can use the username and password to login

1. Correct username and password results in the user logging in and directed to the home page

2. Using an unregistered username results in failure to login and a message saying username does not exist appearing

3.Wrong password results in failure to log in and a wrong password message appearing


## **Add Task**
    
  Click New task, then fill form and submit. New recipe will be created and will be directed to the home page
  
    
 ## **Editing**
    
  Click on the edit button in front of the recipe created by the user, change any information in any variable and update task. Recipe     will be updated and user will be redirected to home page
    
   
  ## **Delete Task**
   
   Click on the Del button in front of the recipe created by the user, Delete the task and the user will be redirected to home page
    
   
   ## **Responsiveness**
    
   The website was tested and respond to devices of different sizes using Chrome Developer tools. Right click in the website, click on      inspect. Adjust size of screen and see how it responds to different devices.

# **Deployment**

The  project was deployed to [Heroku](http://project3-heroku-mongo.herokuapp.com/) with a separate [Github](https://github.com/lubaninondo/project3) branch

**This is how I deployed to Heroku:**

 I click deployed on Heroku and connected to GitHub and chose lubaninondo/project3.
 
 I clicked deploy branch.
 
 **Var Config**
 
 MONGO_URI
 
 IP
 
 PORT
 
 


# **Credit**

## **Acknowledgement**
    
Thanks to Zartis who kept on encouraging me to do the course

The project was inspired by [jstokes1994](https://github.com/Code-Institute-Submissions/online-cookbook-2), [Ramanathan03](https://github.com/Code-Institute-Submissions/recipes-1), [Idettore](https://github.com/ldettorre/yummy) and [Code Institute](https://github.com/Code-Institute-Solutions/TaskManager)

## **Media**

Food images are from [veronicamollica]( http://veronicamollica.com/vegan-vs-flexitarian/) , [one.org](https://www.one.org/us/blog/10-popular-dishes-from-across-africa/) 


