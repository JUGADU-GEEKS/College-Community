import imagesLoaded from "https://esm.sh/imagesloaded";

console.clear();

// -------------------------------------------------
// ------------------ Utilities --------------------
// -------------------------------------------------

// Math utilities
const wrap = (n, max) => (n + max) % max;
const lerp = (a, b, t) => a + (b - a) * t;

// DOM utilities
const isHTMLElement = (el) => el instanceof HTMLElement;

const genId = (() => {
	let count = 0;
	return () => {
		return (count++).toString();
	};
})();

class Raf {
	constructor() {
		this.rafId = 0;
		this.raf = this.raf.bind(this);
		this.callbacks = [];

		this.start();
	}

	start() {
		this.raf();
	}

	stop() {
		cancelAnimationFrame(this.rafId);
	}

	raf() {
		this.callbacks.forEach(({ callback, id }) => callback({ id }));
		this.rafId = requestAnimationFrame(this.raf);
	}

	add(callback, id) {
		this.callbacks.push({ callback, id: id || genId() });
	}

	remove(id) {
		this.callbacks = this.callbacks.filter((callback) => callback.id !== id);
	}
}

class Vec2 {
	constructor(x = 0, y = 0) {
		this.x = x;
		this.y = y;
	}

	set(x, y) {
		this.x = x;
		this.y = y;
	}

	lerp(v, t) {
		this.x = lerp(this.x, v.x, t);
		this.y = lerp(this.y, v.y, t);
	}
}

const vec2 = (x = 0, y = 0) => new Vec2(x, y);

export function tilt(node, options) {
	let { trigger, target } = resolveOptions(node, options);

	let lerpAmount = 0.06;

	const rotDeg = { current: vec2(), target: vec2() };
	const bgPos = { current: vec2(), target: vec2() };

	const update = (newOptions) => {
		destroy();
		({ trigger, target } = resolveOptions(node, newOptions));
		init();
	};

	let rafId;

	function ticker({ id }) {
		rafId = id;

		rotDeg.current.lerp(rotDeg.target, lerpAmount);
		bgPos.current.lerp(bgPos.target, lerpAmount);

		for (const el of target) {
			el.style.setProperty("--rotX", rotDeg.current.y.toFixed(2) + "deg");
			el.style.setProperty("--rotY", rotDeg.current.x.toFixed(2) + "deg");

			el.style.setProperty("--bgPosX", bgPos.current.x.toFixed(2) + "%");
			el.style.setProperty("--bgPosY", bgPos.current.y.toFixed(2) + "%");
		}
	}

	const onMouseMove = ({ offsetX, offsetY }) => {
		lerpAmount = 0.1;

		for (const el of target) {
			const ox = (offsetX - el.clientWidth * 0.5) / (Math.PI * 3);
			const oy = -(offsetY - el.clientHeight * 0.5) / (Math.PI * 4);

			rotDeg.target.set(ox, oy);
			bgPos.target.set(-ox * 0.3, oy * 0.3);
		}
	};

	const onMouseLeave = () => {
		lerpAmount = 0.06;

		rotDeg.target.set(0, 0);
		bgPos.target.set(0, 0);
	};

	const addListeners = () => {
		trigger.addEventListener("mousemove", onMouseMove);
		trigger.addEventListener("mouseleave", onMouseLeave);
	};

	const removeListeners = () => {
		trigger.removeEventListener("mousemove", onMouseMove);
		trigger.removeEventListener("mouseleave", onMouseLeave);
	};

	const init = () => {
		addListeners();
		raf.add(ticker);
	};

	const destroy = () => {
		removeListeners();
		raf.remove(rafId);
	};

	init();

	return { destroy, update };
}

function resolveOptions(node, options) {
	return {
		trigger: options?.trigger ?? node,
		target: options?.target
			? Array.isArray(options.target)
				? options.target
				: [options.target]
			: [node]
	};
}

// -----------------------------------------------------

// Global Raf Instance
const raf = new Raf();

// Auto-slide functionality
let autoSlideTimer = null;
let autoSlideInterval = 3000; // 3 seconds
let isAutoSlidePaused = false;

function startAutoSlide() {
	if (autoSlideTimer) {
		clearInterval(autoSlideTimer);
	}
	
	autoSlideTimer = setInterval(() => {
		if (!isAutoSlidePaused) {
			change(1)();
		}
	}, autoSlideInterval);
}

function pauseAutoSlide() {
	isAutoSlidePaused = true;
}

function resumeAutoSlide() {
	isAutoSlidePaused = false;
}

function stopAutoSlide() {
	if (autoSlideTimer) {
		clearInterval(autoSlideTimer);
		autoSlideTimer = null;
	}
}

