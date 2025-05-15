document.addEventListener('DOMContentLoaded', function() {
    // Переменная для хранения текущего рейтинга
    let currentRating = 0;
    const stars = document.querySelectorAll('.star');
    const ratingValue = document.getElementById('rating-value');
    let productsData;

    // КОМЕНТ 
    const commentInput = document.querySelector('.comment');
    const errorElement = document.querySelector('.error');
    const charCountElement = document.getElementById('char-count');
    
    // Функция для обновления отображения звезд
    function updateStars(rating) {
        stars.forEach(star => {
            const starValue = parseInt(star.getAttribute('data-value'));
            if (starValue <= rating) {
                star.src = "/static/img/great_star.png";
            } else {
                star.src = "/static/img/empty_star.png";
            }
        });
        ratingValue.textContent = rating;
    }
    
    // Обработчик клика по звезде
    stars.forEach(star => {
        star.addEventListener('click', function() {
            currentRating = parseInt(this.getAttribute('data-value'));
            updateStars(currentRating);
        });
    });
    
    // Для select и товаров
    try {
        const productsDataElement = document.getElementById('products-data');
        if (!productsDataElement) {
            throw new Error('Элемент с данными о продуктах не найден');
        }
        
        productsData = JSON.parse(productsDataElement.textContent.trim());
        const productsCount = productsData.count;
        
        async function loadProductData(productId) {
            try {
                const response = await fetch(`/shop/main_page/products/${productId}`);
                if (!response.ok) {
                    throw new Error('Ошибка получения данных');
                }
                const data = await response.json();
                
                document.getElementById('product-image').src = data.Image;
                document.getElementById('product-title').textContent = data.Title;
                document.getElementById('product-price').textContent = `${data.Cost} руб`;
                
                currentRating = 0;
                updateStars(currentRating);
                commentInput.value = '';
                errorElement.textContent = '';
                charCountElement.textContent = '0';
                commentInput.style.borderColor = '#0E9956';
            } catch (error) {
                console.error('Ошибка загрузки данных товара:', error);
                alert('Не удалось загрузить информацию о товаре');
            }
        }

        if (productsCount === 1 && productsData.singleProductId) {
            loadProductData(productsData.singleProductId);
        } else if (productsCount > 1) {
            const productSelect = document.getElementById('products');
            if (productSelect) {
                productSelect.addEventListener('change', function() {
                    const productId = this.value;
                    if (productId) {
                        loadProductData(productId);
                    }
                });
                
                if (productSelect.value) {
                    productSelect.dispatchEvent(new Event('change'));
                }
            }
        }
    } catch (error) {
        console.error('Ошибка инициализации:', error);
    }



commentInput.addEventListener('input', function() {
    const comment = this.value;
    const remainingChars = 500 - comment.length;
    
    // Обновляем счетчик символов
    charCountElement.textContent = comment.length;
    
    // Проверка на превышение лимита
    if (comment.length > 500) {
        errorElement.textContent = 'Превышен лимит в 500 символов!';
        this.style.borderColor = '#ff6b6b';
    } else {
        errorElement.textContent = '';
        this.style.borderColor = comment.length === 500 ? '#ffb347' : '#0E9956';
    }
});



// ОПУБЛИКОВАТЬ ОТЗЫВ

const addReviewBtn = document.querySelector('.add_review_btn');
const commentError = document.querySelector('.comment_error');

addReviewBtn.addEventListener('click', async function() {
    let productId;
    if (productsData.count === 1) {
        productId = productsData.singleProductId;
    } else {
        productId = document.getElementById('products').value;
    }

    // комментарий не пустой
    const comment = commentInput.value.trim();
    if (!comment) {
        commentError.textContent = 'Пожалуйста, напишите комментарий';
        return;
    } else {
        commentError.textContent = '';
    }

    //оценка выбрана
    if (currentRating === 0) {
        commentError.textContent = 'Пожалуйста, поставьте оценку';
        return;
    }

    try {
        // Кодируем комментарий для URL
        const encodedComment = encodeURIComponent(comment);
        
        // Отправляем 
        const response = await fetch(`/create_review/product/${productId}/${currentRating}/${encodedComment}`);
        
        if (response.ok) {
            // Успешная отправка
            window.location.href = `/get_reviews/product/${productId}`;
        } else {
            throw new Error('Ошибка сервера');
        }
    } catch (error) {
        console.error('Ошибка при отправке отзыва:', error);
        commentError.textContent = 'Произошла ошибка при отправке отзыва';
    }
});
});