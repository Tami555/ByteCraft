document.addEventListener('DOMContentLoaded', function() {
    const wayRadios = document.querySelectorAll('input[name="way"]');
    // Отправляем на страницу выбора адреса
    wayRadios.forEach(radio => {
        radio.addEventListener('click', function() {
            if (this.checked) {
                window.location.href = `/${this.value}`;
                this.checked = false;
                document.querySelector('#adress_id').innerHTML = '-';
                document.querySelector('#delivery_id').innerHTML = '-';
            }
        });
    });

// ЗАКАЗ делаем
const Btn_Buy = document.querySelector('.buy_products_finish');
const Courier = document.querySelector('input[id="courier"]'); 
const Pickup = document.querySelector('input[id="pickup"]');
const noCheckError = document.querySelector('.no_check_error');

// Для окна
const modalOverlay = document.querySelector('.modal-overlay');
const messageBlock = document.querySelector('.message_finish_block');
const imgAnswer = document.querySelector('.img_answer');
const statusText = document.querySelector('.status');
const messageText = document.querySelector('.message');
const btnFurther = document.querySelector('.btn_further');

Btn_Buy.addEventListener('click', async () => {
    noCheckError.innerHTML = '';
    
    try {
        if (Courier.checked) {
            const address = document.querySelector('#adress_id')?.textContent.trim();
            if (!address) {
                noCheckError.innerHTML = 'Укажите адрес доставки!';
                return;
            }
            
            const response = await fetch(`/create_order/courier/${encodeURIComponent(address)}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            const result = await response.json();
                if (result.status === 'success') {
                    showMessage(true);
                } else {
                    showMessage(false, result.message);
                }
            
        } else if (Pickup.checked) {
            const pickupId = localStorage.getItem('selectedPickupAddress_Id');
            if (!pickupId) {
                noCheckError.innerHTML = 'Выберите пункт выдачи!';
                return;
            }
            
            const response = await fetch(`/create_order/pickup/${pickupId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            const result = await response.json();
                if (result.status === 'success') {
                    showMessage(true);
                } else {
                    showMessage(false, result.message);
                }
            
        } else {
            noCheckError.innerHTML = 'Выберите способ доставки!';
        }
    } catch (error) {
        console.error('Ошибка:', error);
        showMessage(false, 'Произошла ошибка при оформлении заказа');
    }
});


//для показа сообщения
function showMessage(isSuccess, message = '') {
    if (isSuccess) {
        messageBlock.classList.add('success');
        messageBlock.classList.remove('error');
        imgAnswer.src = 'https://cdn0.iconfinder.com/data/icons/round-ui-icons/512/tick_green.png';
        statusText.textContent = 'УСПЕШНО';
        messageText.textContent = 'Спасибо за заказ !!!';
        btnFurther.textContent = 'Продолжить покупки';
        btnFurther.classList.add('success');
        btnFurther.classList.remove('error');
    } else {
        messageBlock.classList.add('error');
        messageBlock.classList.remove('success');
        imgAnswer.src = 'https://cdn4.iconfinder.com/data/icons/essentials-72/24/039_-_Cross-256.png';
        statusText.textContent = 'ОШИБКА';
        messageText.textContent = message || 'Произошла ошибка';
        btnFurther.textContent = 'Отмена';
        btnFurther.classList.add('error');
        btnFurther.classList.remove('success');
    }

    modalOverlay.classList.add('active');
    messageBlock.classList.add('active');
}


// Закрытие окна
function closeModal(isSuccess) {
    modalOverlay.classList.remove('active');
    messageBlock.classList.remove('active');
    
    // Перенаправление
    setTimeout(() => {
        if (isSuccess) {
            window.location.href = '/shop/main_page';
        } else {
            window.location.href = '/shop/basket';
        }
    }, 300);
}

// Обработчики закрытия
modalOverlay.addEventListener('click', () => {
    const isSuccess = messageBlock.classList.contains('success');
    closeModal(isSuccess);
});

btnFurther.addEventListener('click', () => {
    const isSuccess = messageBlock.classList.contains('success');
    closeModal(isSuccess);
});

});