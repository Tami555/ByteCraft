document.addEventListener('DOMContentLoaded', function() {
    const contentDiv = document.querySelector('.content');

    contentDiv.addEventListener('click', function(event) {
        if (event.target.classList.contains('plus')){
            console.log('Корзина плюсует')
            const productId = event.target.dataset.productId;
            console.log('ПЛЮС В КОРЗИНЕ РАБОТАЕТ')
                const plusButton = event.target;
                const counter_value = document.querySelector(`.value-${productId}`);
    
                const product_quantity = parseInt(plusButton.getAttribute('data-product-quantity'))
                let quantity = parseInt(counter_value.textContent)
    
                console.log(`В КОРЗИНЕ -> ${quantity}, А ВСЕГО -> ${product_quantity}`)
    
                if (quantity < product_quantity){
                    // plusButton.style.backgroundColor = '#D9D9D9'; // Проблема с цветом
                    plusButton.classList.remove('disabled');
                    quantity += 1;
                    counter_value.innerHTML = `${quantity}`;
                    update_final_price()
                    fetch(`/shop/main_page/product_basket/add/${productId}/${quantity}`)
                                .then(response => response.json())
                                .then(json => console.log(json.answer))
                }
                else{
                    plusButton.classList.add('disabled');
                    plusButton.disabled = true;
                }
            }

            else if (event.target.classList.contains('minus')){
                   console.log('Корзина минусует')
                    const productId = event.target.dataset.productId;
                    const plusButton = document.querySelector(`.plus-${productId}`)
                    // plusButton.style.backgroundColor = '#D9D9D9';
                    plusButton.classList.remove('disabled');
                    const minusButton = event.target;
                    const counter_value = document.querySelector(`.value-${productId}`);
        
                    let quantity = parseInt(counter_value.textContent)
                
                    if (quantity > 1){
                        quantity -= 1;
                        counter_value.innerHTML = `${quantity}`;
                        update_final_price()
                        fetch(`/shop/main_page/product_basket/add/${productId}/${quantity}`)
                                    .then(response => response.json())
                                    .then(json => console.log(json.answer))
                    }
                    else{
                        // Удаление
                        console.log('Удаляем');
                        fetch(`/shop/main_page/product_basket/delete/${productId}`)
                            .then(response => response.json())
                            .then(json => console.log(json.answer))
                            window.location.href = `/shop/basket`;
                    }
                }

            else if (event.target.closest('.delete_product')) {
                console.log('Удаляем');
                const deleteButton = event.target.closest('.delete_product');
                const productId = deleteButton.dataset.productId;
            
                fetch(`/shop/main_page/product_basket/delete/${productId}`)
                    .then(response => response.json())
                    .then(json => console.log(json.answer))
                    window.location.href = '/shop/basket';
            }
            
            function update_final_price() {
                const productBlocks = document.getElementsByClassName('product_block');
                let totalPrice = 0;
            
                for (let i = 0; i < productBlocks.length; i++) {
                    const productBlock = productBlocks[i];
            
                    const priceElement = productBlock.querySelector('.price');
                    let price = 0; 
            
                    if (priceElement) {
                        const priceText = priceElement.textContent.replace(/[^0-9.]/g, ''); // Очищаем от лишних символов
                        price = parseFloat(priceText); 
                    }
            
                    const quantityElement = productBlock.querySelector(`.value_counter`);
                    let quantity = 0;
            
                    if (quantityElement) { 
                        quantity = parseInt(quantityElement.textContent); 
                    }
            
                    if (!isNaN(price) && !isNaN(quantity)) {
                        totalPrice += price * quantity;
                    } else {
                        console.warn("Не удалось получить цену или количество для товара:", productBlock);
                    }
                }
                const finalPriceElement = document.querySelector('.final_price');
                finalPriceElement.textContent = `ИТОГ: ${totalPrice} руб`;            
                console.log("Общая стоимость покупки:", totalPrice);
            }
    });
});