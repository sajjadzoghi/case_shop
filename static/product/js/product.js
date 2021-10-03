// slide images of product
$('#img-1').css('display', '');

function currentDiv(n) {
    showDivs(slideIndex = n);
}

function showDivs(n) {
    var i;
    var x = document.getElementsByClassName("mySlides");
    var dots = document.getElementsByClassName("demo");
    if (n > x.length) {
        slideIndex = 1
    }
    if (n < 1) {
        slideIndex = x.length
    }
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace("w3-opacity-off", "");
    }
    x[slideIndex - 1].style.display = "block";
    dots[slideIndex - 1].className += " w3-opacity-off";
}


// quantity of product
let quantity = $('#quantity').val();
let inventory = $('#inventory').val();

function increaseValue() {
    if (inventory > quantity) {
        quantity++;
        $('#quantity').val(quantity);
    }
}

function decreaseValue() {
    if (quantity > 1) {
        quantity--;
        $('#quantity').val(quantity);
    }
}


// check if product is in SessionStorage
let product_id = $('#product-id').val();
let name = $('#name-fa').html();
let image = $('#image').val();
let color = $('#color').val();
let price = $('#price').val();
let guarantee = $('#guarantee').val();

if (sessionStorage.items) {
    let items = JSON.parse(sessionStorage.items);
    for (let item of items) {
        if (item.id === product_id) {
            $(`#add-product${product_id}`).prop('disabled', 'true').addClass('active');
        }
    }
}
// adding product to cart through "SessionStorage"
$(`#product-form`).submit(function (e) {
    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $(this);
    var product_data = {
        'id': product_id,
        'name': name,
        'image': image,
        'color': color,
        'quantity': quantity,
        'price': price,
        'guarantee': guarantee,
    };
    if (sessionStorage.cart_quantity) {
        sessionStorage.cart_quantity = Number(sessionStorage.cart_quantity) + 1;
    } else {
        sessionStorage.cart_quantity = 1;
    }
    $('#cart-btn').prop('disabled', '');
    $('#cart-quantity').html(sessionStorage.cart_quantity);


    if (sessionStorage.items) {
        let items = JSON.parse(sessionStorage.items);
        items.push(product_data);
        sessionStorage.items = JSON.stringify(items);
    } else {
        let items = [];
        items.push(product_data);
        sessionStorage.items = JSON.stringify(items);
    }

    $('#cart-modal .modal-body').prepend(`<div id="item${product_id}">
                        <div class="row" style="direction: rtl;margin-right: 1px">
                            <img alt="item" src="${image}">
                            <h5 class="text-dark" style="margin-top: 2rem;margin-right: 3px">${name}</h5>
                            <i onclick="remove_item(${product_id})" class="fa fa-fw fa-trash"
                               style="font-size: 32px;margin-right: auto;margin-left: 5px;margin-top: 1.6rem;cursor: pointer"></i>
                        </div>
                        <div class="row" style="direction: rtl;margin-right: 1px">
                            <p class="text-dark">${quantity} عدد</p>
                            <div style="height: 1.2rem;border: 0.001mm ridge grey;margin-right: 2rem;margin-left: 2rem;"></div>
                            <p class="text-dark">رنگ ${color}</p>
                        </div>
                        <h5 class="text-dark" style="direction: rtl">${price} میلیون تومان</h5>
                        <p>_____________________________________</p>
                    </div>`);

    $(`#add-product${product_id}`).prop('disabled', 'true').addClass('active');

});