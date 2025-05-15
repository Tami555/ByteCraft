# Работа с Каталoгом
from flask import Blueprint, render_template, jsonify, make_response, redirect
from flask_login import current_user
from data.db_session import create_session
from flask_login import login_required
from data.category import Category
from data.product import Product
blueprint = Blueprint('catalog_api', __name__, template_folder='templates')


@blueprint.route('/shop/catalog/show/all')
@login_required
def get_all_catalog():
    try:
        ses = create_session()
        categories = ses.query(Category).all()
        return render_template('catalogs_page.html', categories=categories)
    except Exception as e:
        print('Ошибка во всех категориях')
    finally:
        ses.close()

@blueprint.route('/shop/catalog/get_products/categore/<int:id_categore>')
@login_required
def get_product_By_categore(id_categore):
    try:
        ses = create_session()
        categore = ses.query(Category).filter(Category.Id == id_categore).first()
        lst_product = ses.query(Product).filter(Product.category == categore).all()
        favorites = [x.Id for x in current_user.favorites]
        return render_template('products_page.html', title=categore.Title, products=lst_product, favorites=favorites)
    except Exception as e:
        print(e)
        print('Ошибка во всех категориях')
        return redirect('/')
    finally:
        ses.close()
