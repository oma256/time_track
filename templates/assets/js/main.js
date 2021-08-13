// ============search==============

$(document).ready(function () {
    let input = $(".search-block form .input input");
    let searchResultBlock = $('#search-result__content_id');

    input.on("input", function () {
        if (input.val().length === 0) {
            input.siblings(".searchBut").css("display", 'block');
            input.siblings(".close-search").css("display", 'none');
        } else {
            input.siblings(".searchBut").css("display", 'none');
            input.siblings(".close-search").css("display", 'block');
            searchResultBlock.css('display', 'block');
        }
    });

    input.on("focus", function () {
        input.css({
            "border": "1px",
            "border-style": "solid",
            "border-color": "#6A4B93",
        });
    });

    input.on("blur", function () {
        input.css({
            "border": "1px",
            "border-style": "solid",
            "border-color": "transparent",
        });
        input.siblings(".searchBut").css("display", 'block');
        input.siblings(".close-search").css("display", 'none');
        const setResultDisplay = () => searchResultBlock.css('display', 'none');
        setTimeout(setResultDisplay, 500);
    })
});


// =============how and hide menu==============


$(document).ready(function () {

    let but = $(".button-hide");
    let con = $(".left");
    let con2 = $(".right-header");

    but.click(function () {
        con.toggleClass("show-menu");
        con2.toggleClass("header-right__active");
    })
})

// ==============admin dropdown================

$(document).ready(function () {

    let but = $(".admin-dropdown .dropdown-button");
    let con = $(".admin-dropdown .dropdown-content");

    let open = function () {
        but.addClass("active");
        con.css("height", con[0].scrollHeight)
    };
    let close = function () {
        but.removeClass("active");
        con.css("height", 0)
    };

    but.click(function () {
        if (but.hasClass('active')) {
            close()
        } else {
            open()
        }
    })
})


// ==============modal close===============


$(document).ready(() => {
    $(".modal-finish__close").click(() => {
        $(".add-staff__modal-finish").css("display", 'none');
        window.location.reload(true);
    })
});


$(document).ready(() => {
    $(".modal-cancel").click(() => {
        $(".add-filial__modal-finish").css("display", 'none');
        $("body").removeClass("body-overflow");
    });
    $(".button .admin-but").click(() => {
        $(".add-filial__modal-finish").css("display", 'block');
        $("body").addClass("body-overflow");
    })
});

// ==========select content=============

const butSelect = $('.select-content__all');

const showSelect = (index) => {
    butSelect.each((i, obj) => {
        if (i === index) {
            $(obj).find(".select-content__info").addClass("active");
            $(obj).find(".select-content").css("height", $(obj).find(".select-content")[0].scrollHeight)
        } else {
            $(obj).find(".select-content__info").removeClass("active");
            $(obj).find(".select-content").css("height", 0)
        }
    })
};

const hideSelect = () => {
    butSelect.each((i, obj) => {
        $(obj).find(".select-content__info").removeClass("active");
        $(obj).find(".select-content").css("height", 0)
    })
};

butSelect.each((i, obj) => {
    $(obj).find(".select-content__info").click(() => {
        if ($(obj).find(".select-content__info").hasClass("active")) {
            hideSelect()
        } else {
            showSelect(i)
        }
    })
});


