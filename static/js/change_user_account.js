// Работа с авами
    const avatar = document.querySelector('#avatar');
    const avatarsBlock = document.querySelector('.block_new_avatars');

    // Сначала скрываем блок с аватарками
    avatarsBlock.style.display = 'none';
    avatarsBlock.style.opacity = '0';
    avatarsBlock.style.transition = 'opacity 0.3s ease';
    
    avatar.addEventListener('click', function(e) {
        e.stopPropagation();
        
        if (avatarsBlock.style.display === 'none') {
            avatarsBlock.style.display = 'flex';
            setTimeout(() => {
                avatarsBlock.style.opacity = '1';
            }, 10);
        } else {
            // Скрываем блок с аватарками
            avatarsBlock.style.opacity = '0';
            setTimeout(() => {
                avatarsBlock.style.display = 'none';
            }, 300);
        }
    });

    // Обработчик клика на документ - скрываем блок
    document.addEventListener('click', function() {
        if (avatarsBlock.style.display !== 'none') {
            avatarsBlock.style.opacity = '0';
            setTimeout(() => {
                avatarsBlock.style.display = 'none';
            }, 300);
        }
    });

    const avatarItems = document.querySelectorAll('.item-ava img');
    avatarItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.stopPropagation();
            
            const srcParts = this.src.split('/');
            const filename = srcParts[srcParts.length - 1];
            
            avatar.src = this.src;
            avatar.setAttribute('value', filename);
        });
    });

    // Предотвращаем закрытие при клике внутри блока аватарок
    avatarsBlock.addEventListener('click', function(e) {
        e.stopPropagation();
    });



const Btn_Save = document.querySelector('.btn_save_change');
Btn_Save.addEventListener("click", () => {
    // Получаем значения полей
    const lastname = document.querySelector('#lastname').value;
    const firstname = document.querySelector('#firstname').value;
    const patronymic = document.querySelector('#patronymic').value;
    const email = document.querySelector('#email').value;
    const phone = document.querySelector('#phone').value;
    const err = document.querySelector('.error');
    const ava = document.querySelector('.avatar').getAttribute('value');

    // Очищаем предыдущую ошибку
    err.textContent = '';

    // Проверка на пустые поля
    if (!lastname || !firstname || !patronymic || !email || !phone) {
        err.textContent = "Заполните все поля";
        return;
    }

    // Проверка на точки (по вашему примеру)
    if (lastname === '.' || firstname === '.' || patronymic === '.' || email === '.' || phone === '.') {
        err.textContent = "Некорректные данные";
        return;
    }

    // Простая проверка на запрещённые символы
    const badSymbols = ['&', '?'];
    for (let char of badSymbols) {
        if (lastname.includes(char) || firstname.includes(char) || patronymic.includes(char)) {
            err.textContent = `Уберите символ ${char} из полей`;
            return;
        }
    }

    // Отправка данных
    fetch(`/user_account/change/${lastname}/${firstname}/${patronymic}/${email}/${phone}/${ava}`)
        .then(response => {
            if (response.status === 404) {
                throw new Error('Страница не найдена');
            }
            return response.json();
        })
        .then(data => {
            if (data.status === 'success') {
                window.location.href = '/user_account';
            } else {
                err.textContent = data.error || 'Ошибка при сохранении';
            }
        })
        .catch(error => {
            if (error.message === 'Страница не найдена') {
                err.textContent = 'Ошибка загрузки. Обновите страницу.';
            } else {
                err.textContent = 'Произошла ошибка';
            }
        });
});