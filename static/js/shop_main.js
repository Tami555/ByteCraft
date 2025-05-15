    
document.addEventListener('DOMContentLoaded', function() {
    const contentDiv = document.querySelector('.content');  // Получаем родительский контейнер
    const finderDiv = document.querySelector('.finder');
    const mainProductDiv = document.querySelector('.main_one_product');
    const overlayDiv = document.createElement('div');
    overlayDiv.classList.add('overlay');
    document.body.appendChild(overlayDiv);


    function updateLikeButton(productId, isFavorite) {
        const likeButtons = document.querySelectorAll(`.like[data-product-id="${productId}"]`); 
        likeButtons.forEach(button => {
            button.src = isFavorite ? "/static/img/like.png" : "/static/img/no_like.png";
        });
    }

    const updateBasketDisplay = (productId) => {
        fetch('/shop/main_page/products/' + productId) 
                .then(response => response.json())
                .then(product => {
                    const isFavorite = product.is_favorite;
                    const quantity = product.quantity_in_basket;
                    localStorage.setItem('quantity_in_basket', quantity); // Добавляем в локалку
                    mainProductDiv.style.background = `linear-gradient(#2A2A2A, ${product.Category.Background})`;
                    mainProductDiv.innerHTML = `
                        <img class="like" src="${isFavorite ? '/static/img/like.png' : '/static/img/no_like.png'}" data-product-id="${product.Id}">
                        <img class="img_one_product" src="${product.Image}">
                        <h3 class="zagol_1">${product.Title}</h3>
                        <a href="/get_reviews/product/${productId}">
                            <div class="mark_block" style="width: 250px">
                                <p>Отзывы</p>
                                <img src="/static/img/great_star.png">
                                <p class="mark">${product.Mark}</p>
                            </div>
                        </a>
                        <p class="zagol_1">Цена: ${product.Cost}</p>
                        <div>
                            <p class="zagol_2">Описание:</p>
                            <p class="simple" style="color: ${product.Category.Color}">${product.Description}</p>
                        </div>
                        <div>
                            <p class="zagol_2">Технические характеристики:</p>
                            <p class="simple" style="color: ${product.Category.Color}">${product.TechnicalSpecifications}</p>
                        </div>
                        <div>
                            <p class="zagol_2">Категория:</p>
                            <p class="simple" style="color: ${product.Category.Color}">${product.Category.Title}</p>
                        </div>
                        <div>
                            <p class="zagol_2">Продавец:</p>
                            <p class="simple" style="color: ${product.Category.Color}">${product.Seller.FirstName} ${product.Seller.LastName}</p> 
                        </div>

                        ${product.QuantityStock ?
                            `<p class="zagol_1" >В наличии: ${product.QuantityStock}</p>`:
                            `<p></p>`
                        }
                        ${product.QuantityStock ?
                            (quantity ? 
                                `<div class='btns_basket'>
                                    <button class='put_in_basket_already' data-product-id="${product.Id}">Добавлен</button>
                                    <div class='counter'>
                                        <div class='plus' data-product-quantity="${product.QuantityStock}">+</div>
                                        <div class='value'>${quantity}</div>
                                        <div class='minus' data-product-quantity="${product.QuantityStock}" data-product-id="${product.Id}">-</div>
                                    </div>
                                </div>`
                                :
                                `<button class="put_in_basket" style="background: ${product.Category.Color}" data-product-id="${product.Id}"> В корзину</button>`)
                            :
                            `<p class="zagol_1" style="color: red;">Товара нет в наличии</p>`
                        }
                        <img class="close" src="https://cdn0.iconfinder.com/data/icons/phosphor-light-vol-4/256/triangle-light-256.png">
                    `;

                    // Отображение main_one_product и overlay
                    mainProductDiv.classList.add('show');
                    overlayDiv.classList.add('show');
                    const CloseImg = document.querySelector('.close');
                    
                    overlayDiv.addEventListener('click', ()=> {
                        const q = parseInt(localStorage.getItem('quantity_in_basket'));
                        if (q > 0){
                            fetch(`/shop/main_page/product_basket/add/${product.Id}/${q}`)
                            .then(response => response.json())
                            .then(json => console.log(json.answer))
                        }
                        mainProductDiv.classList.remove('show');
                        overlayDiv.classList.remove('show');
                    }, { once: true });

                    CloseImg.addEventListener('click', ()=> {
                        const q = parseInt(localStorage.getItem('quantity_in_basket'));
                        if (q > 0){
                            fetch(`/shop/main_page/product_basket/add/${product.Id}/${q}`)
                            .then(response => response.json())
                            .then(json => console.log(json.answer))
                        }
                        mainProductDiv.classList.remove('show');
                        overlayDiv.classList.remove('show');
                    }, { once: true });

                })
                .catch(error => {
                    console.error('Ошибка при загрузке информации о продукте:', error);
                });
            }

    // ПОИСК
    const searchInput = document.querySelector('.finder input[type="text"]');
    const searchButton = document.querySelector('.btn_find');

    const findIcon = "/static/img/find.png"; // поиск
    const noFindIcon = "/static/img/no_find3.png"; //сброс
    let isSearching = false; 

    function performSearch() {
        const searchTerm = searchInput.value.trim();

        if (searchTerm !== '') {
            const encodedSearchTerm = encodeURIComponent(searchTerm);
            window.location.href = `/shop/products/found/${encodedSearchTerm}`;
            isSearching = true;
            searchButton.src = noFindIcon; 
            searchInput.value = searchTerm;
        }
    }

    function resetSearch() {
        window.location.href = '/shop/main_page'; 
        isSearching = false;
        searchButton.src = findIcon;
        searchInput.value = ''; 
    }

    function handleSearchButtonClick() {
        if (!isSearching) {
            performSearch();
        } else {
            resetSearch();
        }
    }
    if (searchInput.value) {
        isSearching = true;
        searchButton.src = noFindIcon;
    }
    searchButton.addEventListener('click', handleSearchButtonClick);
    searchInput.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            performSearch();
        }
    });


    // ПОЛНАЯ ИНФА ТОВАРА
    contentDiv.addEventListener('click', function(event) {
        if (event.target.classList.contains('dop_infa_product')) {
            const productId = event.target.dataset.productId;
            updateBasketDisplay(productId);
        }

        // ИЗБРАННЫЕ LIKE
        else if (event.target.classList.contains('like')) {
            const likeButton = event.target;
            const productId = likeButton.getAttribute('data-product-id');
            let isFavorite = likeButton.src.endsWith('/static/img/like.png');

            const addToFavoritesUrl = `/shop/main_page/favorites/add/${productId}`;
            const removeFromFavoritesUrl = `/shop/main_page/favorites/delete/${productId}`;

            const newIsFavorite = !isFavorite;
            updateLikeButton(productId, newIsFavorite); // Обновляем все кнопки
            // Отправляем AJAX запрос
            const url = isFavorite ? removeFromFavoritesUrl : addToFavoritesUrl;

            fetch(url)
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'added') {
                        console.log(`Product ${productId} added to favorites`);
                    } else if (data.status === 'deleted') {
                        console.log(`Product ${productId} removed from favorites`);
                    } else if (data.status === 'already_in_favorites') {
                        console.log(`Product ${productId} already in favorites`);
                    }  else if (data.status === 'not_in_favorites') {
                        console.log(`Product ${productId} not in favorites`);
                    }
                     else {
                        console.error(`Error: ${data.status}`);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    updateLikeButton(productId, isFavorite);
                });
        }

        // РАБОТА С КОРЗИНОЙ
        // Добавить
        else if (event.target.classList.contains('put_in_basket')) {
            const productId = event.target.dataset.productId;
            localStorage.setItem('quantity_in_basket', 1);
            fetch(`/shop/main_page/product_basket/add/${productId}/${1}`)
                    .then(response => response.json())
                    .then(json => console.log(json.answer))
                    // ОБНОВИТЬ ИНТЕРФЕЙС (так как товар вообще был добавлен)
                    updateBasketDisplay(productId);
        }


        // ДОБАВЛЕН
        else if (event.target.classList.contains('put_in_basket_already')) {
            console.log('Переход на вкладку с корзиной');
            const productId = event.target.dataset.productId;
            const q = parseInt(localStorage.getItem('quantity_in_basket'));
                        if (q > 0){
                            fetch(`/shop/main_page/product_basket/add/${productId}/${q}`)
                            .then(response => response.json())
                            .then(json => console.log(json.answer))
                        }
            window.location.href = `/shop/basket`;
        }

        // ПЛЮС
        else if (event.target.classList.contains('plus')){
            console.log('ПЛЮС РАБОТАЕТ')
            const plusButton = event.target;
            const product_quantity = parseInt(plusButton.getAttribute('data-product-quantity'))
            let quantity = parseInt(localStorage.getItem('quantity_in_basket'))

            const counter_value = document.querySelector('.value');

            console.log(`В КОРЗИНЕ -> ${quantity}, А ВСЕГО -> ${product_quantity}`)
            console.log(typeof(quantity), typeof(product_quantity))
            if (quantity < product_quantity){
                quantity += 1;
                localStorage.setItem('quantity_in_basket', quantity);
                counter_value.innerHTML = `${quantity}`;
            }
            else{
                plusButton.disabled = true;
            }
        }

        // МИНУС
        else if (event.target.classList.contains('minus')){
            console.log('МИНУС РАБОТАЕТ')
            const MinusButton = event.target;
            const productId = MinusButton.getAttribute('data-product-id');
            let quantity = parseInt(localStorage.getItem('quantity_in_basket'))
            const counter_value = document.querySelector('.value');
            console.log(`В КОРЗИНЕ -> ${quantity}`)

            if (quantity > 1){
                quantity -= 1;
                localStorage.setItem('quantity_in_basket', quantity);
                counter_value.innerHTML = `${quantity}`;
            }
            else{
                // Удалить товар, если количестов меньше 1
                console.log('Удалить из корзины')
                fetch(`/shop/main_page/product_basket/delete/${productId}`)
                    .then(response => response.json())
                    .then(json => console.log(json.answer))
                 // ОБНОВИТЬ ИНТЕРФЕЙС (так как товар вообще удален)
                 updateBasketDisplay(productId);
            }
        }
    });
});