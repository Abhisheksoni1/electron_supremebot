
/*select change*/

var x, i, j, selElmnt, a, b, c;
x = document.getElementsByClassName("custom-select");
for (i = 0; i < x.length; i++) {
  selElmnt = x[i].getElementsByTagName("select")[0];
  a = document.createElement("DIV");
  a.setAttribute("class", "select-selected");
  a.innerHTML = selElmnt.options[selElmnt.selectedIndex].innerHTML;
  x[i].appendChild(a);
  b = document.createElement("DIV");
  b.setAttribute("class", "select-items select-hide");
  for (j = 0; j < selElmnt.length; j++) {
    c = document.createElement("DIV");
    c.innerHTML = selElmnt.options[j].innerHTML;
    c.addEventListener("click", function(e) {
        var y, i, k, s, h;
        s = this.parentNode.parentNode.getElementsByTagName("select")[0];
        h = this.parentNode.previousSibling;
        for (i = 0; i < s.length; i++) {
          if (s.options[i].innerHTML == this.innerHTML) {
            s.selectedIndex = i;
            h.innerHTML = this.innerHTML;

            if (s.id == "taskSelected"){
                if ((h.innerHTML).split(":")[1] == "-"){

                document.getElementById("save_task").disabled = false;
                document.getElementById("size").value = "";
                document.getElementById("color").value = "";
                document.getElementById("keyword").value = "";
                document.getElementById("category").value = "";
                document.getElementById("timer").value = "";
                $('#proxy').val("0");
                $('#proxy').parent('.custom-select').children('.select-selected').html("No proxy");
//                document.getElementById("proxy").value = "";
                $('#category').val("0");
                $('#category').parent('.custom-select').children('.select-selected').html("-");

                $('#profile').val("0");
                $('#profile').parent('.custom-select').children('.select-selected').html("-");
                $('#timer').val("0");
                $('#timer').parent('.custom-select').children('.select-selected').html("No timer");
                }
                else{
                    var chartDataUrl = "http://127.0.0.1:8000/get_task"+"/"+(h.innerHTML).split(":")[1];
                    $.getJSON(chartDataUrl, function(data) {
                     var size = document.getElementById("size");
                     size.value = data['size'];
                     var color = document.getElementById("color");
                     color.value = data['color'];
                     var keyword = document.getElementById("keyword");
                     keyword.value = data['keyword'];
                     var category = document.getElementById("category");
                     category.value = data['category'];
//                     var profile = document.getElementById("profile")
//                     profile.innerHTML = data['profile']
                     var timer = document.getElementById("timer");
                     timer.value = data['timer'];
//                     var proxy = document.getElementById("proxy");
//                     proxy.value = data['proxy'];
                     document.getElementById("save_task").disabled = true;
                     $('#proxy').val(data['proxy']);
                     $('#proxy').parent('.custom-select').children('.select-selected').html(data['proxy']);
                     $('#category').val(data['category']);
                     $('#category').parent('.custom-select').children('.select-selected').html(data['category']);

                     $('#profile').val(data['profile']);
                     $('#profile').parent('.custom-select').children('.select-selected').html(data['profile']);
                     $('#timer').val(data['timer']);
                     $('#timer').parent('.custom-select').children('.select-selected').html(data['timer']);


        //             alert(data['category']);
                    });
                }
             }

             if (s.id == "profileSelected"){
                             if (h.innerHTML == "Profiles"){
                                document.getElementById("save_profile").disabled = false;
                                document.getElementById("address1").value = "";
                                document.getElementById("address2").value = "";
                                document.getElementById("city").value = "";
                                document.getElementById("zipcode").value = "";
                                document.getElementById("nameoncard").value = "";
                                document.getElementById("cardnumber").value = "";
                                document.getElementById("cvv").value = "";
                                document.getElementById("phonenumber").value = "";
                                document.getElementById("email").value = "";
                                $('#month').val("0");
                                $('#month').parent('.custom-select').children('.select-selected').html("Month");
                                $('#year').val("0");
                                $('#year').parent('.custom-select').children('.select-selected').html("Year");
                                $('#country').val("0");
                                $('#country').parent('.custom-select').children('.select-selected').html("Country");
                                $('#paymentoption').val("0");
                                $('#paymentoption').parent('.custom-select').children('.select-selected').html("Payment Option");
                             }
                             else{
                             var chartDataUrl = "http://127.0.0.1:8000/get_profile"+"/"+(h.innerHTML).split(":")[1];
                                                 $.getJSON(chartDataUrl, function(data) {
                             var address1 = document.getElementById("address1");
                             address1.value = data['address1'];
                             var address2 = document.getElementById("address2");
                             address2.value = data['address2'];
                             var city = document.getElementById("city");
                             city.value = data['city'];

                             var zipcode = document.getElementById("zipcode");
                             zipcode.value = data['zip_code'];
                             var cardnumber = document.getElementById("cardnumber");
                             cardnumber.value = data['card_number'];

                             var nameoncard = document.getElementById("nameoncard");
                             nameoncard.value = data['name'];
                             var cvv = document.getElementById("cvv");
                             cvv.value = data['cvv'];

                             var phonenumber = document.getElementById("phonenumber");
                             phonenumber.value = data['phone'];
                             var email = document.getElementById("email");
                             email.value = data['email'];
                             document.getElementById("save_profile").disabled = true;
                             $('#month').val(data['month']);
                             $('#month').parent('.custom-select').children('.select-selected').html(data['month']);

                             $('#year').val(data['year']);
                             $('#year').parent('.custom-select').children('.select-selected').html(data['year']);
                             $('#country').val(data['country']);
                             $('#country').parent('.custom-select').children('.select-selected').html(data['country']);
                             $('#paymentoption').val(data['payment_option']);
                             $('#paymentoption').parent('.custom-select').children('.select-selected').html(data['payment_option']);
//                             alert(data['name']);
                             });
                          }
             }
            y = this.parentNode.getElementsByClassName("same-as-selected");
            for (k = 0; k < y.length; k++) {
              y[k].removeAttribute("class");
            }
            this.setAttribute("class", "same-as-selected");
            break;
          }
        }
        h.click();
    });
    b.appendChild(c);
  }
  x[i].appendChild(b);
  a.addEventListener("click", function(e) {
      e.stopPropagation();
      closeAllSelect(this);
      this.nextSibling.classList.toggle("select-hide");
      this.classList.toggle("select-arrow-active");
    });
}
function closeAllSelect(elmnt) {
  var x, y, i, arrNo = [];
  x = document.getElementsByClassName("select-items");
  y = document.getElementsByClassName("select-selected");
  for (i = 0; i < y.length; i++) {
    if (elmnt == y[i]) {
      arrNo.push(i)
    } else {
      y[i].classList.remove("select-arrow-active");
    }
  }
  for (i = 0; i < x.length; i++) {
    if (arrNo.indexOf(i)) {
      x[i].classList.add("select-hide");
    }
  }
}
document.addEventListener("click", closeAllSelect);

/*select change end*/
