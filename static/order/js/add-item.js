// send the order-items to the database after submitting the order

$('#add-item-form').submit(function (e) {
        e.preventDefault(); // avoid to execute the actual submit of the form.

        var form = $(this);
        var url = form.attr('action');
        var form_data = form.serialize();

        $.ajax({
            type: "post",
            url: url,
            data: form_data,
            success: function () {
            },
        });
    });

sessionStorage.order_id = $('#id_order').val();
let items = JSON.parse(sessionStorage.items);
for (let item of items) {
    $('#id_product').val(item.product);
    $('#id_quantity').val(item.quantity);

    $('#add-item-form').submit();
}


$('#del-coupon').val(sessionStorage.coupon_code);
$('#del-coupon-form').submit();
