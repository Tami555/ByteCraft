from flask import Blueprint, render_template, jsonify, make_response, redirect
from flask_login import current_user, login_required
from sqlalchemy.orm import joinedload
from data.db_session import create_session
from data.product import Product
from data.favorites import Favorites
from data.user import User
from sqlalchemy import  func, select
from blueprints.basket_api import get_Quantity_IN_Basket

blueprint = Blueprint('shop_api', __name__,template_folder='templates')

lst_product = []


@blueprint.route('/shop/main_page')
@login_required
def main_popular():
    ses = create_session()
    try:
        products = ses.query(Product).order_by(func.random()).limit(10).all()
        user = ses.query(User).filter(User.Id == current_user.Id).first()
        favorites = [x.Id for x in user.favorites]
        
        return render_template('products_page.html', 
                           title="POPULAR NOW:", 
                           products=products, 
                           favorites=favorites)
    except Exception as e:
        print(f"Error: {e}")
        return redirect('/')
    finally:
        ses.close()


@blueprint.route('/shop/main_page/products/<int:id>')
@login_required
def get_one_product(id):
    print('ПОЛУЧАЕТ ИНФУ О ТОВАРЕ')
    try:
        ses = create_session()
        product = ses.query(Product).filter(Product.Id == id).first()
        is_favorite = product.Id in [x.Id for x in current_user.favorites]
        quantity_in_basket = get_Quantity_IN_Basket(id)
        if product:
                return jsonify({
                    'Id': product.Id,
                    'Title': product.Title,
                    'Description': product.Description,
                    'TechnicalSpecifications': product.TechnicalSpecifications,
                    'QuantityStock' : product.QuantityStock,
                    'Cost': product.Cost,
                    'Image': product.Image,
                    'Seller' : product.seller.to_dict(), 
                    'Category': product.category.to_dict(),
                    'is_favorite': is_favorite, 
                    'quantity_in_basket': quantity_in_basket,
                    'Mark': round(sum([x.Mark for x in product.reviews]) / len(product.reviews), 2) if len(product.reviews) > 0 else "нет" 
                })
        else:
            return make_response(jsonify({'error': 'Not found'}), 404)
    except Exception as e:
        print('Ошибка в полной инфе')
        return make_response(jsonify({'error': 'Full error'}), 400)
    finally:
        ses.close()


# Поиск
@blueprint.route('/shop/products/found/<string:context>')
@login_required
def find_context(context):
    print('Мы начинаем искать !!!!')
    try:
        ses = create_session()
        pr = ses.query(Product).all()
        found_products = []
        
        for product in pr:
            if any([context.lower() in prr.lower() for prr in [product.Title,product.Description, product.TechnicalSpecifications]]):
                found_products.append(product)
        favorites = [x.Id for x in current_user.favorites]
        return render_template('products_page.html', products=found_products, favorites=favorites, search_query=context)
    
    except Exception as e:
         print(f'Ошибка{e}')
         return redirect('/')

    finally:
        ses.close()