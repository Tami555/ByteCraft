from flask import Blueprint, render_template, redirect, jsonify
from flask_login import current_user, login_required
from data.db_session import create_session
from data.user import User
from data.card import Card

blueprint = Blueprint('card_api', __name__, template_folder='templates')


@blueprint.route('/shop/user_card/')
@blueprint.route('/shop/user_card/<page>/')
def get_user_card(page=None):
    ses = create_session()
    user = ses.query(User).filter(User.Id == current_user.Id).first()
    UserCard = user.card

    if UserCard.CardNumber == 0:
        print('Еще нет карты')
    else:
        print(f'Есть,  - > {UserCard.CardNumber}')

    if page == 'add_update':
        template = 'add_update_card.html'
    else:
        template = 'user_card.html' 

    return render_template(template, title='Ваша Карта', card=UserCard)


@blueprint.route('/shop/user_card/add_update/<string:cardNumber>/<string:period>/<string:code>')
def add_update_card(cardNumber, period, code):
    try:
        period = period.replace(' ', '/')
        ses = create_session()
        user = ses.query(User).filter(User.Id == current_user.Id).first()
        if user.card.CardNumber == 0:
            print('Карты нет, Создаем')
            new_card = Card()
            new_card.CardNumber = int(cardNumber)
            new_card.Code = int(code)
            new_card.Period = period
            new_card.Balance = 0.00
            ses.add(new_card)
            user.card = new_card
            ses.add(user)
            ses.commit()
        else:
            print('Карта уже есть, обновляем')
            user.card.CardNumber = int(cardNumber)
            user.card.Code = int(code)
            user.card.Period = period
            ses.add(user)
            ses.commit()
        print('ВСЕ НОООРМ !!!')
        return jsonify({'status': 'okay card'})
    except Exception as e:
        return jsonify({'status': f'error ->  {e}'})
    finally:
        ses.close()


@blueprint.route('/shop/user_card/replenish_balanse/<int:money>')
def replenish_balanse(money):
    try:
        print('ПОПОЛЕНИЕ УРААА !!!')
        ses = create_session()
        user = ses.query(User).filter(User.Id == current_user.Id).first()
        user.card.Balance = user.card.Balance + money
        ses.add(user)
        ses.commit()
        return jsonify({'status': 'okay card'})
    except Exception as e:
        return jsonify({'status': f'error ->  {e}'})
    finally:
        ses.close()
    