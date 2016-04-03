from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


app = Flask(__name__)


@app.route('/')
def DefaultMenu():
    restaurant = session.query(Restaurant).first()
    item       = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    output     = "<h1>"+ restaurant.name +"</h1>" + "</br>"
    for i in item:
        output+=i.name
        output+="</br>"
        output+=i.price
        output+="</br>"
        output+=i.description
        output+="</br>"
        output+="</br>"
    return  output


@app.route('/restaurant/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    item       = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    output     = "<h1>"+ restaurant.name +"</h1>" + "</br>"
    for i in item:
        output+=i.name
        output+="</br>"
        output+=i.price
        output+="</br>"
        output+=i.description
        output+="</br>"
        output+="</br>"
    return  output


#Task 1: Create route for newMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/new/')
def newMenuItem(restaurant_id):
	return "page to create a new menu item. Task 1 complete!"

#Task 2: Create route for editMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
	return "page to edit a new menu item. Task 2 complete!"

#Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
			return "page to delete a new menu item. Task 3 complete!"



if __name__=='__main__':
    app.debug = True
    app.run(host='0.0.0.0', port = 5000)
