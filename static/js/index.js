
const file_map = {
  "#dm_gen": "dm_report_gen.py",
  "#db_refresh": "db_refresh.py",
  "#auto_insta": "start_bot.py",
}
let available_dates = []

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
  .on("changeDate", "#datepicker", function () {
    let date = $(this).datepicker('getDate');
    date = moment(date).format('YYYY-MM-DD')
    get_smart_chart(date)
    $(this).datepicker('hide');

    let idx = _.indexOf(available_dates, date) || 0
    $("#prev_date").data("date", available_dates[idx - 1])
    $("#next_date").data("date", available_dates[idx + 1])
  })
  .on("click", "button.date-btn", function () {
    let date = $(this).data("date")
    $('#datepicker').datepicker('update', date);
    $('#datepicker').datepicker('setDate', date);
  })

let tab = parse_url().searchKey.tab || "info"
const tab_map = {
  info: plot_info,
  chart: plot_chart,
  smart_log: plot_smart_log
}

$(window).on('load', function () {
  redraw()
})

function redraw() {
  $('[data-toggle="tooltip"]').tooltip('hide')

  $(".loader").removeClass("d-none");
  // funky way to execute stuff
  tab_map[tab]()
  $(`#nav_${tab}`).addClass("active")
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

function update_btn_color() {
  // update button color if script is running
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
      })
  })
  Prism.highlightAll();
}


function get_smart_chart(date) {
  $.ajax({
    url: "get_smart_log",
    method: "GET",
    dataType: 'json',
    data: { date: date }
  })
    .done(function (data) {
      $("#visual").attr("src", data.img)
    })

}

function make_calendar() {
  $.ajax({
    url: "get_calendar_dates",
    method: "GET",
    dataType: 'json',
  })
    .done(function (cal) {
      available_dates = cal.dates

      // date picker
      $('#datepicker').datepicker({
        format: 'yyyy/mm/dd',
        beforeShowDay: function (date) {
          return {
            enabled: _.includes(available_dates, moment(date).format('YYYY-MM-DD'))
          }
        },
        todayBtn: true,
        todayHighlight: true,
        startDate: cal.min,
        endDate: cal.max,
        defaultViewDate: cal.max
      });

      $("#prev_date").attr("data-date", cal.min)
      $("#next_date").attr("date-date", cal.max)

    })

}

// _________________________plot functions__________________________

function plot_info() {
  $('#log_template')
    .one('template', function () {
      update_btn_color()
    })
    .template({ target: "#main_placeholder" })
}

function plot_chart() {
  // script_status()
  $('#visual_template')
    .one('template', function () {
      $.ajax({
        url: "get_visual",
        method: "GET",
        dataType: 'json',
        // data: { file_name: file_name }
      })
        .done(function (data) {
          $("#visual").attr("src", data.img)
        })
    })
    .template({ target: "#main_placeholder" })
}

function plot_smart_log() {
  $('#smart_log_template')
    .one('template', function () {
      make_calendar()
    })
    .template({ target: "#main_placeholder" })
}