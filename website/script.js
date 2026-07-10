const year = document.querySelector("#year");
if (year) {
  year.textContent = new Date().getFullYear().toString();
}

const navToggle = document.querySelector(".nav-toggle");
const siteNav = document.querySelector("#site-nav");
if (navToggle && siteNav) {
  navToggle.addEventListener("click", () => {
    const isOpen = navToggle.getAttribute("aria-expanded") === "true";
    navToggle.setAttribute("aria-expanded", (!isOpen).toString());
    siteNav.classList.toggle("is-open", !isOpen);
    document.body.classList.toggle("nav-open", !isOpen);
  });

  siteNav.addEventListener("click", (event) => {
    if (event.target instanceof HTMLAnchorElement) {
      navToggle.setAttribute("aria-expanded", "false");
      siteNav.classList.remove("is-open");
      document.body.classList.remove("nav-open");
    }
  });
}

const bookingForm = document.querySelector(".booking-form");
if (bookingForm) {
  bookingForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const formData = new FormData(bookingForm);
    const name = formData.get("name") || "your name";
    const eventType = formData.get("event-type") || "speaking event";
    const organization = formData.get("organization") || "your organization";
    const status = bookingForm.querySelector(".form-status");
    if (status) {
      status.textContent = `Inquiry prepared for ${name}: ${eventType} with ${organization}. Review the details and send them through your preferred contact channel.`;
    }
  });
}

const stripeButtons = document.querySelectorAll(".stripe-button");
const stripeNote = document.querySelector(".stripe-note");
const stripeLinks = {
  starter: "",
  builder: "",
};

stripeButtons.forEach((button) => {
  button.addEventListener("click", (event) => {
    const plan = button.getAttribute("data-stripe-link") || "";
    const checkoutUrl = stripeLinks[plan];
    if (!checkoutUrl) {
      event.preventDefault();
      if (stripeNote) {
        stripeNote.textContent = "Stripe checkout is ready for live payment links. Add approved Stripe Payment Links before launch; no payment was collected.";
      }
      return;
    }
    button.setAttribute("href", checkoutUrl);
  });
});
