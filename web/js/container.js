var arrButtons = [{"Display_Text":"Home","URL":"Home.html",},{"Display_Text":"Image","URL":"Image.html"},{"Display_Text":"Container","URL":"Container.html"}];
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
    if (btnVal == "Create")
    {
        var disProp = $("#create_container").css("display");
        if (disProp == "none")
        {
            //alert("Entered");
            disProp = "block";
            //alert(disProp);
            $("#create_container").css("display", disProp);
            $("#container_list").css("display", "none");
        }
    }
    else if(btnVal=="Stop")
    {
        var containerId = [];
        var div = '<div>';
        var tableRow = $('#tbl_container tr').length-1;
        var checkedItem = 0;
        //alert(tableRow);
        for(var i=0;i<tableRow;i++)
        {
            var containerrow = $('#tbl_container').find("tr").eq(i + 1).html();
            if ((i) < tableRow)
            {
                var checked = $('#containercheckBox' + (i + 1)).is(':checked');
                if (checked == true)
                {
                    checkedItem = checkedItem +1;
                    //alert(checked);
                    containerId.push($('#con_list' + (i + 1)).find('td:eq(1)').html());
                   
                    //alert(containerId);
                } 
            }
        }
        for(var i=0;i<containerId.length;i++)
        {
            var par = '<p>' + containerId[i] + '</p>';
            div = div + par;
            //alert(div);
        }
        div = div + '</div>';
        //alert(div);
        if((containerForm == "block") && (checkedItem > 0))
        {
            //alert("Entered");
            $('#stopped_list').html(div);
            $('#container_list').css("display", "none");
            $('#stopped_list').css("display", "block");
        }

    }
})


