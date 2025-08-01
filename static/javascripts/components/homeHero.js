let currentSlide = 0;

const slides = document.querySelectorAll(".slide");
const infos = document.querySelectorAll(".slide-info");
const nextBtn = document.querySelector(".slider--btn__next");
const prevBtn = document.querySelector(".slider--btn__prev");
let intervalId;

function showSlide(index) {
  slides.forEach((slide, i) => {
    slide.removeAttribute("data-current");
    slide.removeAttribute("data-next");
    slide.removeAttribute("data-previous");

    if (i === index) slide.setAttribute("data-current", "");
    else if (i === (index + 1) % slides.length) slide.setAttribute("data-next", "");
    else if (i === (index - 1 + slides.length) % slides.length) slide.setAttribute("data-previous", "");
  });

  infos.forEach((info, i) => {
    info.removeAttribute("data-current");
    info.removeAttribute("data-next");
    info.removeAttribute("data-previous");

    if (i === index) info.setAttribute("data-current", "");
    else if (i === (index + 1) % infos.length) info.setAttribute("data-next", "");
    else if (i === (index - 1 + infos.length) % infos.length) info.setAttribute("data-previous", "");
  });
}

function nextSlide() {
  currentSlide = (currentSlide + 1) % slides.length;
  showSlide(currentSlide);
}

function prevSlide() {
  currentSlide = (currentSlide - 1 + slides.length) % slides.length;
  showSlide(currentSlide);
}

function startAutoSlide() {
  intervalId = setInterval(nextSlide, 2000); // 2 seconds
}

function stopAutoSlide() {
  clearInterval(intervalId);
}

// Initialize
document.addEventListener("DOMContentLoaded", () => {
  showSlide(currentSlide);
  startAutoSlide();

  nextBtn.addEventListener("click", () => {
    nextSlide();
    stopAutoSlide();
    startAutoSlide();
  });

  prevBtn.addEventListener("click", () => {
    prevSlide();
    stopAutoSlide();
    startAutoSlide();
  });
});
