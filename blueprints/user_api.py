import re

from flask import Blueprint, render_template, jsonify, make_response, redirect
from flask_login import current_user, login_required, logout_user

from data.db_session import create_session
from data.user import User
from data.order import Order

from main import avatars

blueprint = Blueprint('user_api', __name__,template_folder='templates')



@blueprint.route('/user_account')
@login_required
def get_our_user():
    ses = create_session()
    user = ses.query(User).filter(User.Id == current_user.Id).first()
    purchases = ses.query(Order).filter(Order.IdUser == current_user.Id).count()
    return render_template("user_account.html", user=user, purchases = purchases)



@blueprint.route('/user_account/change')
@login_required
def change_profile():
    ses = create_session()
    user = ses.query(User).filter(User.Id == current_user.Id).first()
    return render_template("change_user_account.html", user=user, avatars_img=avatars)



@blueprint.route('/user_account/change/<string:lastname>/<string:firstname>/<string:pat>/<string:email>/<string:phone>/<string:img>')
@login_required
def change_profile_data(lastname, firstname, pat, email, phone, img):
    ses = create_session()
    user = ses.query(User).filter(User.Id == current_user.Id).first()
    try:
        user.LastName = lastname
        user.FirstName = firstname
        user.Patronymic = pat
        # проверка на корректнось почты
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return jsonify({'status': 'error', 'error': 'Введена некорректная почта !'})
        user.Email = email
        # корректность телефона
        if not is_correct_mobile_phone_number_ru(phone):
            return jsonify({'status': 'error', 'error': 'Введен некорректный номер телефона!'})
        user.PhoneNumber = phone
        # Ава
        if img not in avatars:
            return jsonify({'status': 'error', 'error': 'Проблемы с аватаркой!'})
        user.Image_Avatar = img
        
        ses.add(user)
        ses.commit()
        return jsonify({'status': 'success'})  

    except Exception as e:
        print(f'Ошибка у нас в аккаунте: {e}')
        return jsonify({'status': 'error', 'error': 'Ошибка при изменении'})

    finally:
        ses.close()


# выход из аккауета
@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect('/start')



def is_correct_mobile_phone_number_ru(number: str):
    try:
        number = number.replace(' ', '')
        number = number.replace('-', '')
        if number[0] == '8' or (number[0] == '+' and number[1] == '7'):
            number = number[1:] if number[0] == '8' else number[2:]
        # Трехзначный код
            if number[0] == '(' and number[4] == ')' and [int(x) for x in number[1:4]]:
                number = number[5:]
            elif [int(x) for x in number[0:3]]:
                number = number[3:]
            else:
                return False

            return True if len(number) == 7 and [int(x) for x in number] else False
        else:
            return False
    except Exception:
        return False
