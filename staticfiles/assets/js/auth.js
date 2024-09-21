let password_shower = document.querySelectorAll(".auth-password_shower")

password_shower.forEach(shower => {
    shower.addEventListener("click", () => {
        shower.firstElementChild.classList.toggle("fa-eye")
        shower.firstElementChild.classList.toggle("fa-eye-slash")
        input = shower.previousElementSibling
        input.classList.toggle("showed")
        if (input.className == "showed") {
            input.type = "text"
        } else {
            input.type = "password"
        }
    })
});


let timeLeft = 60;
var timerElement = document.querySelector(".auth-form-resend-link span");
var resendLink = timerElement.parentElement;

var originalHref = resendLink.getAttribute("href");

function startTimer() {
    var countdownTimer = setInterval(function () {
        var minutes = Math.floor(timeLeft / 60);
        var seconds = timeLeft % 60;

        seconds = seconds < 10 ? "0" + seconds : seconds;

        timerElement.innerHTML = "(" + minutes + ":" + seconds + ")";

        timeLeft--;

        if (timeLeft < 0) {
            clearInterval(countdownTimer);
            timerElement.innerHTML = "";

            resendLink.setAttribute("href", originalHref);
        }
    }, 1000);
}

resendLink.addEventListener('click', function (e) {
    if (timeLeft > 0) {
        e.preventDefault(); // Linkni faollashtirmaslik
    } else {
        timeLeft = 30; // Timer reset qilinadi
        startTimer(); // Timer qayta boshlanadi
        resendLink.setAttribute("href", ""); // Timer ishlayotgan paytda hrefni olib tashlash
    }
});

if (timeLeft > 0) {
    resendLink.setAttribute("href", "");
    startTimer();
}









let comming_password = document.querySelector(".auth-form-input-wrapper input");
let password_items = document.querySelectorAll(".auth-form-password-item");

comming_password.addEventListener("focus", () => {
    // Initial activation of the first item on focus
    password_items[0].classList.add("active");
});

comming_password.addEventListener("keyup", () => {
    let comming_txt_pass = comming_password.value;

    // Ensure the input does not exceed 5 characters
    if (comming_txt_pass.length > 5) {
        comming_txt_pass = comming_txt_pass.slice(0, 5);
        comming_password.value = comming_txt_pass; // Update the input value to reflect the trimmed string
    }

    password_items.forEach((item, index) => {
        if (index < comming_txt_pass.length) {
            item.innerHTML = comming_txt_pass[index];
            item.classList.add("active");
        } else {
            item.innerHTML = "";
            item.classList.remove("active");
        }
    });

    // Manage the active class for the next item if there's space
    if (comming_txt_pass.length < password_items.length) {
        password_items[comming_txt_pass.length].classList.add("active");
    }
});

comming_password.addEventListener("blur", () => {
    // Remove active class on blur if no input
    password_items.forEach(item => {
        if (item.innerHTML === "") {
            item.classList.remove("active");
        }
    });
});