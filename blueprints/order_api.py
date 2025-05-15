from datetime import datetime, timedelta
import random
import asyncio

from flask import Blueprint, render_template, jsonify
from flask_login import current_user, login_required
from data.db_session import create_session

from data.order import Order
from data.basket import Basket
from data.pick_up_point import PickUpPoint
from data.type_delivery import TypeDelivery
from data.user import User
from data.ordered_goods import Ordered_Goods
from data.cites import Cites

from external_API.send_email import send_email
import external_API.yandex_map_api as Yandex_Map_API
from .basket_api import get_object_product


blueprint = Blueprint('order_api', __name__,template_folder='templates')

# ЗАКАЗЫ ПОЛЬЗОВАТЕЛЯ
@blueprint.route('/user_orders')
@login_required
def get_already_orders():
    ses = create_session()
    orders = ses.query(Order).filter(Order.IdUser == current_user.Id).all()[::-1]
    orders = [get_full_order_infa(ses, order) for order in orders]
    return render_template('already_order.html', orders=orders, title="Мои покупки")


def get_full_order_infa(ses, order):
    # Полная инфа о заказе
    infa = {}
    infa['Id'] = order.Id
    infa['Summa'] = order.Summa
    infa['Data'] = order.Data.strftime("%d.%m.%Y %H:%M").replace(' ', ', ')
    infa['DateReceipt'] = order.DateReceipt.strftime("%d.%m.%Y %H:%M").split(' ')
    infa['Already'] = order.DateReceipt < datetime.now()
    infa['DeliveryAddress'] = order.DeliveryAddress
    infa['PickUpPoint'] = order.pickup.Title if order.pickup is not None else order.pickup
    infa['Delivery'] = order.delivery.Title

    products = []
    for p in order.products:
        infa_product = {}
        infa_product['product'] = p

        prod_bask = ses.query(Ordered_Goods).filter(
                Ordered_Goods.c.IdOrder == order.Id,
                Ordered_Goods.c.IdProduct == p.Id
            ).first()
        infa_product['quantity'] = int(prod_bask.Quantity)
        products.append(infa_product)

    infa['Products'] = products

    return infa


# Страница ОФОРМЛЕНИЯ ЗАКАЗА
@blueprint.route('/place_order')
@blueprint.route('/place_order/<string:delivery_type>/<string:address>')
@login_required
def place_order(address='-', delivery_type='-'):
    ses = create_session()
    try:
        basket = ses.query(Basket).filter(Basket.IdUser == current_user.Id).first()
        products = []
        for x in basket.products:
            if x.QuantityStock != 0:
                products.append(get_object_product(ses, x, basket))

        summa = sum([x['Quantity'] * x['Cost'] for x in products])

        # Работаем с типом доставки:
        pickup_selected = courier_selected = False

        if delivery_type != '-':
            cost = ses.query(TypeDelivery).filter(TypeDelivery.Title == delivery_type).first().Cost
            summa += cost
            delivery_cost = 'Бесплатно' if cost == 0 else f"{cost} рублей"

            match delivery_type:
                case "pickup":
                    pickup_selected = True
                case "courier":
                    courier_selected = True
        else:
            delivery_cost = '-'

        return render_template('place_order.html', products=products, summa=summa, address=address, delivery_cost=delivery_cost, pickup_selected=pickup_selected, courier_selected=courier_selected)

    except Exception as e:
        ses.rollback()
        print(f'Хъюстан у нас проблемы, при оформлении заказа - > {e}')
        return jsonify({'answer': f'ОШИБКА !! при оформлении заказа!!! {str(e)}'}), 500
    finally:
        ses.close()  


# Окно самовывоза 
@blueprint.route('/pickup')
@login_required
def get_pickup():
    print('Путь - САМОВЫВОЗ')
    try:
        cites = get_all_cites()
        selected_city = cites[0] if cites else None
        return render_template('pickup_way.html', cites=cites, selected_city=selected_city, title="Пункты Выдачи")
    except Exception as e:
        print(f'Ошибка ребят !! в самовывозе -> {e}')
        return jsonify({'answer': f'ОШИБКА !! в самовывозе!!! {str(e)}'}), 500


# Получаем пункты выдачи для определенного города
@blueprint.route('/get_cites_adress/<int:id>')
@login_required
def get_city_adress(id):
    print('Запрос на АДРЕСА !!!')
    try:
        ses = create_session()
        addresses = ses.query(PickUpPoint).filter(PickUpPoint.IdCity == id).all()
        print( [{adr.Id : adr.Title} for adr in addresses])
        return jsonify({"adress": [{adr.Id : adr.Title} for adr in addresses]})
    except Exception as e:
        print(f'Ошибка ребят !! в самовывозе, при получении адресов-> {e}')
        return jsonify({"adress": []})
    finally:
        ses.close()

# Получаем города
def get_all_cites():
    ses = create_session()
    cites = ses.query(Cites).all()
    ses.close()
    return cites


# Окно для Курьера (выбор своего адреса)
@blueprint.route('/courier')
@login_required
def get_courier():
    try:
        # Получаем метки пунктов выдачи ByteCraft
        coords_points = get_BC_markers()
        img_map = Yandex_Map_API.get_img_at_coord(bc_marks=coords_points)
        return render_template('сourier_way.html', title="Введите Адрес", img_map=img_map)
    
    except Exception as e:
        print(f'Ошибка ребят !! в курьере -> {e}')
        return jsonify({'answer': f'ОШИБКА !! в курьере!!! {str(e)}'}), 500
    

