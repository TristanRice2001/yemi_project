(function () {
  const emailInput = document.getElementById("user-email");
  const emailForm = document.getElementById("email-input-form");
  const emailButton = document.getElementById("email-submit");

  const changeEmailSubmitDisabled = (value) => {
    value
      ? emailButton.removeAttribute("disabled")
      : emailButton.setAttribute("disabled", true);
  };

  const setEmailSubmitButtonLoading = () => {
    emailButton.querySelector("span").classList.add("hidden");
    emailButton.querySelector("svg").classList.remove("hidden");
  };

  const setEmailSubmitCompleted = () => {
    emailButton
      .querySelector(".header__email-loading-svg")
      .classList.add("hidden");
    emailButton
      .querySelector(".header__email-completed-svg")
      .classList.remove("hidden");
    emailButton
      .querySelector(".header__email-completed-svg")
      .classList.add("header__email-completed-svg--animated");
  };

  const onEmailInputChange = (e) => {
    const emailValid = e.target.value !== "" && emailInput.checkValidity();
    changeEmailSubmitDisabled(emailValid);
  };

  const onEmailFormSubmit = (e) => {
    e.preventDefault();
    const emailValue = emailInput.value;
    setEmailSubmitButtonLoading();
    setTimeout(() => {
      setEmailSubmitCompleted();
    }, 2000);
  };

  emailForm.addEventListener("submit", onEmailFormSubmit);
  emailInput.addEventListener("input", onEmailInputChange);
})();
