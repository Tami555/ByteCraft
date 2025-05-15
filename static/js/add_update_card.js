document.addEventListener('DOMContentLoaded', function () {

    const btnSafeCard = document.querySelector('.btn_safe_card');
    btnSafeCard.addEventListener('click', function () {
        //номер карты
        const cardNumberInputs = document.querySelectorAll('.card-number');
        
        let cardNumber = '';
        for (let i = 0; i < cardNumberInputs.length; i++) {
            cardNumber += cardNumberInputs[i].value;
        }
        // срок действия
        const periodMonth = document.querySelector('.period-month').value;
        const periodYear = document.querySelector('.period-year').value;
        const period = periodMonth + '/' + periodYear;

        //CVV/CVC
        const code = document.querySelector('input[name="code"]').value;

        //Валидация
        let isValid = true;

        //Валидация номера карты
        if (!/^\d{16}$/.test(cardNumber)) {
            document.getElementById('err_number').textContent = 'Неверный номер карты';
            isValid = false;
        } else {
            document.getElementById('err_number').textContent = '';
        }

        //Валидация срока действия
        if (!/^\d{2}\/\d{2}$/.test(period) || parseInt(periodMonth) > 12 || parseInt(periodYear) < 25) {
            document.getElementById('err_period').textContent = 'Неверный срок действия';
            isValid = false;
        } else {
            document.getElementById('err_period').textContent = '';
        }

        //Валидация кода
        if (!/^\d{3}$/.test(code)) {
            document.getElementById('err_code').textContent = 'Неверный код';
            isValid = false;
        } else {
            document.getElementById('err_code').textContent = '';
        }

        //Отправка
        if (isValid) {
            console.log('Проверки прошли !!')
            console.log(`Kарта: ${cardNumber}, ${period}, ${code}`)
            const url = `/shop/user_card/add_update/${cardNumber}/${period.replace('/', ' ')}/${code}`;
            fetch(url)
            window.location.href = `/shop/user_card`;
        }
    });
});