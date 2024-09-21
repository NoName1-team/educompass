let follower = document.querySelector(".header-sidebar_follower")
let sidebar_ul = document.querySelector(".siderbar-links")
let sidebar_items = document.querySelectorAll(".sidebar-link")
let sidebar_item_active = document.querySelector(".sidebar-link.active")
let form_wrapper = document.querySelector(".searching-form")
let back = document.querySelector(".back")
const underline = document.querySelector('.company-detail-follower');

sidebar_items.forEach(element => {
    element.addEventListener("mouseenter", () => {
        follower.style.top = `${element.getBoundingClientRect().top - 4}px`
        follower.style.height = `${element.getBoundingClientRect().height + 6}px`
        follower.style.width = `${element.getBoundingClientRect().width + 16}px`
    })
});

sidebar_ul.addEventListener("mouseleave", () => {
    setTimeout(() => {
        follower.style.top = `${sidebar_item_active.getBoundingClientRect().top - 4}px`
        follower.style.height = `${sidebar_item_active.getBoundingClientRect().height + 6}px`
    }, 500);
})

window.addEventListener("load", () => {
    follower.style.top = `${sidebar_item_active.getBoundingClientRect().top - 4}px`
    follower.style.height = `${sidebar_item_active.getBoundingClientRect().height + 6}px`
    follower.style.width = `${sidebar_item_active.getBoundingClientRect().width + 16}px`
    setTimeout(() => {
        follower.classList.add("opened")
    }, 500);
})

if (form_wrapper) {
    input = form_wrapper.firstElementChild.firstElementChild
    results = form_wrapper.lastElementChild
    input.addEventListener("click", () => {
        form_wrapper.classList.add("opened")
        back.classList.add("displayed")
        results.classList.remove("noned")
        results.style.width = `${input.getBoundingClientRect().width + 2}px`
        window.scrollTo({
            top: input.getBoundingClientRect().top - 100,
        })
        setTimeout(() => {
            results.classList.remove("cleared")
            back.classList.add("color")
        }, 200);
    })

    back.addEventListener("click", () => {
        back.classList.remove("color")
        results.classList.add("cleared")
        setTimeout(() => {
            results.classList.add("noned")
            form_wrapper.classList.remove("opened")
            back.classList.remove("displayed")
        }, 200);
    })
}
let network = document.querySelector(".notification.success")
window.addEventListener("online", () => {
    network.classList.add("opened")
    setTimeout(() => {
        network.classList.remove("opened")
    }, 3000);
})

window.addEventListener("offline", () => {
    network_down = network.previousElementSibling
    network.classList.remove("opened")
    network_down.classList.add("opened")
    setTimeout(() => {
        network_down.classList.remove("opened")
    }, 3000);
})


document.addEventListener('DOMContentLoaded', function () {
    const cookieConsent = document.querySelector(".notification.warning")
    const acceptButton = document.getElementById('accept-cookies');

    if (!getCookie('cookie_consent')) {
        cookieConsent.classList.add('opened');
    }

    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }

    function setCookie(name, value, days) {
        const d = new Date();
        d.setTime(d.getTime() + (days * 24 * 60 * 60 * 1000));
        const expires = `expires=${d.toUTCString()}`;
        document.cookie = `${name}=${value};${expires};path=/`;
    }

    acceptButton.addEventListener('click', function () {
        setCookie('cookie_consent', 'accepted', 365);
        cookieConsent.classList.remove('opened');
    });
});
window.addEventListener("load", () => {
    localStorage.setItem("current_url", `${window.location}`)
})

navbar_link = document.querySelector(".navbar-link.active")
window.addEventListener("scroll", () => {
    if (window.scrollY > 300) {
        navbar_link.classList.add("scroll_up")
        navbar_link.setAttribute("href", "#")
    } else {
        navbar_link.classList.remove("scroll_up")
        navbar_link.setAttribute("href", `${localStorage.getItem("current_url")}`)
    }
})


