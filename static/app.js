
let cart = [];

function showMenu() {
    const menuDiv = document.getElementById('menu');
    const dishesItemsDiv = document.getElementById('dishes-items');
    const drinksItemsDiv = document.getElementById('drinks-items');
    const dessertsItemsDiv = document.getElementById('desserts-items');
    menuDiv.style.display = 'block';
    dishesItemsDiv.innerHTML = '';
    drinksItemsDiv.innerHTML = '';
    dessertsItemsDiv.innerHTML = '';

    dishesItems.forEach(item => {
        const menuItemDiv = document.createElement('div');
        menuItemDiv.classList.add('menu-item');
        menuItemDiv.innerHTML = `
            <img src="${item.img}" alt="${item.name}">
            <div>
                <h3>${item.name}</h3>
                <p>${item.price} FC</p>
                <button onclick="addToCart(${item.id}, 'dish')">Ajouter au Panier</button>
            </div>
        `;
        dishesItemsDiv.appendChild(menuItemDiv);
    });

    drinksItems.forEach(item => {
        const menuItemDiv = document.createElement('div');
        menuItemDiv.classList.add('menu-item');
        menuItemDiv.innerHTML = `
            <img src="${item.img}" alt="${item.name}">
            <div>
                <h3>${item.name}</h3>
                <p>${item.price} FC</p>
                <button onclick="addToCart(${item.id}, 'drink')">Ajouter au Panier</button>
            </div>
        `;
        drinksItemsDiv.appendChild(menuItemDiv);
    });

    dessertsItems.forEach(item => {
        const menuItemDiv = document.createElement('div');
        menuItemDiv.classList.add('menu-item');
        menuItemDiv.innerHTML = `
            <img src="${item.img}" alt="${item.name}">
            <div>
                <h3>${item.name}</h3>
                <p>${item.price} FC</p>
                <button onclick="addToCart(${item.id}, 'dessert')">Ajouter au Panier</button>
            </div>
        `;
        dessertsItemsDiv.appendChild(menuItemDiv);
    });
}

function addToCart(itemId, category) {
    let item;
    if (category === 'dish') {
        item = dishesItems.find(i => i.id === itemId);
    } else if (category === 'drink') {
        item = drinksItems.find(i => i.id === itemId);
    } else if (category === 'dessert') {
        item = dessertsItems.find(i => i.id === itemId);
    }
    cart.push(item);
    alert(`${item.name} a été ajouté au panier.`);
}

function viewCart() {
    const cartDiv = document.getElementById('cart');
    const cartItemsDiv = document.getElementById('cart-items');
    const totalPriceSpan = document.getElementById('total-price');
    cartDiv.style.display = 'block';
    cartItemsDiv.innerHTML = '';

    let totalPrice = 0;
    cart.forEach(item => {
        totalPrice += item.price;
        const cartItemDiv = document.createElement('div');
        cartItemDiv.classList.add('cart-item');
        cartItemDiv.innerHTML = `
            <div>
                <h3>${item.name}</h3>
                <p>${item.price} FC</p>
            </div>
        `;
        cartItemsDiv.appendChild(cartItemDiv);
    });

    totalPriceSpan.textContent = totalPrice;
}

function placeOrder() {
    const tableNumber = prompt("Entrez votre numéro de table:");
    if (tableNumber) {
        fetch('/place-order', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({tableNumber, cart})
        }).then(response => {
            if (response.ok) {
                alert("Commande passée avec succès!");
                cart = [];
                document.getElementById('cart').style.display = 'none';
            } else {
                alert("Une erreur s'est produite. Veuillez réessayer.");
            }
        });
    }
}
