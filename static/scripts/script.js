$(document).ready(function () {
  updateMain();
  $(window).on("resize", updateMain);

  $("#state_select").on("change", function () {
    var state_id = this.value;
    var url = `http://localhost:8000/cities/${state_id}`;
    $.get(url, function (data) {
      $("#cities").html(data);
    });
  });
});

function updateMain() {
  var main = $("main"),
    header = $("header"),
    margin_height = header.height();
  main.css(
    "height",
    Math.max($(window).height() - margin_height, main.height())
  );
  main.css("margin-top", margin_height);
}
