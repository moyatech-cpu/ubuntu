$(document).ready(function () {
  $.fn.serializeFormJSON = function () {

        var o = {};
        var a = this.serializeArray();
        $.each(a, function () {
            if (o[this.name]) {
                if (!o[this.name].push) {
                    o[this.name] = [o[this.name]];
                }
                o[this.name].push(this.value || '');
            } else {
                o[this.name] = this.value || '';
            }
        });
        return o;
    };

  function validateEmail(email) {
    var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
  }

  $('#submit_contact').on('click', function () {
      var form = $('#contact_form');
      datas = JSON.stringify(form.serializeArray())
      data = form.serializeFormJSON();
      
      c_name = false
      if('name' in data && data['name'] == '') {
        document.getElementById('name');
        c_name = true;
      }
      if(c_name) {
        document.getElementById("contact_us_message").innerHTML = "Sorry, We need First Name. Please complete the required fields.";
        document.getElementById('contact_us_message').style.color = "red";
        return false;
      }

      c_phone = false
      if('phone' in data && data['phone'] == '') {
        document.getElementById('phone');
        c_phone = true;
      }
      if(c_phone) {
        document.getElementById("contact_us_message").innerHTML = "Sorry, We need Phone Number. Please complete required fields.";
        document.getElementById('contact_us_message').style.color = "red";
        return false;
      }

      c_email = false
      if('email' in data && data['email'] == '') {
        document.getElementById('email');
        c_email = true;
      }
      if(c_email) {
        document.getElementById("contact_us_message").innerHTML = "Sorry, We need Email ID. Please complete required fields.";
        document.getElementById('contact_us_message').style.color = "red";
        return false;
      }

      c_message = false
      if('message' in data && data['message'] == '') {
        document.getElementById('message');
        c_message = true;
      }
      if(c_message) {
        document.getElementById("contact_us_message").innerHTML = "Sorry, We need Some Description. Please complete required fields.";
        document.getElementById('contact_us_message').style.color = "red";
        return false;
      }

      if (!validateEmail(data['email'])){
        document.getElementById('email').style.borderColor = "red";
        document.getElementById("contact_us_message").innerHTML = "Email is Invalid";
        document.getElementById('contact_us_message').style.color = "red";
        return false;
      }
      else {
        $.ajax({
            type: "POST",
            dataType: "json",
            contentType : "application/json",
            url: '/contact_us_lead',
            data: JSON.stringify({'jsonrpc': "2.0", 'method': "call", "params": {'datas' : datas}}),
            success: function (data) {
              document.getElementById("contact_us_message").innerHTML = "THANK YOU CONTACT US.";
              document.getElementById('contact_us_message').style.color = "green";
              document.getElementById('email').style.borderColor = "#5FBBF9";
              document.getElementById("contact_form").reset();
            },
            error: function(data){
                console.log("ERROR ", data);
            }
        });
      }
  });
});