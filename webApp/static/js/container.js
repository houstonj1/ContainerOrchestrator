var arrButtons = [{"Display_Text":"Home","URL":"http://localhost/",},{"Display_Text":"Image","URL":"http://localhost/images"},{"Display_Text":"Container","URL":"http://localhost/containers"}];
var imageSource = [{"Display_Text":"Home", "src":"<i class='fa fa-home' aria-hidden='true' style='font-size:35px'></i>"},{"Display_Text":"Image","src":"<i class='fa fa-picture-o' aria-hidden='true' style='font-size:35px'></i>"},{"Display_Text":"Container","src":"<i class='fa fa-sellsy' aria-hidden='true' style='font-size:35px'></i>"}]
var containerSource =[{"Display_Text":"Create"},{"Display_Text":"Start"},{"Display_Text":"Stop"},{"Display_Text":"Remove"}];
$(document).ready(function() {
  var tbl = "<table>";
  var tr = "<tr>";
  for (var i=0;i<arrButtons.length;i++) {
    var url = arrButtons[i].URL;
    //alert(url);
    //var td = "<td style='padding:4px;'><input type='button' value='" + arrButtons[i].Display_Text + "' onclick=goto('" +url + "');  /></td>"  ;
    var td = "<td style='padding:4px;'><input class='menu_buttons textbox' type='button' value='" + arrButtons[i].Display_Text + "'  /><span style='display:none;'>" +url + "</span> </td>"  ;
    //var myDiv = "<div style='background-color:" + color + "'>" + url  + "</div>"
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
    var td = "<td style='padding:4px;'><input class='containerBtn containerBtns container_btn_click' type='button' value='" + containerSource[j].Display_Text + "'  /></td>" ;
    tr = tr + td;
    //alert(containerSource[j].Display_Text);
  }
  tr = tr + "</tr>";
  tbl = tbl + tr + "</table>";
  $("#container_menu").html(tbl);
});

$(document).on("mouseover",".menu_buttons",function() {
  var btn_offset = $(this).offset();
  //alert(btn_offset.left);
  //alert(btn_offset.top);
  var src;
  var imgKey = $(this).val();
  for(var i=0;i<imageSource.length;i++) {
    //alert(imageSource[i].Display_Text);
    if(imgKey == imageSource[i].Display_Text) {
      src = imageSource[i].src;
      //alert(src);
      break;
    }
  }
  $("#menu_img_icon").parent().css({position:'relative'});
  $("#menu_img_icon").css({top: (btn_offset.top)- (1.4*btn_offset.top), left: btn_offset.left + 80, position:'absolute'});
  //var img = "<img class='img_style' src='" + src + "' ></img>";
  var img = src
  $("#menu_img_icon").html(img);
  //$("#dvMenuBar").append(img);
})
$(document).on("mouseleave",".menu_buttons",function() {
  $("#menu_img_icon").html("");
})
function goto(url) {
  window.location.href = url;
//alert(url);
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
        //alert("Entered");
        disProp = "block";
        //alert(disProp);
        $("#create_container").css("display", disProp);
        $("#container_list").css("display", "none");
      }
      else {
        $("#create_container").css("display", "none");
        $("#container_list").css("display", "block");
      }
      var createConForm = [];
      var containerName = '';
      $(document).on('click', '#create_con', function (e) {
          //alert('enter');
          //e.preventDefault();
          createConForm.push($('#container_name').val());
          containerName = $('#container_name').val()
          createConForm.push($('#image_name').val());
          createConForm.push($('#command').val());
          if ($('#detach').is(':checked')) {
              createConForm.push('True');
          }
          else {
              createConForm.push('False');
          }
          createConForm.push($('#hostname').val());
          if ($('#network_dis').is(':checked')) {
              createConForm.push('True');
          }
          else {
              createConForm.push('False');
          }
          createConForm.push($('#network_mode').val());
          createConForm.push($('#mac').val());
          createConForm.push($('#ports').val());
          if ($('#publish_ports').is(':checked')) {
              createConForm.push('True');
          }
          else {
              createConForm.push('False');
          }
          //alert(createConForm);
          //alert('hi');
          //alert(createConForm.length);

          var sentForm = '';
          for (var j = 0; j < createConForm.length; j++) {
              if (j == createConForm.length - 1) {
                  var temp = createConForm[j];
              }
              else {
                  var temp = createConForm[j] + ',';
              }
              sentForm = sentForm.concat(temp);
          }
          //alert(sentForm);
          //alert('success');
          console.log(sentForm);
          $.ajax({                //This ajax call is to the python script that sends the data of create form
              type: 'POST',
              url: '/containers/create',
              data: { 'data': sentForm },
              success: function(response) {
                  $("#create_container").css("display", "none");
                  $("#container_list").css("display", "block");
                  $("#tbl_container").html(response);
              },
              error: function () { }    //error from the python script
          });
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
                $("#tbl_container").html(response);
            },
            error: function(response) {
                //placeholder
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
                          var status = ($('#con_list' + (i + 1)).find('td:eq(3)').html());
                          if (status == "running") {
                              var running = status;
                          }
                      }
                  }
              }
              console.log("HERE")
              console.log(running)
              var containerCreatorString = '';
              var status_containerIdString = btnVal + ',';
              for (var i = 0; i < containerId.length; i++) {
                  if (i == containerId.length - 1) {
                      var temp = containerId[i];
                      var temp2 = containerCreator[i];
                  }
                  else {
                      var temp = containerId[i] + ',';
                      var temp2 = containerCreator[i] + ',';
                  }
                  status_containerIdString = status_containerIdString.concat(temp);
                  containerCreatorString = containerCreatorString.concat(temp2);
                  //alert(status_containerIdString);
                  //alert(containerCreatorString);
              }
              if (running == 'running') {
                  alert("Container is Running. Needs to be stopped before removing.");
              }
              else {          //Added this else
                  $.ajax(         //Ajax call to the database to check if the person who clicked remove is the one that created the container.
                  {
                      type: 'GET',
                      url: 'http://localhost/static/php/removeContainer.php', //Need for url for the php script
                      data: { 'data': containerCreatorString },
                      datatype: 'text/plain',
                      success: function (data) {
                          if (data == success) {      //this will equal to whatever is returned by data.
                              $.ajax({                    //this call is to the python script with string" Status,ContainerID(similar to start/ stop)
                                  type: 'POST',
                                  url: '/containers',
                                  data: { 'data': status_containerIdString },
                                  success: function (response) {
                                      alert('Container successfully removed');
                                  },
                                  error: function () {
                                      alert("Container Not Removed");
                                  }
                              });
                          }
                      },
                      error: function () {
                          alert("Container not removed 2")
                      }
                  });
              }   //end of new logic
          }
      }
})
