const allModelBtns = document.querySelectorAll(".modal-btn");

// const modalWraper = document.querySelector('.modal-wrapper');

const allModalClose = document.querySelectorAll(".modal-close-btn");

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
        console.log("I'm clicked");
        let wrapperName = btn.getAttribute("target")
        let wrapper = document.querySelector(`.${wrapperName}`)
        wrapper.classList.remove("d-none");
        wrapper.classList.add("d-flex");

    })
});