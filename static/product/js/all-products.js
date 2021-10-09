// jQuery & AJAX for showing products list with pagination

let content = $('.products-row');
let pagination = $('.pagination');

$.ajax({
    type: "Get",
    url: "http://127.0.0.1:8000/api/v1/products/",
    dataType: "json",
    success: function (resp) {
        for (let product of resp.results) {
            $(content).append(`<div class="card col-3">
                <img class="card-img-top" src="${product.images[0].image}" alt="Card image">
                <div class="card-body">
                    <p class="card-text" style="direction: rtl">${product.name_fa}</p>
                    <div class="row" style="margin-left: 2px;height: 3rem">
                        <i class="fa fa-fw fa-star" style="color: yellow;font-size: 15px;margin-top: 7px"></i>
                        <h4>${product.rate_average}</h4>
                        <p style="margin-top: 4px">(${product.voters_number}دیدگاه)</p>
                    </div>
                    <div class="row" style="margin-left: 1rem;height: 1.5rem">
                        <h5><del id="price${product.id}">&nbsp${product.price}</del></h5>
                    </div>
                    <div class="row" style="margin-left: 3px">
                        <p style="margin-top: 3px">تومان</p>
                        <h3 id="final-price${product.id}">&nbsp${product.final_price}</h3>
                    </div>
                    <a href="${product.id}" class="stretched-link"></a>
                </div>
            </div>`);

            let price = $(`#price${product.id}`).html();
            $(`#price${product.id}`).html(numberWithCommas(price));
            let final_price = $(`#final-price${product.id}`).html();
            $(`#final-price${product.id}`).html(numberWithCommas(final_price));
            if (price === final_price) {
                $(`#price${product.id}`).html('<br>');
            }
        }

        $(pagination).append(`<button id="previous" class="page" onclick="page('${resp.previous}')">&laquo;</button>`)
        for (let i = 1; i <= resp.num_pages; i++) {
            if (i === 1) {
                $(pagination).append(`
                    <button class="active" onclick="page('http://127.0.0.1:8000/api/v1/products/?page=${i}')" disabled>${i}</button>`)
            } else {
                $(pagination).append(`
                    <button class="page" onclick="page('http://127.0.0.1:8000/api/v1/products/?page=${i}')">${i}</button>`)
            }
        }
        $(pagination).append(`<button id="next" class="page" onclick="page('${resp.next}')">&raquo;</button>`);

        $('#previous').prop('disabled', true);
    }
});

function page(url) {
    if (url != null) {
        $.ajax({
            type: "Get",
            url: `${url}`,
            dataType: "json",
            success: function (resp) {
                $(content).empty();
                for (let product of resp.results) {
                    $(content).append(`<div class="card col-3">
                        <img class="card-img-top" src="${product.images[0].image}" alt="Card image">
                        <div class="card-body">
                            <p class="card-text" style="direction: rtl">${product.name_fa}</p>
                            <div class="row" style="margin-left: 2px;height: 3rem">
                                <i class="fa fa-fw fa-star" style="color: yellow;font-size: 15px;margin-top: 7px"></i>
                                <h4>${product.rate_average}</h4>
                                <p style="margin-top: 4px">(${product.voters_number}دیدگاه)</p>
                            </div>
                            <div class="row" style="margin-left: 1rem;height: 1.5rem">
                                <h5><del id="price${product.id}">&nbsp${product.price}</del></h5>
                            </div>
                            <div class="row" style="margin-left: 3px">
                                <p style="margin-top: 3px">تومان</p>
                                <h3 id="final-price${product.id}">&nbsp${product.final_price}</h3>
                            </div>
                            <a href="${product.id}" class="stretched-link"></a>
                        </div>
                    </div>`);

                    let price = $(`#price${product.id}`).html();
                    $(`#price${product.id}`).html(numberWithCommas(price));
                    let final_price = $(`#final-price${product.id}`).html();
                    $(`#final-price${product.id}`).html(numberWithCommas(final_price));
                    if (price === final_price) {
                        $(`#price${product.id}`).html('<br>');
                    }
                }

                $(pagination).empty();
                $(pagination).append(`<button class="page" id="previous" onclick="page('${resp.previous}')">&laquo;</button>`)
                for (let i = 1; i <= resp.num_pages; i++) {
                    $(pagination).append(`
                        <button class="page" onclick="page('http://127.0.0.1:8000/api/v1/products/?page=${i}')">${i}</button>`)
                }
                $(pagination).append(`<button id="next" class="page" onclick="page('${resp.next}')">&raquo;</button>`);

                if (url === 'http://127.0.0.1:8000/api/v1/products/') {
                    url = 'http://127.0.0.1:8000/api/v1/products/?page=1';
                }

                $('.page').each(function () {
                    if ($(this).attr('onclick') === `page('${url}')`) {
                        $(this).attr('class', 'active');
                        $(this).prop('disabled', true);
                    }
                });

                if (resp.next == null) {
                    $('#next').prop('disabled', true);
                } else if (resp.previous == null) {
                    $('#previous').prop('disabled', true);
                }
            }
        });
    }
}

function numberWithCommas(x) {
    return x.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
}