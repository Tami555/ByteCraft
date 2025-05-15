document.addEventListener('DOMContentLoaded', function () {

    const MoneyBlock = document.querySelector('.money_block');
    const ReplenishBalanceDiv = document.querySelector('.replenish_balsnse');
    const overlayDiv = document.createElement('div');

    const Balance_btn = document.querySelector('.btn_replenish_balsnse');
    
    overlayDiv.classList.add('overlay');
    document.body.appendChild(overlayDiv);


    MoneyBlock.addEventListener('click', function(event) {
        if (event.target.classList.contains('put_money')) {
            event.preventDefault();
            ReplenishBalanceDiv.classList.add('show');
            overlayDiv.classList.add('show');
        }
    });

    overlayDiv.addEventListener('click', ()=> {
        ReplenishBalanceDiv.classList.remove('show');
        overlayDiv.classList.remove('show');
    });

    Balance_btn.addEventListener('click', ()=>{
        const money = document.getElementById('balance').value;
        const user_balance = document.querySelector('.balanse');
        const parsedMoney = parseFloat(money);

        if (isNaN(parsedMoney) || parsedMoney <= 0 || isNaN(money)) {
            document.getElementById('err_balance').textContent = 'введите корректную сумму пополнения ';
            return; 
        }
        else if (parsedMoney > 100000){
            document.getElementById('err_balance').textContent = 'сумма слишком большая!!!';
            return; 
        }
        else{
            document.getElementById('err_balance').textContent = '';
        }
        const url = `/shop/user_card/replenish_balanse/${money}`;
        fetch(url)
        const currentBalanceText = user_balance.textContent;
        const currentBalance = parseFloat(currentBalanceText.replace(' рублей', ''));

        if (isNaN(currentBalance)) {
            console.error("Не удалось получить текущий баланс пользователя.");
            document.getElementById('err_balance').textContent = 'Ошибка при получении текущего баланса.';
            return;
        }
        const newBalance = currentBalance + parsedMoney;
        user_balance.textContent = newBalance + ' рублей';

        ReplenishBalanceDiv.classList.remove('show');
        overlayDiv.classList.remove('show');
    })
});