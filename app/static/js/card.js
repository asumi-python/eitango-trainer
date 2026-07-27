// Card flip: reveal meaning and show answer buttons
const revealBtn = document.getElementById("reveal-btn");
const cardBack = document.getElementById("card-back");
const answerButtons = document.getElementById("answer-buttons");

if (revealBtn) {
  revealBtn.addEventListener("click", function () {
    cardBack.classList.remove("hidden");
    answerButtons.classList.remove("hidden");
    revealBtn.classList.add("hidden");
  });
}

// Settings page: show/hide streak input based on mastery mode
document.querySelectorAll('input[name="mastery_mode"]').forEach(function (radio) {
  radio.addEventListener("change", function () {
    const streakSection = document.getElementById("streak-section");
    if (streakSection) {
      streakSection.style.display = this.value === "auto" ? "flex" : "none";
    }
  });
});
