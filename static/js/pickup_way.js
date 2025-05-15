document.addEventListener('DOMContentLoaded', function() {

    // Получаем адреса пунктов выдачи по городам, для САМОВЫВОЗА
    const citySelect = document.getElementById('cites');
    const pickupContainer = document.querySelector('.cites_pick_up');
    
        // Функция для загрузки адресов
    function loadAddresses(cityId) {
        if (cityId) {
            pickupContainer.innerHTML = '<p class="loading">Загрузка пунктов выдачи...</p>';
            
            fetch(`/get_cites_adress/${cityId}`)
                .then(response => {
                    if (!response.ok) throw new Error('Ошибка сети');
                    return response.json();
                })
                .then(data => {
                    renderPickupPoints(data.adress);
                })
                .catch(error => {
                    console.error('Ошибка:', error);
                    pickupContainer.innerHTML = '<p class="error">Ошибка при загрузке адресов</p>';
                });
        }
        }
        
        // Загружаем адреса для выбранного города при загрузке страницы
        const initiallySelectedCityId = citySelect.value;
        if (initiallySelectedCityId) {
            loadAddresses(initiallySelectedCityId);
        }
        
        // Обработчик изменения города
        citySelect.addEventListener('change', function() {
            loadAddresses(this.value);
        });
    
        function renderPickupPoints(addresses) {
            // Очищаем контейнер
            pickupContainer.innerHTML = '';
            
            if (!addresses || addresses.length === 0) {
                // Если адресов нет
                const noAddressMsg = document.createElement('p');
                noAddressMsg.className = 'no-address';
                noAddressMsg.textContent = 'В этом городе пока нет пунктов выдачи :(';
                pickupContainer.appendChild(noAddressMsg);
                return;
            }
            
            // Получаем сохраненные данные из localStorage
            const savedAddress = localStorage.getItem('selectedPickupAddress');
            const savedAddressId = localStorage.getItem('selectedPickupAddress_Id');
        
            // Создаем радио-кнопки для каждого адреса
            addresses.forEach(addressObj => {
                const addressId = Object.keys(addressObj)[0];
                const addressText = addressObj[addressId];
                
                const wrapper = document.createElement('div');
                wrapper.className = 'input_way';
                
                const radio = document.createElement('input');
                radio.type = 'radio';
                radio.id = `address_${addressId}`;
                radio.name = 'way';
                radio.value = addressText;
                radio.dataset.addressId = addressId; // Сохраняем ID в data-атрибуте
        
                // Проверяем, совпадает ли сохраненный адрес с текущим
                if (savedAddress === addressText && savedAddressId === addressId) {
                    radio.checked = true;
                }
                
                const label = document.createElement('label');
                label.htmlFor = `address_${addressId}`;
                label.className = 'pickup_adress';
                label.textContent = addressText;
                
                // Добавляем обработчик изменения выбора
                radio.addEventListener('change', function() {
                    if (this.checked) {
                        localStorage.setItem('selectedPickupAddress', addressText);
                        localStorage.setItem('selectedPickupAddress_Id', addressId);
                    }
                });
                
                wrapper.appendChild(radio);
                wrapper.appendChild(label);
                pickupContainer.appendChild(wrapper);
            });
        }

    // Выбираем адрес для САМОВЫВОЗА
    document.querySelector('#pickup_adress_check')?.addEventListener('click', function() {
        const selectedAddress = document.querySelector('input[name="way"]:checked');
        if (selectedAddress) {
            
            // Сохраняем выбранный адрес в localStorage
            localStorage.setItem('selectedPickupAddress', selectedAddress.value);

            window.location.href = `/place_order/pickup/${selectedAddress.value}`;
            console.log('НОРМ АДРЕС !')
        } else {
            document.querySelector('.error').innerHTML = 'Выберете адрес, пожалуйста!'
        }
    });
});