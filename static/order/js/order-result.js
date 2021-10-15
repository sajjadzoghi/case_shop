// remove sessionStorage all items

$('#order-id').html(`کد سفارش: ${sessionStorage.order_id}`);
$('#cart-modal .modal-body').empty();
$('#cart-quantity').html(0);
sessionStorage.removeItem('items');
sessionStorage.removeItem('total_price');
sessionStorage.removeItem('coupon_code');
sessionStorage.removeItem('coupon_amount');
sessionStorage.removeItem('total_price_coupon');
sessionStorage.removeItem('cart_quantity');
sessionStorage.removeItem('order_id');