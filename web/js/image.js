var arrButtons = [{"Display_Text":"Home","URL":"Home.html",},{"Display_Text":"Image","URL":"Image.html"},{"Display_Text":"Container","URL":"Container.html"}];
var imageSource = [{"Display_Text":"Home", "src":"<i class='fa fa-home' aria-hidden='true' style='font-size:35px'></i>"},{"Display_Text":"Image","src":"<i class='fa fa-picture-o' aria-hidden='true' style='font-size:35px'></i>"},{"Display_Text":"Container","src":"<i class='fa fa-sellsy' aria-hidden='true' style='font-size:35px'></i>"}]
$(document).ready(function() {
  var tbl = "<table>";
  var tr = "<tr>";
  for (var i=0;i<arrButtons.length;i++) {
    var url = arrButtons[i].URL;
    var color = 'red';
    if (i == 0) {
      color = 'blue';
    }
    //alert(url);
    //var td = "<td style='padding:4px;'><input type='button' value='" + arrButtons[i].Display_Text + "' onclick=goto('" +url + "');  /></td>"  ;
    var td = "<td style='padding:4px;'><input class='menu_buttons textbox' type='button' value='" + arrButtons[i].Display_Text + "'  /><span style='display:none;'>" +url + "</span> </td>"  ;
    //var myDiv = "<div style='background-color:" + color + "'>" + url  + "</div>"
    tr = tr + td;
  }
  tr= tr + "</tr>";
  tbl = tbl +  tr + "</table>";

  $("#dvMenuBar").html(tbl);

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
$(document).on("click", ".image_buttons", function () {
    var id = $(this).attr("id");
    switch(id)
    {
        case "nginx_btn":
            $("#img_path").val("nginx:latest");
            break;
        case "docker_btn":
            $("#img_path").val("docker:latest");
            break;
        case "redis_btn":
            $("#img_path").val("redis:latest");
            break;
        case "ubuntu_btn":
            $("#img_path").val("ubuntu:latest");
            break;
        default:
            break;
    }
})

$(document).on("click", "#pull_img_btn", function (e) {
    e.preventDefault();
    var img_val = $("#img_path").val()
    var numrow = $('#img_container tr').length;
    //alert(img_val);
    //alert(numrow);
    if(img_val=="")
    {
        alert("Error:No image path");
    }
    else
    {
        //alert("Entered");
        var tr = "<tr id=img_list'" + numrow + "' align='center'><td><input type='checkbox' id='imagecheckBox" + numrow + "' name='containercheckBox" + numrow + "'></td>";
        //alert(tr);
        var td = "<td>" + img_val + "</td>";
        //alert(td);
        tr = tr + td + "</tr>";
        //alert(tr);
    }
    $("#img_container").append(tr);
})