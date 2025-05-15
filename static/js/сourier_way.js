document.addEventListener('DOMContentLoaded', function() {
    let check_address = false;
    const addressInput = document.querySelector('#our_adress');
    const foundButton = document.querySelector('.btn_found');
    const errorElement = document.querySelector('.error');
    
    // Следим за изменениями в поле адреса
    addressInput?.addEventListener('input', function() {
        check_address = false; // Сбрасываем флаг проверки при любом изменении адреса
        foundButton.classList.remove('highlight'); // Убираем подсветку кнопки
    });

    // Проверка адреса через API карт
    foundButton?.addEventListener('click', function() {
        const our_adress = addressInput.value;

        if (our_adress != ''){
            fetch(`/img_map/${our_adress}`)
                .then(response => {
                    if (!response.ok) throw new Error('Ошибка сети');
                    return response.json();
                })
                .then(data => {
                    if (data.image){
                        document.querySelector('.map_img').src = data.image;
                        errorElement.innerHTML = '';
                        check_address = true;
                        foundButton.classList.remove('highlight'); // Убираем подсветку после успешной проверки
                    }
                    else{
                        errorElement.innerHTML = data.error;
                        addressInput.value = '';
                        check_address = false;
                    }
                })
                .catch(error => {
                    console.error('Ошибка:', error);
                    errorElement.innerHTML = 'Ошибка при загрузке адресов';
                });
        }
    });

    // Выбор адреса для курьера
    document.querySelector('#сourier_adress_check')?.addEventListener('click', function() {
        const our_adress = addressInput.value;
        if (our_adress != '') {
            if (check_address){
                window.location.href = `/place_order/courier/${our_adress}`;
                console.log('НОРМ АДРЕС !');
            }
            else{
                errorElement.innerHTML = 'Проверьте свой адрес на корректность с помощью карты, пожалуйста!';
                foundButton.classList.add('highlight'); // Подсвечиваем кнопку проверки
                
                // Добавляем анимацию "прыгания" на 3 секунды
                foundButton.classList.add('jump');
                setTimeout(() => {
                    foundButton.classList.remove('jump');
                }, 3000);
            }
        } else {
            errorElement.innerHTML = 'Выберете адрес, пожалуйста!';
        }
    });
});