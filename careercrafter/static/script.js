var volumeSliders = document.querySelectorAll(".volume-slider");
var para = document.querySelectorAll(".para");
var currentGroup = 1;
var loader = document.getElementById('preloader');
window.addEventListener("load", function(){
  loader.style.display = "none";
})

function updateSliderStyleAndText(slider, index, currentGroup) {
  var colors = ["darkgreen", "green", "lightgreen", "blue", "coral", "orangered", "red"];
  var texts = ["Strongly Agree", "Agree", "Slightly Agree", "Neutral", "Slightly Disagree", "Disagree", "Strongly Disagree"];
  var value = slider.value;
  var colorIndex = Math.min(Math.floor(value / 14), 6);

  slider.style.background = colors[colorIndex];
  para[index].innerHTML = texts[colorIndex];
  para[index].style.color = colors[colorIndex];

  
  // Check if all sliders in the current group have been interacted with
  var currentGroupSliders = Array.from(volumeSliders).slice((currentGroup - 1) * 10, currentGroup * 10);
  var allInteracted = currentGroupSliders.every(slider => parseInt(slider.value) !== 50);

  // Enable the next button if all sliders in the current group have been interacted with
  nextButton.disabled = !allInteracted;

  // Check if all sliders have been interacted with
  var allSlidersInteracted = Array.from(volumeSliders).every(slider => parseInt(slider.value) !== 50);

  // Enable the submit button if all sliders have been interacted with
  submitButton.disabled = !allSlidersInteracted;
}

// Loop through each slider and add event listener
volumeSliders.forEach(function(slider, index) {
  slider.oninput = function() {
    // Pass currentGroup as a parameter to updateSliderStyleAndText function
    updateSliderStyleAndText(this, index, currentGroup);
  };
});
// JavaScript to dynamically handle questions
document.addEventListener('DOMContentLoaded', function() {
  const questions = document.querySelectorAll('.q-box');
  const nextButton = document.getElementById('nextButton');
  const backButton = document.getElementById('backButton');
  const submitButton = document.getElementById('submitButton');
  
  // Function to show questions based on group
  function showQuestions(group) {
    questions.forEach((question, index) => {
      if (index >= (group - 1) * 10 && index < group * 10) {
        question.style.display = 'block';
      } else {
        question.style.display = 'none';
      }
    });

    if (group === 1) {
      backButton.disabled = true;
    } else {
        backButton.disabled = false;
    }

  // Display or hide next and submit buttons based on the group
  if (group < 6) { // Assuming there are 60 questions divided into 6 groups of 10
      nextButton.disabled = true;
      submitButton.style.display = 'none';
  } else {
      nextButton.style.display = 'none';
      submitButton.style.display = 'block';
  }
    
  }

  // Initially show first group of questions
  showQuestions(currentGroup);

 // Event listener for next button
nextButton.addEventListener('click', function() {
  currentGroup++;
  showQuestions(currentGroup);
  window.scrollTo({ top: 0, behavior: 'smooth' });
});
// Event listener for previous button
backButton.addEventListener('click', function() {
  currentGroup--;
  showQuestions(currentGroup);
  window.scrollTo({ top: 0, behavior: 'smooth' });
});

  // Disable next button and submit button initially
  submitButton.disabled = true;
});


