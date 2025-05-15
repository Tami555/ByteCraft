document.addEventListener('DOMContentLoaded', function() {
    const youPoint = document.getElementById('you_p');
    const dropdownMenu = document.querySelector('.dropdown');
    const menu = document.querySelector('.menu');
    const mainPoint = document.getElementById('main_p');
    const catalogPoint = document.getElementById('catalog_p');
    const basketPoint = document.getElementById('basket_p');
    const menuPoints = [mainPoint, catalogPoint, basketPoint];
    let isMobile = window.matchMedia("(max-width: 768px)").matches;

    // Функция для закрытия меню
    function closeDropdown() {
        dropdownMenu.style.display = 'none';
        youPoint.style.backgroundColor = '#396a53';
        document.body.classList.remove('menu-open');
    }

    // Обработчик клика по кнопке пользователя
    youPoint.addEventListener('click', function(e) {
        e.stopPropagation();
        e.preventDefault();

        // Переключаем видимость меню
        const isOpen = dropdownMenu.style.display === 'flex';
        dropdownMenu.style.display = isOpen ? 'none' : 'flex';
        document.body.classList.toggle('menu-open', !isOpen);

        // Убираем background у других элементов меню
        menuPoints.forEach(point => {
            if (point) {
                point.style.backgroundColor = '#396a53';
            }
        });

        if (!isOpen) {
            youPoint.style.backgroundColor = '#0E9956';
            if (!isMobile) {
                youPoint.style.borderRadius = '10px 0px 0px 10px';
            }
        } else {
            youPoint.style.backgroundColor = '#396a53';
        }
    });

    // Закрываем меню при клике вне меню
    document.addEventListener('click', function(event) {
        if (!event.target.closest('#you_p') && !event.target.closest('.dropdown')) {
            closeDropdown();
        }
    });
    // Закрываем меню при прокрутке (только для мобильной версии)
    if (isMobile) {
        menu.addEventListener('scroll', function() {
            if (dropdownMenu.style.display === 'flex') {
                closeDropdown();
            }
        });
    }
    // Обработчик изменения размера окна
    window.addEventListener('resize', function() {
        isMobile = window.matchMedia("(max-width: 768px)").matches;
    });
});