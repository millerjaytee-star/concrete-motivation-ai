const year = document.querySelector("#year");
if (year) {
  year.textContent = new Date().getFullYear().toString();
}

const bookingForm = document.querySelector(".booking-form");
if (bookingForm) {
  bookingForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const status = bookingForm.querySelector(".form-status");
    if (status) {
      status.textContent = "Booking details are ready to copy once a form service is connected.";
    }
  });
}