function init() {
	const loader = document.querySelector(".loader");

	const slides = [...document.querySelectorAll(".slide")];
	const slidesInfo = [...document.querySelectorAll(".slide-info")];

	const buttons = {
		prev: document.querySelector(".slider--btn__prev"),
		next: document.querySelector(".slider--btn__next")
	};

	loader.style.opacity = 0;
	loader.style.pointerEvents = "none";

	slides.forEach((slide, i) => {
		const slideInner = slide.querySelector(".slide__inner");
		const slideInfoInner = slidesInfo[i].querySelector(".slide-info__inner");

		tilt(slide, { target: [slideInner, slideInfoInner] });
	});

	// Add click event listeners with auto-slide pause/resume
	buttons.prev.addEventListener("click", () => {
		change(-1)();
		pauseAutoSlide();
		setTimeout(resumeAutoSlide, 3000); // Resume after 3 seconds
	});
	
	buttons.next.addEventListener("click", () => {
		change(1)();
		pauseAutoSlide();
		setTimeout(resumeAutoSlide, 3000); // Resume after 3 seconds
	});

	// Add hover pause functionality
	const slider = document.querySelector(".slider");
	slider.addEventListener("mouseenter", pauseAutoSlide);
	slider.addEventListener("mouseleave", resumeAutoSlide);

	// Start auto-slide
	startAutoSlide();
}

function setup() {
	initializeSlides();
	init();
}

// Helper to initialize slide states
function initializeSlides() {
	// Only select direct children of .slides for .slide and .slide__bg, to preserve order
	const slidesWrapper = document.querySelector('.slides');
	const slides = [...slidesWrapper.querySelectorAll(':scope > .slide')];
	const slideBgs = [...slidesWrapper.querySelectorAll(':scope > .slide__bg')];
	const slidesInfo = [...document.querySelectorAll('.slide-info')];
	if (slides.length < 1) return;
	// Remove all data attributes
	slides.forEach(slide => {
		slide.removeAttribute("data-current");
		slide.removeAttribute("data-previous");
		slide.removeAttribute("data-next");
		slide.style.zIndex = "";
	});
	slidesInfo.forEach(slide => {
		slide.removeAttribute("data-current");
		slide.removeAttribute("data-previous");
		slide.removeAttribute("data-next");
	});
	slideBgs.forEach(slide => {
		slide.removeAttribute("data-current");
		slide.removeAttribute("data-previous");
		slide.removeAttribute("data-next");
	});
	// Set initial states
	slides[0].setAttribute("data-current", "");
	slides[0].style.zIndex = "20";
	slidesInfo[0].setAttribute("data-current", "");
	slideBgs[0].setAttribute("data-current", "");
	if (slides.length > 1) {
		slides[1].setAttribute("data-next", "");
		slides[1].style.zIndex = "10";
		slidesInfo[1].setAttribute("data-next", "");
		slideBgs[1].setAttribute("data-next", "");
		slides[slides.length - 1].setAttribute("data-previous", "");
		slides[slides.length - 1].style.zIndex = "10";
		slidesInfo[slidesInfo.length - 1].setAttribute("data-previous", "");
		slideBgs[slideBgs.length - 1].setAttribute("data-previous", "");
	}
}

function change(direction) {
	return () => {
		// Only select direct children of .slides for .slide and .slide__bg, to preserve order
		const slidesWrapper = document.querySelector('.slides');
		const slides = [...slidesWrapper.querySelectorAll(':scope > .slide')];
		const slideBgs = [...slidesWrapper.querySelectorAll(':scope > .slide__bg')];
		const slidesInfo = [...document.querySelectorAll('.slide-info')];
		if (slides.length < 1) return;

		// Find current index
		let currentIdx = slides.findIndex(slide => slide.hasAttribute("data-current"));
		if (currentIdx === -1) currentIdx = 0;
		let prevIdx = (currentIdx - 1 + slides.length) % slides.length;
		let nextIdx = (currentIdx + 1) % slides.length;

		// Remove all data attributes and reset zIndex
		slides.forEach(slide => {
			slide.removeAttribute("data-current");
			slide.removeAttribute("data-previous");
			slide.removeAttribute("data-next");
			slide.style.zIndex = "";
		});
		slidesInfo.forEach(slide => {
			slide.removeAttribute("data-current");
			slide.removeAttribute("data-previous");
			slide.removeAttribute("data-next");
		});
		slideBgs.forEach(slide => {
			slide.removeAttribute("data-current");
			slide.removeAttribute("data-previous");
			slide.removeAttribute("data-next");
		});

		// Calculate new indices
		let newCurrentIdx = (currentIdx + direction + slides.length) % slides.length;
		let newPrevIdx = (newCurrentIdx - 1 + slides.length) % slides.length;
		let newNextIdx = (newCurrentIdx + 1) % slides.length;

		// Set new data attributes and zIndex
		slides[newCurrentIdx].setAttribute("data-current", "");
		slides[newCurrentIdx].style.zIndex = "20";
		slidesInfo[newCurrentIdx].setAttribute("data-current", "");
		slideBgs[newCurrentIdx].setAttribute("data-current", "");

		slides[newPrevIdx].setAttribute("data-previous", "");
		slides[newPrevIdx].style.zIndex = "10";
		slidesInfo[newPrevIdx].setAttribute("data-previous", "");
		slideBgs[newPrevIdx].setAttribute("data-previous", "");

		slides[newNextIdx].setAttribute("data-next", "");
		slides[newNextIdx].style.zIndex = "10";
		slidesInfo[newNextIdx].setAttribute("data-next", "");
		slideBgs[newNextIdx].setAttribute("data-next", "");
	};
}

// Start
setup();
