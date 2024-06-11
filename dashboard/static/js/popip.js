// pop up code 

$(document).ready(function(){
  // The speed of the popup fade in and out can be customized by changing the value of popUpToggleSpeed 
  const popUpToggleSpeed = 100; // Speed in milliseconds

  /* The click event is linked to the class .popup-button because 
   * there are multiple buttons that can trigger the click event
   */
  $(".popup-button").click(function(){
    // Toggle changes the visibility of the #popup-window by changing the css property display from hidden to visible.     
    $("#popup-window").toggle(popUpToggleSpeed);
  });
});
