$(document).ready(function () {
  updateMain();
  $(window).on("resize", updateMain);

  $("#state_select").on("change", function () {
    var state_id = this.value;
    var url = `http://localhost:8000/cities/${state_id}`;
    $.get(url, function (data) {
      $("#cities").html(data.data);
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

function onSubmit(form) {
  var data = $(form).serializeArray();
  var indexed_array = {};
  data.map((n) => {
    if (n["value"] !== "") indexed_array[n["name"]] = n["value"];
  });

  indexed_array["latest"] = $("#latest")[0].checked;

  $("#results").hide();
  $("#loading-icon").show();

  var url = `http://localhost:8000/result`;
  console.log(indexed_array);

  $.ajax({
    url: url,
    type: "post",
    data: JSON.stringify(indexed_array),
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    success: function (response, textStatus, jqXHR) {
      $("#loading-icon").hide();
      $("#results").html(response.data);
      $("#results").show();
    },
    error: function (ajaxContext) {
      console.log(ajaxContext);
      $("#loading-icon").hide();
      $("html").html(ajaxContext.responseText)
    },
  });

  return false;
}