const selectContent = () => {

    // ==============checkbox add category==============

    $(document).ready(() => {
        let addCategory = $(".filial-and-department");

        addCategory.each((i, obj) => {
            $(obj).find(".radio").siblings(".add-radio").click(() => {
                $(obj).find(".add-radio").css("display", 'none');
                $(obj).find(".input-category").css("display", 'flex')
            });

            $(obj).find(".radio").find(".button-add-input").click((e) => {
                const $this = $(e.currentTarget);
                $(obj).find(".add-radio").css("display", 'block');
                $(obj).find(".input-category").css("display", 'none');
                $(obj).find(".radio").find("input[type=radio]").prop("checked", false);
                $this.siblings("input").val("");
            });

            $(obj).find(".radio").find("input[type=radio]").click(() => {
                $(obj).find(".add-radio").css("display", 'block');
                $(obj).find(".input-category").css("display", 'none')
            })
        })
    })

    // ===============hide and show checkbox departments==============

    $(document).ready(() => {

        let but = $(".filial-and-department");

        let show = (index) => {
            but.each((i, obj) => {
                if (i === index) {
                    $(obj).find('.select-content__all').css("display", 'flex')
                }
            })
        };

        let hide = (index) => {
            but.each((i, obj) => {
                if (i === index) {
                    $(obj).find('.select-content__all').css("display", 'none');
                    $(obj).find(".select-content__all .select-content .radio input").prop('checked', false);
                    $(obj).find(".select-content__all .select-content").css("height", 0);
                    $(obj).find(".select-content__info").removeClass("active");
                    $(obj).find('.input-category').css("display", 'none');
                    $(obj).find('.add-radio').css("display", 'flex');
                    $(obj).find(".select-content__all .select-content__info span").text((text) => {
                        text = "Выберите" + " " + $(obj).find(".checkbox-info .name").text().toLowerCase();
                        return text
                    })
                }
            })
        };

        but.each((i, obj) => {
            $(obj).find(".checkbox-block input").on("change", () => {
                if ($(obj).find(".checkbox-block input").is(":checked")) {
                    show(i)
                } else {
                    hide(i);
                }
            })
        });

        // ===============hide and show checkbox time==============

        let but2 = $(".set-time");

        let showTime = (index) => {
            but2.each((i, obj) => {
                if (i === index) {
                    $(obj).find(".select-content__time-all").addClass("show-time");
                    $(obj).find(".filter-block").css("display", 'none');
                }
            })
        };

        let hideTime = (index) => {
            but2.each((i, obj) => {
                if (i === index) {
                    $(obj).find(".select-content__time-all").removeClass("show-time");
                    $(obj).find(".filter-block").css("display", 'block');
                    $(obj).find(".select-content__all .select-content .radio input").prop('checked', false);
                    $(obj).find(".select-content__all .select-content").css("height", 0);
                    $(obj).find(".select-content__info").removeClass("active");
                }
            })
        };

        but2.each((i, obj) => {
            $(obj).find(".checkbox input").on('change', () => {
                if ($(obj).find(".checkbox input").is(":checked")) {
                    showTime(i)
                } else {
                    hideTime(i)
                }
            })
        });

        // =============copy text checkbox=============

        $('.select-content .radio input[type=radio]').change(function () {
            let selectedItem = $(this).siblings('label').text();
            let selectForm = $(this).closest(".select-content__all").find(".select-content__info span");
            $(this).closest(".select-content").css("height", 0);
            $(this).closest(".select-content").siblings(".select-content__info").removeClass("active");
            selectForm.text(selectedItem);
            let itemId = $(this).parent().attr('id');
            selectForm.attr('org_id', itemId);
        })

    })
};

selectContent();

// ===========disabled header link==============

$(document).ready(function () {
    $(".menu .disabled").click(function (e) {
        e.preventDefault()
    });

    // ================close block=============

    var menuBtn = $('.checkbox-all .checkbox'),
        menuBtn3 = $('.select-content__all'),
        menuBtn2 = $('.select-content__all .select-content__info'),
        menu = $('.select-content__all .select-content'),
        mapBlock = $('.modal-location__map'),
        mapBut = $('.modal-location'),
        body = $('body');

    $(document).click(function (e) {
        if (!menuBtn.is(e.target) && !menuBtn3.is(e.target) && menuBtn3.has(e.target).length === 0
            && !mapBut.is(e.target) && !mapBlock.is(e.target) && mapBlock.has(e.target).length === 0
        ) {
            menuBtn2.removeClass('active')
            menu.css('height', 0);
            mapBlock.parent('.modal-location__content').css('visibility', 'hidden');
            body.removeClass('body-overflow');
        }
    });

})

// ===============preloader functions===============

const preloaderEl = document.getElementById('preloader');

function preloadStart() {
    preloaderEl.classList.add('visible');
}

function preloaderEnd() {
    preloaderEl.classList.remove('visible');
}


