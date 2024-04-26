function updateSlider(slider, index) {
    var colors = ["darkgreen", "green" , "lightgreen", "blue", "orangered" , "coral", "red"];
    var texts = ["Agree", "Slightly Agree", "Less Agree", "Neutral", "Less Disagree", "Slightly Disagree", "Disagree"];
    var value = slider.value;
    var colorIndex = Math.min(Math.floor(value / 14), 6);

    slider.style.background = colors[colorIndex];
    para[index].innerHTML = texts[colorIndex];
    para[index].style.color = colors[colorIndex];
  }

  var volumeSliders = document.querySelectorAll(".volume-slider");
  var para = document.querySelectorAll(".para");

  volumeSliders.forEach(function(slider, index) {
    slider.oninput = function() {
      updateSlider(this, index);
      console.log("volume : " + this.value);
    };
  });

const navbar = document.getElementById('myNavbar');
    window.addEventListener('scroll', () => {
    if (window.scrollY > navbar.clientHeight) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});