const allModelBtns = document.querySelectorAll(".modal-btn");

const allModalClose = document.querySelectorAll(".modal-close-btn");

const textNums = document.querySelectorAll(".time-text");

textNums.forEach(ptag => {
    if (ptag.innerText === "0") {
        ptag.parentElement.parentElement.style.backgroundColor = "rgba(166, 25, 46, 0.80)";
        ptag.parentElement.style.backgroundColor = "#A6192E"
    }
})

allModalClose.forEach(btn => {
    btn.addEventListener("click", function(){
        let wrapperName = btn.getAttribute("target")
        let wrapper = document.querySelector(`.${wrapperName}`)
        wrapper.classList.add("d-none");
        wrapper.classList.remove("d-flex");
    })
})

allModelBtns.forEach(btn => {
    btn.addEventListener("click", function(){
        let wrapperName = btn.getAttribute("target")
        let wrapper = document.querySelector(`.${wrapperName}`)
        wrapper.classList.remove("d-none");
        wrapper.classList.add("d-flex");
    })
});