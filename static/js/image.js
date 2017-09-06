var arrButtons = [{ "Display_Text": "Home", "URL": "/", }, { "Display_Text": "Images", "URL": "/images" }, { "Display_Text": "Containers", "URL": "/containers" }, { "Display_Text": "Help", "URL": "/help" }];
var imageSource = [{ "Display_Text": "Home", "src": "<i class='fa fa-home' aria-hidden='true' style='font-size:35px'></i>" }, { "Display_Text": "Images", "src": "<i class='fa fa-picture-o' aria-hidden='true' style='font-size:35px'></i>" }, { "Display_Text": "Containers", "src": "<i class='fa fa-sellsy' aria-hidden='true' style='font-size:35px'></i>" }, { "Display_Text": "Help", "src": "<i class='fa fa-question-circle' aria-hidden='true' style='font-size:35px'></i>" }];
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
$(document).on("click", '#pull_img_btn', function(){
  var re = /\w+:\w/;
  var imageName = document.getElementById('img_path').value;
  var validateName = re.test(imageName);
  console.log("RE" + validateName);
  console.log(imageName);
  if(validateName == true){
    $.ajax({
      type: 'POST',
      url: '/images',
      data: {'name':imageName},
      success: function(response){
        console.log("HERE");
        $("#img_return_table").html(response);
      }
    })
  } else {
    $.ajax({
      type: 'POST',
      url: '/images/pull_name_fail',
      success: function(response){
        console.log("HERE");
        $("#img_return_table").html(response);
      }
    })
  }
})
$(document).on("click", "#rmv_img_btn", function(){
  var imageList = [];
  var imageNames = "";
  var btnVal = $(this).val();
  var table = $('#img_container tr').length-1;
  for(var i=0; i<table; i++){
    var row = $('#img_container').find('tr').eq(i+1).html();
    if((i)<table){
      var checked = $('#imagecheckBox' + (i+1)).is(':checked');
      if(checked==true){
        var name = $('#img_list'+(i+1)).find('td:eq(1)').html() + ':' + $('#img_list'+(i+1)).find('td:eq(2)').html();
        imageList.push(name);
      }
    }
  }
  for(var i=0;i<imageList.length; i++){
    if(i == imageList.length-1){
      imageNames = imageNames.concat(imageList[i]);
    } else {
      imageNames = imageNames.concat(imageList[i] + ',');
    }
  }
  console.log(imageNames);
  $.ajax({
    type: 'POST',
    url: '/images/remove',
    data: {'list':imageNames},
    success: function(response){
      console.log("HERE")
      $("#img_return_table").html(response);
    }
  });
})
