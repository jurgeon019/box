function add_cart_item(e){
    var item_id = e.target.dataset.item_id
    var input = document.querySelector('.add_item_to_cart_input')
    var quantity = '';
    if(input){
        quantity = input.value
    }
    var data = {
        "item_id":item_id,
        "quantity":quantity,
    }
    $.ajax({
        url:'/add_cart_item/',
        method:'POST',
        async:true, 
        data:data,
        success:function(data){
            get_cart_items()

        }
    })
}


function remove_cart_item(e){
    var cart_item_id = e.target.dataset.cart_item_id
    var data = {
        "cart_item_id":cart_item_id,
    }
    $.ajax({
        method:'POST',
        url:'/remove_cart_item/',
        data:data,
        success:function(e){
            get_cart_items()
        }
    })
}


function change_cart_item_quantity(e){
    var quantity = e.target.value
    var cart_item_id = e.target.dataset.cart_item_id
    var data = {
        'cart_item_id':cart_item_id,
        'quantity':quantity,
    }
    var cart_items_quantities = document.querySelectorAll('.cart_item_quantity')
    var cart_items_total_prices = document.querySelectorAll('.cart_item_total_price')
    $.ajax({
        method:'POST',
        url:'/change_cart_item_amount/',
        async:true, 
        data:data,
        success:function(data){
            console.log(data)
            cart_items_quantities.forEach(function(cart_item_quantity){
                if(cart_item_quantity.dataset.cart_item_id == cart_item_id){
                    cart_item_quantity.innerHTML=quantity
                }
            })
            cart_items_total_prices.forEach(function(cart_item_total_price){
                if(cart_item_total_price.dataset.cart_item_id == cart_item_id){
                    cart_item_total_price.innerHTML=data['cart_item_total_price']
                }
            })
            var cart_total_price    = data['cart_total_price']
            var cart_items_count    = data['cart_items_count']
            var cart_items_quantity = data['cart_items_quantity']
            document.querySelector('.cart_total_price').innerHTML = cart_total_price
            document.querySelector('.cart_items_count').innerHTML = cart_items_count
            document.querySelector('.cart_items_quantity').innerHTML = cart_items_quantity

        }
    })
}


function get_cart_items(){
    var data = {}
    $.ajax({
        url:'/get_cart_items/',
        method:'POST',
        async:true,
        data:data, 
        success:function(data){
            console.log(data)
            var cart_total_price    = data['cart_total_price']
            var cart_items_count    = data['cart_items_count']
            var cart_items_quantity = data['cart_items_quantity']
            document.querySelector('.cart_total_price').innerHTML = cart_total_price
            document.querySelector('.cart_items_count').innerHTML = cart_items_count
            document.querySelector('.cart_items_quantity').innerHTML = cart_items_quantity
            
            var cart_items          = data['cart_items']
            var cart_items_html = '';
            cart_items.forEach(function(cart_item){
                cart_items_html += 
                `
                <br/>
                <h2>Товар в корзині:</h2>
                <p>id: ${cart_item.id}</p>
                <p>Назва: ${cart_item.item.title}</p>
                <p>Вартість: ${cart_item.item.price}</p>
                <p>Кількість товару в корзині: 
                    <span data-cart_item_id="${cart_item.id}" class="cart_item_quantity">
                        ${cart_item.quantity}
                    </span>
                </p>
                <p>Сумарна вартість товару в корзині:
                    <span data-cart_item_id="${cart_item.id}" class="cart_item_total_price">
                        ${cart_item.total_price}
                    </span> 
                </p>
                <input  
                    data-cart_item_id="${cart_item.id}" 
                    class="change_cart_item_quantity" 
                    type="number" 
                    value="${cart_item.quantity}" name="quantity" min="1" 
                />
                <input 
                    data-cart_item_id="${cart_item.id}" 
                    class="remove_cart_item_from_cart_button"
                    type="button"
                    value="Remove Cart Item From Cart"
                />
                <br/>
                `
            })
            document.querySelector('.cart_items_list').innerHTML = cart_items_html
            
            $('.remove_cart_item_from_cart_button').click(remove_cart_item)
            $('.change_cart_item_quantity').on('change', change_cart_item_quantity)

        }
    })
}


function get_items(){
    var category = document.querySelector('.category_slug').value;
    var data = {
        "category":category,
    }
    $.ajax({
        url:'/get_items/',
        method:'POST',
        async:true,
        data:data,
        success:function(data){
            var json_items = data['json_items']
            var shop_items_list = document.querySelector('.shop_items_list')
            console.log(shop_items_list)
            var items_html = ''
            var text = '';
            // console.log(json_items)
            json_items.forEach(function(item){
                text  = 'Add To Cart';
                class_ = 'add_item_to_cart_button';
                // if(data.items_in_cart.includes(item.id)){
                //     text = 'Remove from Cart'
                //     class_ = 'remove_cart_item_from_cart_button'
                // }
                items_html += `
                <br/>
                <h2>Товар на сайті</h2>
                <p>Назва: <a href="/test_item/${item.slug}/">${item.title}</a></p>
                <p>Ціна: ${item.price}</p>
                <p>Категорія: ${item.category.title}</p>
                <button data-item_id=${item.id} class="${class_}">${text}</button>
                <br/>
                `
            })
            shop_items_list.innerHTML = items_html
            $('.add_item_to_cart_button').on('click', add_cart_item)
        }
    })
}


document.addEventListener('DOMContentLoaded', function(){
    get_items()
    get_cart_items()
    $('.add_item_to_cart_button').on('click', add_cart_item)
})





