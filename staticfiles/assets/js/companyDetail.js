document.querySelectorAll('.company-detail-dropdown').forEach(item => {
    item.addEventListener('click', function () {
        document.querySelectorAll('.company-detail-dropdown').forEach(i => i.classList.remove(
            'active'));
        this.classList.add('active');
        document.querySelector("html").classList.remove("closed")
        if (underline) {
            underline.style.width = this.offsetWidth + 'px';
            underline.style.left = this.offsetLeft + 'px';
        }
    });
});

window.addEventListener('load', function () {
    const activeItem = document.querySelector('.company-detail-dropdown.active');
    if (underline) {
        underline.style.width = activeItem.offsetWidth + 'px';
        underline.style.left = activeItem.offsetLeft + 'px';
    }

});

tippy('.most-searched', {
    content: "#1 Eng ko'p izlangan",
    placement: 'top',
    duration: 100,
});
tippy('.most-liked', {
    content: "#1 Eng ko'p ma'qul kelgan",
    placement: 'top',
    duration: 100,
});

window.addEventListener('load', function () {
    const masonryItems = document.querySelectorAll('.masonry-item');
    masonryItems.forEach(item => {
        const rowSpan = Math.ceil(item.getBoundingClientRect().height / 10);
        item.style.gridRowEnd = `span ${rowSpan}`;
    });
});

window.addEventListener('resize', function () {
    const masonryItems = document.querySelectorAll('.masonry-item');
    masonryItems.forEach(item => {
        const rowSpan = Math.ceil(item.getBoundingClientRect().height / 10);
        item.style.gridRowEnd = `span ${rowSpan}`;
    });
});

let detail_form_opener = document.querySelector(".company-detail-form-opener")
let company_detail_blocks = document.querySelectorAll(".company-detail-block")
detail_blocks_comments = document.querySelector(".company-detail-block.comments")
let comment_form = document.querySelector(".company-detail-comment-form")
detail_dropdowns = document.querySelectorAll(".company-detail-dropdown")
detail_dropdown_comment = document.querySelector(".company-detail-dropdown.comments")
if (detail_form_opener) {

    detail_form_opener.addEventListener("click", () => {
        company_detail_blocks.forEach((block) => {
            block.classList.remove("active")
        })
        detail_dropdowns.forEach((block) => {
            block.classList.remove("active")
        })
        setTimeout(() => {
            comment_form.classList.add("active")
        }, 500)
        detail_dropdown_comment.classList.add("active")
        detail_blocks_comments.classList.add("active")
        underline.style.width = detail_dropdown_comment.offsetWidth + 'px';
        underline.style.left = detail_dropdown_comment.offsetLeft + 'px';
        document.querySelector("html").classList.add("closed")
    })
}

if (comment_form) {

    window.addEventListener("scroll", () => {
        if (window.scrollY <= 150) {
            comment_form.classList.remove("active")
        }
    })
}

const triggerLine = document.querySelector('.company-detail-scroller');
const motherBlock = document.querySelector('.company-detail-comment-form');
const textarea = document.querySelector('.company-detail-comment-details textarea');
const rating_spans = document.querySelectorAll('.company-detail-comment-form_rating span');

let isDragging = false;
let startY;

if (triggerLine) {
    triggerLine.addEventListener('mousedown', startDrag);
    triggerLine.addEventListener('touchstart', startDrag);

    rating_spans.forEach(span => {
        span.addEventListener("click", (e) => {
            motherBlock.style.bottom = '0px';
        });
    });

    function startDrag(e) {
        if (e.target === textarea || Array.from(rating_spans).includes(e.target)) {
            return;
        } else {
            isDragging = true;
            startY = (e.clientY || e.touches[0].clientY);
            motherBlock.style.cursor = 'grabbing';
            document.body.style.overflow = 'hidden';
            document.addEventListener('mousemove', onMouseMove);
            document.addEventListener('touchmove', onMouseMove);
            document.addEventListener('mouseup', onMouseUp);
            document.addEventListener('touchend', onMouseUp);
        }
    }

    function onMouseMove(e) {
        if (isDragging) {
            e.preventDefault();
            let clientY = e.clientY || e.touches[0].clientY;
            let y = startY - clientY;
            if (y < 0) {
                motherBlock.style.bottom = `-${-y}px`;
                if (parseInt(motherBlock.style.bottom, 10) < -50) {
                    motherBlock.classList.remove("active");
                    document.querySelector("html").classList.remove("closed");
                    motherBlock.style.bottom = '';
                    isDragging = false;
                    onMouseUp();
                }
            }
        }
    }

    function onMouseUp() {
        if (isDragging) {
            isDragging = false;
            motherBlock.style.cursor = 'grab';
            document.removeEventListener('mousemove', onMouseMove);
            document.removeEventListener('touchmove', onMouseMove);
            document.removeEventListener('mouseup', onMouseUp);
            document.removeEventListener('touchend', onMouseUp);
            document.body.style.overflow = 'auto';
            document.querySelector("html").classList.remove("closed");
            motherBlock.classList.remove("active");
        }
    }
}