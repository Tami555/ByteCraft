document.addEventListener('DOMContentLoaded', function() {
    // Функция обновления состояния кнопки "лайка"
    function updateLikeButton(productId, isFavorite) {
        const likeButtons = document.querySelectorAll(`.like[data-product-id="${productId}"]`);
        likeButtons.forEach(button => {
            button.src = isFavorite ? "/static/img/like.png" : "/static/img/no_like.png";
        });
    }

    // Обработчик кликов для всего документа
    document.addEventListener('click', function(event) {
        if (event.target.classList.contains('like')) {
            const likeButton = event.target;
            const productId = likeButton.dataset.productId || likeButton.getAttribute('data-product-id');
            let isFavorite = likeButton.src.includes('/like.png');

            const addToFavoritesUrl = `/shop/main_page/favorites/add/${productId}`;
            const removeFromFavoritesUrl = `/shop/main_page/favorites/delete/${productId}`;

            const newIsFavorite = !isFavorite;
            updateLikeButton(productId, newIsFavorite);

            const url = isFavorite ? removeFromFavoritesUrl : addToFavoritesUrl;

            fetch(url)
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'added') {
                        console.log(`Product ${productId} added to favorites`);
                    } else if (data.status === 'deleted') {
                        console.log(`Product ${productId} removed from favorites`);
                    } else {
                        // Если сервер вернул ошибку, возвращаем кнопку в исходное состояние
                        updateLikeButton(productId, isFavorite);
                        console.error(`Error: ${data.status || 'Unknown error'}`);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    updateLikeButton(productId, isFavorite);
                });
        }

        // РАБОТА С КОРЗИНОЙ
        // Добавить

        // else if (event.target.classList.contains('put_in_basket')) {
        //     const productId = event.target.dataset.productId;
        //     localStorage.setItem('quantity_in_basket', 1);
        //     fetch(`/shop/main_page/product_basket/add/${productId}/${1}`)
        //             .then(response => response.json())
        //             .then(json => console.log(json.answer))
                    
        //             // должны удалить кнопку "В корзину" на которую нажали
        //             // добавить вместо него, блок с классом div already_in_basket

        // }


        else if (event.target.classList.contains('put_in_basket')) {
            const productId = event.target.dataset.productId;
            const button = event.target; // Сохраняем ссылку на кнопку
            localStorage.setItem('quantity_in_basket', 1);
            
            fetch(`/shop/main_page/product_basket/add/${productId}/${1}`)
                .then(response => response.json())
                .then(json => {
                    console.log(json.answer);
                    
                    // Создаем блок "Добавлен"
                    const addedBlock = document.createElement('div');
                    addedBlock.className = 'already_in_basket';
                    addedBlock.textContent = 'Добавлен';
                    
                    // Заменяем кнопку на блок
                    button.parentNode.replaceChild(addedBlock, button);
                    
                    // Можно добавить анимацию
                    addedBlock.style.opacity = '0';
                    addedBlock.style.transition = 'opacity 0.3s ease';
                    setTimeout(() => {
                        addedBlock.style.opacity = '1';
                    }, 10);
                })
                .catch(error => {
                    console.error('Ошибка при добавлении в корзину:', error);
                    // Можно добавить уведомление об ошибке
                    button.textContent = 'Ошибка';
                    button.style.backgroundColor = '#ff6b6b';
                    setTimeout(() => {
                        button.textContent = 'В корзину';
                        button.style.backgroundColor = '#0E9956';
                    }, 2000);
                });
        }

    });
});