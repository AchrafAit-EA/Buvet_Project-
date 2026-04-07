document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector(".nav-toggle");
  const menu = document.querySelector(".nav-links");
  const overlay = document.querySelector(".nav-overlay");
  const closeBtn = document.querySelector(".close-btn");
  const links = document.querySelectorAll(".nav-links a");

  if (!toggle || !menu || !overlay) return;

  const openMenu = () => {
    menu.classList.add("open");
    overlay.classList.add("show");
    toggle.setAttribute("aria-expanded", "true");
    toggle.innerHTML = '<i class="fa-solid fa-bars"></i>';
  };

  const closeMenu = () => {
    menu.classList.remove("open");
    overlay.classList.remove("show");
    overlay.style.pointerEvents = "none";
    toggle.setAttribute("aria-expanded", "false");
    toggle.innerHTML = '<i class="fa-solid fa-bars"></i>';
  };

  toggle.addEventListener("click", () => {
    menu.classList.contains("open") ? closeMenu() : openMenu();
  });

  overlay.addEventListener("click", closeMenu);
  if (closeBtn) closeBtn.addEventListener("click", closeMenu);

  links.forEach((a) => {
    a.addEventListener("click", (e) => {
      const href = a.getAttribute("href");
      if (!href || !href.startsWith("#")) return;

      const target = document.querySelector(href);
      if (!target) return;

      e.preventDefault();
      closeMenu();

      setTimeout(() => {
        target.scrollIntoView({ behavior: "smooth" });
      }, 350);
    });
  });

  window.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeMenu();
  });
});