let jquery_multiple = document.querySelector(".jquery-multiple")
let filter_wrapper = document.querySelector(".filter-wrapper")
if (filter_wrapper) {
    filter_wrapper.addEventListener('click', function () {
        const selectedOptions = Array.from(jquery_multiple.selectedOptions);
        const values = selectedOptions.map(option => option.value);
    });
}

let gender_wrapper_input = document.querySelector(".filter-gender-wrapper input")
gender_spans = document.querySelectorAll(".filter-gender-wrapper span")
if (gender_wrapper_input) {
    gender_spans.forEach((span) => {
        span.addEventListener("click", () => {
            input = document.querySelector(`.filter-gender-wrapper input#${span.classList[0]}`)
            span.classList.toggle("active")
            input.checked = span.classList.contains("active") ? true : false;
        })
    })
}

let days_wrapper_input = document.querySelector(".filter-days-wrapper input")
days_spans = document.querySelectorAll(".filter-days-wrapper span")
if (days_wrapper_input) {
    days_spans.forEach((span) => {
        span.addEventListener("click", () => {
            input = document.querySelector(`.filter-days-wrapper input#${span.classList[0]}`)
            span.classList.toggle("active")
            input.checked = span.classList.contains("active") ? true : false;
        })
    })
}

let filter_opener = document.querySelector(".filter-opener")
filter_wrapper = document.querySelector(".filter-wrapper")
if (filter_opener) {
    filter_opener.addEventListener("click", () => {
        filter_wrapper.classList.toggle("active")
    })
}

let form_closers = document.querySelectorAll(".form-closer")
form_closers.forEach(closer => {
    closer.addEventListener("click", () => {
        filter_wrapper.classList.remove("active")
    })
});

let submit_cancel = document.querySelector(".forms-submit.cancel"),
    send_request = document.querySelector(".course-detail-send-request")
if (send_request) {
    send_request.addEventListener("click", () => {
        document.querySelector(".main-forms").classList.add("active")
        document.querySelector("html").classList.add("closed")
    })
}
if (submit_cancel) {
    submit_cancel.addEventListener("click", () => {
        document.querySelector(".main-forms").classList.remove("active")
        document.querySelector("html").classList.remove("closed")
    })
}



let raiting_wrapper_input = document.querySelector(".filter-raiting-wrapper input")
raiting_spans = document.querySelectorAll(".filter-raiting-wrapper span")
if (raiting_wrapper_input) {
    raiting_spans.forEach((span) => {
        span.addEventListener("click", () => {
            const loopValue = span.getAttribute('data-loop')
            console.log(loopValue);
            raiting_spans.forEach(element => {
                element.className = ""
            });
            if (loopValue == 1) {
                for (let i = 0; i < loopValue; i++) {
                    raiting_spans[i].classList.add("active")
                    raiting_spans[i].classList.add("worst")
                }
            } else if (loopValue == 2) {
                for (let i = 0; i < loopValue; i++) {
                    raiting_spans[i].classList.add("active")
                    raiting_spans[i].classList.add("bad")
                }
            } else if (loopValue == 3) {
                for (let i = 0; i < loopValue; i++) {
                    raiting_spans[i].classList.add("active")
                    raiting_spans[i].classList.add("normal")
                }
            } else if (loopValue == 4) {
                for (let i = 0; i < loopValue; i++) {
                    raiting_spans[i].classList.add("active")
                    raiting_spans[i].classList.add("good")
                }
            } else if (loopValue == 5) {
                for (let i = 0; i < loopValue; i++) {
                    raiting_spans[i].classList.add("active")
                    raiting_spans[i].classList.add("perfect")
                }
            }
        })
    })
}

document.querySelectorAll('.company-detail-dropdown').forEach(item => {
    item.addEventListener('click', function () {
        document.querySelectorAll('.company-detail-dropdown').forEach(i => i.classList.remove(
            'active'));
        this.classList.add('active');

        underline.style.width = this.offsetWidth + 'px';
        underline.style.left = this.offsetLeft + 'px';
    });
});

