$.ajax({
    type: "Get",
    url: "/api/v1/categories/",
    dataType: "json",
    success: function (resp) {
        for (let category of resp) {
            $('.dropdown-cat').append(`<a href="/category/${category.id}">${category.name}<i class="fa fa-fw fa-${category.icon}"></i></a>`);
        }
    }
});


if (sessionStorage.cart_quantity) {
    $('#cart-quantity').html(sessionStorage.cart_quantity);
} else {
    $('#cart-quantity').html(0);
}

if (sessionStorage.total_price) {
    if (sessionStorage.total_price !== '0') {
        $('#cart-total-price').html(`
            جمع
            کل: ${Number(sessionStorage.total_price)} تومان`);
    } else {
        $('#cart-total-price').hide();
        $('#cart-btn-group').hide();
        $('#cart-modal .modal-body').prepend(` < h4
            id = "is-empty" > !سبد
            خرید
            شما
            خالی
            است < /h4>`);
        $('#cart-modal .modal-body').append(`<button type="button" id="empty-button" class="btn btn-danger" data-dismiss="modal">بستن</button>`);
    }
} else {
    $('#cart-total-price').hide();
    $('#cart-btn-group').hide();
    $('#cart-modal .modal-body').prepend(`<h4 id="is-empty">!سبد خرید شما خالی است</h4>`);
    $('#cart-modal .modal-body').append(`<button type="button" id="empty-button" class="btn btn-danger" data-dismiss="modal">بستن</button>`);
}

if (sessionStorage.items) {
    let items = JSON.parse(sessionStorage.items);
    for (let item of items) {
        $('#cart-modal .modal-body').prepend(`<div id="item${item.product}">
                    <div class="row" style="direction: rtl;margin-right: 1px">
                        <img alt="item" src="${item.image}">
                        <h5 class="text-dark" style="margin-top: 2rem;margin-right: 3px">${item.name}</h5>
                        <i onclick="remove_item('${item.product}')" class="fa fa-fw fa-trash"
                           style="font-size: 32px;margin-right: auto;margin-left: 5px;margin-top: 1.6rem;cursor: pointer"></i>
                    </div>
                    <div class="row" style="direction: rtl;margin-right: 1px">
                        <p class="text-dark">${item.quantity} عدد</p>
                        <div style="height: 1.2rem;border: 0.001mm ridge grey;margin-right: 2rem;margin-left: 2rem;"></div>
                        <p class="text-dark">رنگ ${item.color}</p>
                        <div style="height: 1.2rem;border: 0.001mm ridge grey;margin-right: 2rem;margin-left: 2rem;"></div>
                        <p class="text-dark">قیمت واحد: ${item.price} تومان</p>
                    </div>
                    <h5 class="text-dark" style="direction: rtl">قیمت نهایی: ${Number(item.price) * Number(item.quantity)} تومان</h5>
                    <p>_____________________________________________</p>
                </div>`);
    }
}

function remove_item(id) {
    sessionStorage.removeItem('coupon_code');
    sessionStorage.removeItem('coupon_amount');
    sessionStorage.removeItem('total_price_coupon');
    let items = JSON.parse(sessionStorage.items);
    let new_items = [];
    let new_total = 0;
    for (let item of items) {
        if (item.product !== id) {
            new_items.push(item);
            new_total += (Number(item.price) * Number(item.quantity));
        }
    }
    items = new_items;
    sessionStorage.items = JSON.stringify(items);
    sessionStorage.total_price = new_total;
    $('#cart-total-price').html(`جمع کل: ${sessionStorage.total_price} تومان`);


    $(`#cart-modal #item${id}`).remove();
    $(`#add-product${id}`).prop('disabled', '').removeClass('active');

    $('#coupon-btn').prop('disabled', '');
    $('#coupon').prop('disabled', '');
    $('#coupon-form p').remove();
    $('.tbl-after').remove();
    $('#table-total').show();
    $('#table-total').html(` مبلغ کل سفارش : ${sessionStorage.total_price} تومان`);
    $(`table #item${id}`).remove();


    sessionStorage.cart_quantity = Number(sessionStorage.cart_quantity) - 1;
    $('#cart-quantity').html(sessionStorage.cart_quantity);
    if (sessionStorage.cart_quantity === '0') {
        $('#cart-total-price').hide();
        $('#cart-btn-group').hide();
        $('#cart-modal .modal-body').prepend(`<h4 id="is-empty">!سبد خرید شما خالی است</h4>`);
        $('#cart-modal .modal-body').append(`<button type="button" id="empty-button" class="btn btn-danger" data-dismiss="modal">بستن</button>`);
        sessionStorage.removeItem('items');
        window.location.href = "/"
    }
}


// I.R.Iran provinces and cities for handling all kind of "address-forms" in all pages
let provinces = {
    'آذربایجان شرقی': ['آذرشهر', 'اسکو', 'اهر', 'بستان‌آباد', 'بناب', 'تبریز', 'جلفا', 'چاراویماق', 'سراب', 'شبستر', 'عجب‌شیر', 'کلیبر', 'مراغه', 'مرند', 'ملکان', 'میانه', 'ورزقان', 'هریس', 'هشترود'],
    'اصفهان': ['آران و بیدگل', 'اردستان', 'اصفهان', 'برخوار و میمه', 'تیران و کرون', 'چادگان', 'خمینی‌شهر', 'خوانسار', 'سمیرم', 'شهرضا', 'سمیرم سفلی', 'فریدن', 'فریدون‌شهر', 'فلاورجان', 'کاشان', 'گلپایگان', 'لنجان', 'مبارکه', 'نائین', 'نجف‌آباد', 'نطنز'],
    'تهران': ['اسلام‌شهر', 'پاکدشت', 'تهران', 'دماوند', 'رباط‌کریم', 'ری', 'ساوجبلاغ', 'شمیرانات', 'شهریار', 'فیروزکوه', 'کرج', 'نظرآباد', 'ورامین'],
    'خراسان رضوی': ['بردسکن', 'تایباد', 'تربت جام', 'تربت حیدریه', 'چناران', 'خلیل‌آباد', 'خواف', 'درگز', 'رشتخوار', 'سبزوار', 'سرخس', 'فریمان', 'قوچان', 'کاشمر', 'کلات', 'گناباد', 'مشهد', 'مه ولات', 'نیشابور'],
    'زنجان': ['ابهر', 'ایجرود', 'خدابنده', 'خرمدره', 'زنجان', 'طارم', 'ماه‌نشان'],
    'سمنان': ['دامغان', 'سمنان', 'شاهرود', 'گرمسار', 'مهدی‌شهر'],
    'قزوین': ['آبیک', 'البرز', 'بوئین‌زهرا', 'تاکستان', 'قزوین'],
    'یزد': ['ابرکوه', 'اردکان', 'بافق', 'تفت', 'خاتم', 'صدوق', 'طبس', 'مهریز', 'مِیبُد', 'یزد'],
}

$('.province').append(`<option value="">--استان--</option>`);
for (let province in provinces) {
    $('.province').append(`<option value="${province}">${province}</option>`);
}

function Func(chosen_province) {
    for (let province in provinces) {
        if (province === chosen_province) {
            $('.city').empty();
            $('.city').append(`<option value="">--شهر--</option>`);
            for (let city of provinces[province]) {
                $('.city').append(`<option value="${city}">${city}</option>`);
            }
        }
    }
}