
const file_map = {
  "#dm_gen": "dm_report_gen.py",
  "#db_refresh": "db_refresh.py",
  "#auto_insta": "start_bot.py",
}

$('body')
  .tooltip({
    selector: '[data-toggle="tooltip"]',
    container: 'body',
    animation: true,
    html: true,
    sanitize: false,
    boundary: 'window',
    // trigger: "click focus",
    delay: { "show": 100, "hide": 3000 }
  })
  .on("click", "button.btn-script", function () {
    let selector = "#" + $(this).attr("id")
    let file_name = file_map[selector]
    log_text(file_name)
  })

let tab = parse_url().searchKey.tab || "home"


$(window).on('load', function () {
  redraw()
})

function redraw() {
  $('[data-toggle="tooltip"]').tooltip('hide')
  const tab_map = {
    home: plot_home,
    log: plot_log
  }

  $(".loader").removeClass("d-none");
  // funky way to execute stuff
  tab_map[tab]()
}


function log_text(file_name) {
  $.ajax({
    url: "log",
    method: "GET",
    dataType: 'json',
    data: { file_name: file_name }
  })
    .done(function (data) {
      $("#log_placeholder").text(data.data)
      Prism.highlightAll();
    })
    .fail(function () {
      $("#log_placeholder").text("No Data")
      Prism.highlightAll();
    })
}

function ajax_call(url_hit, method = 'GET', bool_async = true) {
  // use get_ajax_call.done(function(data){  <code> })
  return $.ajax({
    url: url_hit,
    async: bool_async,
    method: method,
    dataType: 'json'
  })
}


function parse_url() {
  return g1.url.parse(location.href)
}

function update_url(obj) {
  var url = g1.url.parse(location.href).update(obj)
  history.pushState({}, '', '?' + url.search);
}

// _________________________plot functions__________________________

function plot_home() {

  // iterate through file map and check while  file is running
  _.each(file_map, function (file_name, id) {
    $.ajax({
      url: "chkrun",
      method: "GET",
      dataType: 'json',
      data: { file_name: file_name }
    })
      .done(function (data) {
        if (data.status)
          $(id).addClass("btn-outline-success")
        else
          $(id).addClass("btn-outline-danger")
        console.log(data);

      })
  })

}


function plot_log() {
  console.log("log")
}