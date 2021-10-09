// remove sessionStorage

$('#order-id').html(`کد سفارش: ${sessionStorage.order_id}`)
sessionStorage.removeItem('items');
sessionStorage.removeItem('total_price');
sessionStorage.removeItem('cart_quantity');
// let order_id = $('#order-id').html();
// let items = JSON.parse(sessionStorage.items);
// for (let item of items) {
//     item.order = order_id;
//
//     let new_item = {
//         "product": Number(item.product),
//         "order": Number(item.order),
//         "quantity": Number(item.quantity)
//     }
//     console.log('********')
//     console.log(new_item)
//     console.log(typeof new_item)
//     console.log('********')
//
//     $.ajax({
//         type: "Post",
//         url: "http://127.0.0.1:8000/api/v1/orders/add-items/",
//         data: new_item,
//         success: function () {
//         }
//     })
// }
