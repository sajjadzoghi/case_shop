// remove sessionStorage all items

$('#order-id').html(`کد سفارش: ${sessionStorage.order_id}`);
$('#cart-modal .modal-body').empty();
$('#cart-quantity').html(0);
sessionStorage.removeItem('items');
sessionStorage.removeItem('total_price');
sessionStorage.removeItem('cart_quantity');
sessionStorage.removeItem('coupon');
sessionStorage.removeItem('order_id');