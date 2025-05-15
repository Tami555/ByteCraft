from flask import Blueprint, render_template, jsonify
from flask_login import current_user, login_required

from data.basket import Basket
from data.product import Product
from data.product_basket import Product_Basket

from data.db_session import create_session
from sqlalchemy import insert, update, and_, delete

blueprint = Blueprint('basket_api', __name__,template_folder='templates')


@blueprint.route('/shop/basket')
@login_required
def get_basket():
    ses = create_session()
    basket = ses.query(Basket).filter(Basket.IdUser == current_user.Id).first()
    products = []
    for product in basket.products:
        
        product_info = get_object_product(ses, product, basket)
       # Проверяем доступное количество
        if product_info['QuantityStock'] == 0:
            pass
        elif product_info['Quantity'] == 0 and product_info['QuantityStock'] > 0:
            # Товар снова в наличии, но в корзине Quantity=0 - устанавливаем 1
            ses.execute(
                Product_Basket.update()
                    .where(Product_Basket.c.IdBasket == basket.Id)
                    .where(Product_Basket.c.IdProduct == product.Id)
                    .values(Quantity=1)
                )
            product_info['Quantity'] = 1
        elif product_info['Quantity'] > product_info['QuantityStock']:
            # Количество в корзине больше, чем есть на складе - корректируем
            ses.execute(
                Product_Basket.update()
                    .where(Product_Basket.c.IdBasket == basket.Id)
                    .where(Product_Basket.c.IdProduct == product.Id)
                    .values(Quantity=product_info['QuantityStock'])
                )
            product_info['Quantity'] = product_info['QuantityStock']
            
        products.append(product_info)
        ses.commit()


    print(products)
    print('Корзинка подъехала!!!')
    return render_template('basket_page.html', product = products, title='ВАША КОРЗИНА:')


def get_object_product(ses, p: Product, basket:Basket):
    lst = {}
    lst['Id'] = p.Id
    lst['Title'] = p.Title
    lst['Image'] = p.Image
    lst['Cost'] = int(p.Cost)
    lst['QuantityStock'] = int(p.QuantityStock)
    prod_bask = ses.query(Product_Basket).filter(
            Product_Basket.c.IdBasket == basket.Id,
            Product_Basket.c.IdProduct == p.Id
        ).first()
    lst['Quantity'] = int(prod_bask.Quantity)
    lst['Background'] = p.category.Background
    lst['Color'] = p.category.Color
    return lst


# Получение количесвта товара в Корзине
def get_Quantity_IN_Basket(id):
    ses = create_session()
    try:
        print(f'Текущий пользователь -> {current_user}')
        basket = ses.query(Basket).filter(Basket.IdUser == current_user.Id).first()
        product = ses.query(Product).filter(Product.Id == id).first()

        prod_bask = ses.query(Product_Basket).filter(
            Product_Basket.c.IdBasket == basket.Id,
            Product_Basket.c.IdProduct == product.Id
        ).first()

        if prod_bask:
            return prod_bask.Quantity
        
        else:
            return 0

    except Exception as e:
        print(f'Хъюстан у нас проблемы, в чеке количества корзиных товаров - > {e}')
        return 0
    finally:
        ses.close()
    

# Добавляем запись
@blueprint.route('/shop/main_page/product_basket/add/<int:product_id>/<int:quantity>')
@login_required
def add_product_basket(product_id, quantity):
    print('Поступил запрос на Добавление/Обновление в КОРЗИНУ')
    ses = create_session()
    try:
        basket = ses.query(Basket).filter(Basket.IdUser == current_user.Id).first()
        # Проверяем, есть ли запись
        existing_product_basket = ses.query(Product_Basket).filter(
            Product_Basket.c.IdBasket == basket.Id,
            Product_Basket.c.IdProduct == product_id
        ).first()
        if existing_product_basket:
            # Если есть, обновляем Quantity
            operation = update(Product_Basket).where(
                and_(Product_Basket.c.IdBasket == basket.Id, Product_Basket.c.IdProduct == product_id)
            ).values(Quantity=quantity)
        else:
            # Если нет, создаем новую
            operation = insert(Product_Basket).values(
                IdBasket=basket.Id,
                IdProduct=product_id,
                Quantity=quantity
            )
        ses.execute(operation)
        ses.commit()
        return jsonify({'answer': 'Успешно !! Товар добавлен в корзину !!!'})
        
    except Exception as e:
        ses.rollback()
        print(f'Хъюстан у нас проблемы, при добавлении/обновлении товара - > {e}')
        return jsonify({'answer': f'ОШИБКА !!  При добавлении/обновлении товара в корзину !!! {str(e)}'}), 500
    finally:
        ses.close()


# Удалеие товара из корзины
@blueprint.route('/shop/main_page/product_basket/delete/<int:product_id>')
@login_required
def delete_product_basket(product_id):
    print('Поступил запрос на Удаление товара из КОРЗИНЫ')
    ses = create_session()
    try:
        basket = ses.query(Basket).filter(Basket.IdUser == current_user.Id).first()
        delete_stmt = delete(Product_Basket).where(
            and_(Product_Basket.c.IdBasket == basket.Id, Product_Basket.c.IdProduct == product_id)
        )
        result = ses.execute(delete_stmt)
        if result.rowcount == 0:
            return jsonify({'answer': 'Ошибка: Товар не найден в корзине'}), 404
        ses.commit()
        return jsonify({'answer': 'Успешно !! Товар удален из корзины !!!'})
    except Exception as e:
        ses.rollback()
        print(f'Хъюстан у нас проблемы, при удалении товара - > {e}')
        return jsonify({'answer': f'ОШИБКА !!  При удалении товара из корзины !!! {str(e)}'}), 500
    finally:
        ses.close()