def get_BC_markers():
    # Получаем координаты всех пунктов выдачи для отображения меток
    try:
        ses = create_session()
        points = ses.query(PickUpPoint).all()
        # Получаем метки пунктов выдачи ByteCraft
        coords_points = [Yandex_Map_API.get_coord_at_address(adress.Title) for adress in points]
        return coords_points
        
    except Exception as e:
        print(f'Ошибка ребят !! при получении меток пунктов выдачи ByteCraft -> {e}')
    
    finally:
        ses.close()

# Получение адреса для курьера 
@blueprint.route('/img_map/<string:our_address>')
@login_required
def get_img_map(our_address=None):
    our_address = Yandex_Map_API.get_coord_at_address(our_address)
    city = Yandex_Map_API.get_city_at_address(our_address)
    # Метки bytecraft
    coords_points = get_BC_markers()

    names_city = [x.Title for x in get_all_cites()]
    
    if our_address is None:
        return jsonify({"error": 'Такой адрес не был найден !!!', "img_map": False})
    elif city not in names_city:
        return jsonify({"error": f'Доставка в город {city.capitalize()} пока не доступна!\n\nВыберете адрес в одном из следующих городов: {', '.join(names_city)}',
                         "img_map": False})
    else:
        img_map = Yandex_Map_API.get_img_at_coord(our_coords=our_address, bc_marks=coords_points) 
    
    return jsonify({"image": img_map})



# СОЗДАНИЕ ЗАКАЗА
@blueprint.route('/create_order/<string:dev_type>/<path:address>', methods=['POST'])
@login_required
def create_order(dev_type, address):
    if dev_type not in ['courier', 'pickup']:
        return jsonify({'status': 'error', 'message': 'Неверный тип доставки'})

    ses = create_session()
    try:
        basket = ses.query(Basket).filter(Basket.IdUser == current_user.Id).first()
        if not basket or not basket.products:
            return jsonify({'status': 'error', 'message': 'Корзина пуста'})
        
        products = []
        for x in basket.products:
            product = get_object_product(ses, x, basket)
            if product['QuantityStock'] < product['Quantity']:
                return jsonify({'status': 'error', 'message': f'Товар "{product["Title"]}" закончился!'})
            if product['QuantityStock'] != 0:
                products.append(product)

        summa = sum([x['Quantity'] * x['Cost'] for x in products])

        # Получаем тип доставки
        delivery_type = ses.query(TypeDelivery).filter(TypeDelivery.Title == dev_type).first()
        if not delivery_type:
            return jsonify({'status': 'error', 'message': 'Ошибка типа доставки'})
        
        summa += delivery_type.Cost

        user = ses.query(User).filter(User.Id == current_user.Id).first()
        if user.card.Id == 0:
            return jsonify({'status': 'error', 'message': 'Нет привязанной карты !'})
        if user.card.Balance < summa:
            return jsonify({'status': 'error', 'message': 'Недостаточно средств на карте'})

        # Списываем деньги
        user.card.Balance -= summa
        ses.add(user)

        # Обновляем товары и продавцов
        for i, pr in enumerate(basket.products):
            pr.QuantityStock -= products[i]['Quantity']
            pr.seller.Balance += products[i]['Quantity'] * pr.Cost
            ses.add(pr)

        # Создаем заказ
        order = Order()
        order.IdUser = user.Id
        order.Summa = summa
        order.Data, order.DateReceipt = get_current_and_future_datetime()
        shop_method = ses.query(TypeDelivery).filter(TypeDelivery.Title == dev_type).first()
        order.ShippingMethod = shop_method.Id

        if dev_type == 'courier':
            order.DeliveryAddress = address
        else:
            try:
                order.IdPickUpPoint = int(address)
            except ValueError:
                return jsonify({'status': 'error', 'message': 'Неверный ID пункта выдачи'})

        ses.add(order)
        ses.commit()

        # Добавляем товары в заказ
        for pr in basket.products:
            quantity = next(p['Quantity'] for p in products if p['Id'] == pr.Id)
            insert_stmt = Ordered_Goods.insert().values(
            IdOrder=order.Id,
            IdProduct=pr.Id,
            Quantity=quantity)
            ses.execute(insert_stmt)

        # Очищаем корзину
        basket.products = []
        ses.commit()

        # Отправляем письмо
        if dev_type != 'courier':
            address = ses.query(PickUpPoint).filter(PickUpPoint.Id == int(address)).first().Title

        try:
        # Создаем новую event loop для асинхронного вызова
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # Запускаем асинхронную функцию
            loop.run_until_complete(send_email(
                name=user.FirstName,
                delivery_date=order.DateReceipt,
                address=address,
                dev_type=dev_type,
                email=user.Email,
                number_order=order.Id
            ))
        except Exception as e:
            print("ОШИБКА ПРИ ОТПРВКИ ПИСЬМА")

        return jsonify({
            'status': 'success',
            'message': 'Заказ успешно оформлен',
            'order_id': order.Id
        })


    except Exception as e:
        print(f'ОШИБКА -> {e}')
        ses.rollback()
        return jsonify({
            'status': 'error',
            'message': 'Произошла ошибка при оформлении заказа'
        })
    finally:
        ses.close()



def get_current_and_future_datetime():
    """
    Возвращает текущую дату и время как объекты datetime
    """
    now = datetime.now()
    days_to_add = random.choice([3, 5, 7, 10])
    future_datetime = now + timedelta(days=days_to_add)
    
    return now, future_datetime 
