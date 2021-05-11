$(document).ready(function () {
  var main = $("main"),
    header = $("header"),
    margin_height = header.height();
  main.css("height", Math.max($(window).height() - margin_height, main.height()));
  main.css("margin-top", margin_height);
});
