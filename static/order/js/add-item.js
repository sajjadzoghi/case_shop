// send the order-items to the database after submitting the order

sessionStorage.order_id = $('#order-id').html();
let items = JSON.parse(sessionStorage.items);
for (let item of items) {
    $('#order').val(sessionStorage.order_id);
    $('#product').val(item.product);
    $('#quantity').val(item.quantity);

    $('#add-item-form').submit();
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
}