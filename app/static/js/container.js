var arrButtons = [{ "Display_Text": "Home", "URL": "/", }, { "Display_Text": "Images", "URL": "/images" }, { "Display_Text": "Containers", "URL": "/containers" }, { "Display_Text": "Help", "URL": "/help" }];
var imageSource = [{ "Display_Text": "Home", "src": "<i class='fa fa-home' aria-hidden='true' style='font-size:35px'></i>" }, { "Display_Text": "Images", "src": "<i class='fa fa-picture-o' aria-hidden='true' style='font-size:35px'></i>" }, { "Display_Text": "Containers", "src": "<i class='fa fa-sellsy' aria-hidden='true' style='font-size:35px'></i>" }, { "Display_Text": "Help", "src": "<i class='fa fa-question-circle' aria-hidden='true' style='font-size:35px'></i>" }];
var containerSource =[{"Display_Text":"Create"},{"Display_Text":"Start"},{"Display_Text":"Stop"},{"Display_Text":"Remove"}];
$(document).ready(function() {
  var tbl = "<table>";
  var tr = "<tr>";
  for (var i=0;i<arrButtons.length;i++) {
    var url = arrButtons[i].URL;
    var td = "<td style='padding:4px;'><input class='menu_buttons textbox' type='button' value='" + arrButtons[i].Display_Text + "'  /><span style='display:none;'>" +url + "</span> </td>"  ;
    tr = tr + td;
  }
  tr= tr + "</tr>";
  tbl = tbl +  tr + "</table>";
  $("#dvMenuBar").html(tbl);
  tbl = "";
  tr = "";
  tbl = "<table>";
  tr = "<tr>";
  for(var j=0;j<containerSource.length;j++) {
    var td = "<td style='padding:4px;'><input class='containerBtn containerBtns container_btn_click' type='button' value='" + containerSource[j].Display_Text + "' style='box-shadow: 2px 2px 2px #888888;' /></td>" ;
    tr = tr + td;
  }
  tr = tr + "</tr>";
  tbl = tbl + tr + "</table>";
  $("#container_menu").html(tbl);
});

$(document).on("mouseover",".menu_buttons",function() {
  var btn_offset = $(this).offset();
  var src;
  var imgKey = $(this).val();
  for(var i=0;i<imageSource.length;i++) {
    if(imgKey == imageSource[i].Display_Text) {
      src = imageSource[i].src;
      break;
    }
  }
  $("#menu_img_icon").parent().css({position:'relative'});
  $("#menu_img_icon").css({top: (btn_offset.top)- (1.4*btn_offset.top), left: btn_offset.left + 80, position:'absolute'});
  var img = src
  $("#menu_img_icon").html(img);
})
$(document).on("mouseleave",".menu_buttons",function() {
  $("#menu_img_icon").html("");
})
function goto(url) {
  window.location.href = url;
}
$(document).on("click", ".menu_buttons", function() {
  var $td = $(this).parent("td");
  var $span = $td.children("span");
  window.location.href = $span.text();
})

$(document).on("click", ".container_btn_click", function () {
    var btnVal = $(this).val();
    var containerForm = $('#container_list').css('display');
    var containerId = [];
    if (btnVal == "Create") {
      var disProp = $("#create_container").css("display");
      if (disProp == "none") {
        disProp = "block";
        $("#create_container").css("display", disProp);
        $("#container_list").css("display", "none");
      }
      else {
        $("#create_container").css("display", "none");
        $("#container_list").css("display", "block");
      }
      var createConForm = [];
      var containerName = '';
      $("#create_container").submit(function (e) {
        $('#create_container').attr("disabled",true);
        e.preventDefault();
        var formValid = false;
        var valid = [];
        var pattern = /\w+/;
        valid.push(pattern.test($('#container_name').val()));
        createConForm.push($('#container_name').val());
        pattern = /\w+:\w+/;
        valid.push(pattern.test($('#image_name').val()));
        createConForm.push($('#image_name').val());
        createConForm.push($('#command').val());
        createConForm.push($('#hostname').val());
        if ($('#network_dis').is(':checked')) {
          createConForm.push('False');
        } else {
          createConForm.push('True');
        }
        pattern = /(bridge|host|none)/;
        valid.push(pattern.test($('#network_mode').val()));
        createConForm.push($('#network_mode').val());
        createConForm.push($('#mac').val());
        createConForm.push($('#ports').val());
        if ($('#publish_ports').is(':checked')) {
          createConForm.push('True');
        } else {
          createConForm.push('False');
        }
        if (valid.every(function(val){return val == true;}) == true){
          var sentForm = '';
          for (var j = 0; j < createConForm.length; j++) {
            if (j == createConForm.length - 1) {
              var temp = createConForm[j];
            } else {
              var temp = createConForm[j] + ',';
            }
            sentForm = sentForm.concat(temp);
          }
          $.ajax({
            type: 'POST',
            url: '/containers/create',
            data: { 'data': sentForm },
            success: function(response) {
              $("#create_return_table").html(response);
              $("#create_container").css("display", "none");
              $("#container_list").css("display", "block");
              },
            error: function () {
            }
          });
        }
      });
    }
    else if (btnVal == "Stop" || btnVal == "Start") {
        var tableRow = $('#tbl_container tr').length-1;
        for(var i=0;i<tableRow;i++)
        {
            var containerrow = $('#tbl_container').find("tr").eq(i + 1).html();
            if ((i) < tableRow)
            {
                var checked = $('#containercheckBox' + (i + 1)).is(':checked');
                if (checked == true)
                {
                  containerId.push($('#con_list' + (i + 1)).find('td:eq(2)').html());
                }
            }
        }
        var status_ContainerIds = btnVal + ',';
        for (var i = 0; i < containerId.length; i++) {
            if (i == containerId.length - 1) {
                var container = containerId[i];
            }
            else {
                var container = containerId[i] + ',';
            }
            var status_ContainerIds = status_ContainerIds.concat(container);
        }
        $.ajax({
            type: 'POST',
            url: '/containers',
            data: { 'data':status_ContainerIds },                 //Sending the string as Status,ContainerID. Ex: "Stop,Container1,Container2". Use ',' to split the string in python.
            dataType: 'html',
            success: function(response) {
                $("#container_return_table").html(response);
            },
            error: function(response) {
            }
        });
      }
      else {
          if (btnVal == 'Remove') {
            var containerCreator = [];
            var tableRow = $('#tbl_container tr').length - 1;
            for (var i = 0; i < tableRow; i++) {
              var containerrow = $('#tbl_container').find("tr").eq(i + 1).html();
              if ((i) < tableRow) {
                var checked = $('#containercheckBox' + (i + 1)).is(':checked');
                if (checked == true) {
                  containerId.push($('#con_list' + (i + 1)).find('td:eq(2)').html());
                  containerCreator.push($('#con_list' + (i + 1)).find('td:eq(4)').html());
                }
              }
            }
            var containerCreatorString = '';
            var status_containerIdString = btnVal + ',';
            for (var i = 0; i < containerId.length; i++) {
              if (i == containerId.length - 1) {
                var temp = containerId[i];
              }
              else {
                var temp = containerId[i] + ',';
              }
              status_containerIdString = status_containerIdString.concat(temp);
            }
            $.ajax({
              type: 'POST',
              url: '/containers',
              data: { 'data': status_containerIdString },
              success: function (response) {
                $("#container_return_table").html(response);
              },
              error: function () {
              }
            });
          }
        }
      })
