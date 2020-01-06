from shop.cart.api.help import help as cart_help 
from shop.item.api.help import help as item_help 


help = {
    'cart':    cart_help, 
    'item':    item_help, 
}
help = {}
help.update(cart_help)
help.update(item_help)