window.addEventListener('load', function () {
    const activeItem = document.querySelector('.company-detail-dropdown.active');
    if (underline) {
        underline.style.width = activeItem.offsetWidth + 'px';
        underline.style.left = activeItem.offsetLeft + 'px';
    }
});

let company_dropdowns = document.querySelectorAll(".company-detail-dropdown")
let detail_blocks = document.querySelectorAll(".company-detail-block")
company_dropdowns.forEach((dropdown) => {
    dropdown.addEventListener("click", () => {
        company_dropdowns.forEach((item) => {
            item.classList.remove("active")
        })
        detail_blocks.forEach((block) => {
            block.classList.remove("active")
            block.classList.remove("activated")
        })
        dropdown.classList.add("active")
        data_attr = dropdown.getAttribute("data-call-block")

        detail_block = document.querySelector(`.company-detail-block.${data_attr}`)
        detail_block.classList.add("active")
    })
})
kurslar = document.querySelector('.company-detail-dropdown.kurslar')
let same_blocks = document.querySelectorAll(".company-detail-same-block"),
    courses_list = document.querySelectorAll(".company-detail-block.courses.course-list .course-item")
courses_course_list = document.querySelector(".company-detail-block.courses.course-list")
same_blocks.forEach((block) => {
    block.addEventListener("click", () => {
        company_dropdowns.forEach((item) => {
            item.classList.remove("active")
        })
        detail_blocks.forEach((block) => {
            block.classList.remove("active")
        })
        kurslar.classList.add("active")
        const underline = document.querySelector('.company-detail-follower');
        underline.style.width = kurslar.offsetWidth + 'px';
        underline.style.left = kurslar.offsetLeft + 'px';

        courses_course_list.classList.add("activated")
        if (block.classList.contains("branch")) {
            data_branch = block.getAttribute("data-open-branch")
            courses_list.forEach(item => {
                if (item.classList.contains(data_branch)) {
                    item.classList.add("choosen")
                    item.classList.remove("actived-by-other")
                } else {
                    item.classList.remove("choosen")
                    item.classList.add("actived-by-other")
                }
            });
        } else {
            data_category = block.getAttribute("data-open-category")
            courses_list.forEach(item => {
                if (item.classList.contains(data_category)) {
                    item.classList.add("choosen")
                    item.classList.remove("actived-by-other")
                } else {
                    item.classList.remove("choosen")
                    item.classList.add("actived-by-other")
                }
            });
        }
    })
})

if (kurslar) {
    kurslar.addEventListener("click", () => {
        courses_list.forEach((course_item) => {
            course_item.classList.remove("choosen")
            course_item.classList.remove("actived-by-other")
        })
    })
}


let comment_form_inputs = document.querySelector(".company-detail-comment-form_rating input")
comment_form_spans = document.querySelectorAll(".company-detail-comment-form_rating span")
if (comment_form_inputs) {
    comment_form_spans.forEach((span) => {
        span.addEventListener("click", () => {
            const loopValue = span.getAttribute('data-loop')
            comment_form_spans.forEach(element => {
                element.className = ""
            });
            if (loopValue == 1) {
                for (let i = 0; i < loopValue; i++) {
                    comment_form_spans[i].classList.add("active")
                    comment_form_spans[i].classList.add("worst")
                }
            } else if (loopValue == 2) {
                for (let i = 0; i < loopValue; i++) {
                    comment_form_spans[i].classList.add("active")
                    comment_form_spans[i].classList.add("bad")
                }
            } else if (loopValue == 3) {
                for (let i = 0; i < loopValue; i++) {
                    comment_form_spans[i].classList.add("active")
                    comment_form_spans[i].classList.add("normal")
                }
            } else if (loopValue == 4) {
                for (let i = 0; i < loopValue; i++) {
                    comment_form_spans[i].classList.add("active")
                    comment_form_spans[i].classList.add("good")
                }
            } else if (loopValue == 5) {
                for (let i = 0; i < loopValue; i++) {
                    comment_form_spans[i].classList.add("active")
                    comment_form_spans[i].classList.add("perfect")
                }
            }
        })
    })
}