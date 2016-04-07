from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


app = Flask(__name__)

@app.route('/restaurant/json')
def restaurantJson():
    restaurant = session.query(Restaurant).all()
    return jsonify(RestaurantList=[i.serialize for i in restaurant])

@app.route('/restaurant/<int:restaurant_id>/menu/json')
def restaurantMenuJson(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    item       = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return jsonify(MenuItem=[i.serialize for i in item])


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/json')
def restaurantMenuItemJson(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    item       = session.query(MenuItem).filter_by(restaurant_id=restaurant.id,id=menu_id).one()
    return jsonify(MenuItem=item.serialize)




@app.route('/')
@app.route('/restaurant/')
def HomePage():
    restaurant = session.query(Restaurant).all()
    return render_template('home.html',restaurant=restaurant)

@app.route('/newrestaurant/', methods=['GET','POST'])
def newRestaurant():
    if request.method == 'POST':
        print 'teste'
        newRest = Restaurant(name = request.form['name'])
        session.add(newRest)
        session.commit()
        flash('New menu item created')
        return redirect(url_for('HomePage'))

    else:
        return render_template('newrestaurant.html')

@app.route('/<int:restaurant_id>/editname/', methods=['get','post'])
def editRestaurant(restaurant_id):
    editRest = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editRest.name = request.form['name']
        session.commit()
        flash('Restaurant edited')
        return redirect(url_for('HomePage'))

    else:
        return render_template('editrestaurant.html',restaurant_id=restaurant_id, editRest=editRest)

@app.route('/<int:restaurant_id>/deleterestaurant/', methods=['get','post'])
def deleteRestaurant(restaurant_id):
    restaurantdel = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurantdel)
        session.commit()
        flash('Restaurant deleted')
        return redirect(url_for('HomePage'))

    else:
        return render_template('deleterestaurant.html',restaurant_id=restaurant_id, restaurantdel=restaurantdel)

@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    item       = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html',restaurant=restaurant, items=item)


#Task 1: Create route for newMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/new/', methods=["GET","POST"])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name = request.form['name'],restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash('New menu item created')
        return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))

    else:
        return render_template('newmenuitem.html',restaurant_id=restaurant_id)

#Task 2: Create route for editMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/', methods=["GET","POST"])
def editMenuItem(restaurant_id, menu_id):
    editItem = session.query(MenuItem).filter_by(restaurant_id=restaurant_id,id = menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editItem.name = request.form['name']
        session.commit()
        flash('Item edited')
        return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))

    else:
        return render_template('editmenuitem.html',restaurant_id=restaurant_id,menu_id=menu_id, editItem=editItem)

#Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/', methods=["GET","POST"])
def deleteMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(restaurant_id=restaurant_id,id = menu_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash('Item deleted')
        return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))

    else:
        return render_template('deletemenuitem.html',restaurant_id=restaurant_id,menu_id=menu_id, item=item)




if __name__=='__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port = 5000)
