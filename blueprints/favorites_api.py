from flask import Blueprint, render_template, jsonify, make_response, redirect
from flask_login import current_user, login_required

from data.db_session import create_session
from data.user import User
from data.basket import Basket
from data.product import Product

blueprint = Blueprint('favorites_api', __name__,template_folder='templates')


@blueprint.route('/favorites')
@login_required
def get_favorites_product():
    lst_products = []
    ses = create_session()
    # мы
    user = ses.query(User).filter(User.Id == current_user.Id).first()
    # избранные
    favorites = user.favorites
    # в корзине
    basket = ses.query(Basket).filter(Basket.IdUser == current_user.Id).first()

    for product in favorites:
        lst_products.append(get_object_product(ses, product, basket))
    return render_template('favorites_page.html', products=lst_products, title="Избранные: ")


def get_object_product(ses, p: Product, basket:Basket):
    lst = {}
    lst['Id'] = p.Id
    lst['Title'] = p.Title
    lst['Image'] = p.Image
    lst['Cost'] = int(p.Cost)
    lst['QuantityStock'] = int(p.QuantityStock)
    lst['in_basket'] = p not in basket.products
    lst['Background'] = p.category.Background
    lst['Color'] = p.category.Color
    return lst


@blueprint.route('/shop/main_page/favorites/add/<int:id>')
@login_required
def add_favorites(id):
    ses = create_session()
    try:
        product = ses.query(Product).filter(Product.Id == id).first()
        if product in current_user.favorites:
            return jsonify({'status': 'already_in_favorites'})
        
        user = ses.query(User).filter(User.Id == current_user.Id).first()
        user.favorites.append(product)
        ses.add(user)   
        ses.commit()
        return jsonify({'status': 'added'})
    except Exception as e:
        ses.rollback()  # Откатываем транзакцию в случае ошибки
        return jsonify({'status': f'error: {str(e)}'})
    finally:
        ses.close()
      

@blueprint.route('/shop/main_page/favorites/delete/<int:id>')
@login_required
def delete_favorites(id):
    ses = create_session()
    try:
        product = ses.query(Product).filter(Product.Id == id).first()
        user = ses.query(User).filter(User.Id == current_user.Id).first()
        if product not in user.favorites:
            return jsonify({'status': 'not_in_favorites'})
        user.favorites.remove(product)
        ses.add(user)
        ses.commit()
        return jsonify({'status': 'deleted'})
    except Exception as e:
        ses.rollback()  # Откатываем транзакцию в случае ошибки
        return jsonify({'status': f'error: {str(e)}'})
    finally:
        ses.close()