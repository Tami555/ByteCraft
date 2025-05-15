from wtforms import StringField, EmailField, PasswordField, TelField, BooleanField
from flask_wtf import FlaskForm

import email_validator
from wtforms.validators import DataRequired, Email, ValidationError
import phonenumbers
from string import ascii_uppercase, ascii_lowercase


class RegistrationForm(FlaskForm):
    firstname = StringField('Имя', validators=[DataRequired("Введите Данные")])
    lastname = StringField('Фамилия', validators=[DataRequired("Введите Данные")])
    patronymic = StringField('Отчество', validators=[DataRequired("Введите Данные")])
    email = EmailField('Email',  validators=[DataRequired("Введите Данные"), Email("Некорректный Email")]) # выдает ошибку
    phone = TelField('Телефон', validators=[DataRequired("Введите Данные")])
    password = PasswordField('Пароль', validators=[DataRequired("Введите Данные")])
    repeat_password = PasswordField('Повторите пароль', validators=[DataRequired("Введите Данные")])
    remember_me = BooleanField('Запомнить меня')

    def validate_phone(self, phone):
        try:
            if phone.data[0] == '+':
                phone.data = phone.data[1:]
            phone_number = phonenumbers.parse(phone.data, "RU")
            if not phonenumbers.is_valid_number(phone_number):
                raise ValidationError("Недействительный номер телефона.")
            phone.data = phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164)
        except phonenumbers.phonenumberutil.NumberParseException:
            raise ValidationError("Некорректный формат номера телефона.")
        

    def validate_password(self, password):
        len_err = 'Длина пароля должна составлять не менее 9 символов.'
        digital_err = 'Пароль должен содержать цифры.'
        letter_err = "Пароль должен содержать символы разного регистра."
        parol = password.data

        if len(parol) < 9:
            raise ValidationError(len_err)
        if not any([x in list('1234567890') for x in parol]):
            raise ValidationError(digital_err)
        lst_e_b = ascii_uppercase
        lst_e_l = ascii_lowercase
        lst_r_l = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        lst_r_b = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'

        if (any(x in parol for x in lst_e_b) or any(x in parol for x in lst_r_b)) and \
            (any(x in parol for x in tuple(lst_e_l)) or any(x in parol for x in tuple(lst_r_l))):
            return True
        else:
            raise ValidationError(letter_err)    

