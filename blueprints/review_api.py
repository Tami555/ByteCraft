from datetime import datetime

from flask import Blueprint, render_template, jsonify, make_response
from urllib.parse import unquote
from flask_login import current_user, login_required
from data.db_session import create_session

from data.order import Order
from data.product import Product
from data.reviews import Reviews

blueprint = Blueprint('review_api', __name__,template_folder='templates')



# ОТЗЫВЫ на заказ (товары)
# ФОРМА НА СОЗДАНИЕ 
@blueprint.route('/create_review/<int:order_id>')
@login_required
def get_review(order_id):
    ses = create_session()
    order = ses.query(Order).filter(Order.Id == order_id).first()
    return render_template('add_review.html', products=order.products)

#САМО СОЗДАНИЕ 
@blueprint.route('/create_review/product/<int:product_id>/<int:mark>/<string:description>')
@login_required
def create_review(product_id, mark, description):
    try:
        ses = create_session()
        product = ses.query(Product).get(product_id)
        if not product:
            return make_response(jsonify({'error': 'Product not found'}), 404)
        
        if mark < 1 or mark > 5:
            return make_response(jsonify({'error': 'Invalid mark'}), 400)
        
        # Декодируем описание
        description = unquote(description)
        
        if len(description) > 500:
            return make_response(jsonify({'error': 'Description too long'}), 400)
            
        # Создаем отзыв
        review = Reviews(
            ProductId=product_id,
            Description=description,
            Mark=mark,
            UserId=current_user.Id,
            Data= datetime.now()
        )     
        ses.add(review)
        ses.commit()
        
        return make_response(jsonify({'success': True}), 200)
        
    except Exception as e:
        print(f'Ошибка при создании отзыва: {str(e)}')
        return make_response(jsonify({'error': 'Internal server error'}), 500)
    finally:
        ses.close()
    

# ВСЕ ОТЗЫВЫ ПО ТОВАРУ (страница)
@blueprint.route('/get_reviews/product/<int:product_id>')
@login_required
def get_reviews_product(product_id):
    ses = create_session()
    product = ses.query(Product).filter(Product.Id == product_id).first()
    reviews = product.reviews[::-1]
    print(f'ОТЗЫВЫ: {reviews}')
    try:
        all_mark = round(sum([x.Mark for x in reviews]) / len(reviews), 2)
    except ZeroDivisionError:
        all_mark = 0
    return render_template('reviews_products.html', product=product, reviews=reviews, main_mark=all_mark)