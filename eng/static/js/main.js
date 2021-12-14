
(function ($) {
    "use strict";


    /*==================================================================
    [ Validate ]*/
    var input = $('.validate-input .input100');

    $('.validate-form').on('submit', function () {
        var check = true;
        var pass_val = '';
        var role = document.getElementById('hero');
        // alert(role);
        for (var i = 0; i < input.length; i++) {
            if ($(input[i]).attr('name') == 'pass') {
                pass_val = $(input[i]).val().trim();
                if (validate(input[i]) == false) {
                    showValidate(input[i]);
                    check = false;
                }
            }
            else if ($(input[i]).attr('name') == 'cpass' && $(input[i]).val().trim() != pass_val) {
                showValidate(input[i]);
                check = false;
            }
            else if (validate(input[i]) == false) {

                showValidate(input[i]);
                check = false;
            }
        }
        if (!check) return check;
        var len = input.length;
        var x = -1;
        if (len == 5)
            x = 3;
        else if (len == 2)
            x = 1;
        else
            return check;
        var pwdObj = input[x];
        var hashObj = new jsSHA("SHA-512", "TEXT", { numRounds: 1 });
        hashObj.update(pwdObj.value);
        var hash = hashObj.getHash("HEX");
        pwdObj.value = hash;
        if (len == 5) input[4].value = '';
        return check;
    });


    $('.validate-form .input100').each(function () {
        $(this).focus(function () {
            hideValidate(this);
        });
    });
    function validate(input) {
        if ($(input).attr('type') == 'email' || $(input).attr('name') == 'email') {
            if ($(input).val().trim().match(/^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{1,5}|[0-9]{1,3})(\]?)$/) == null) {
                return false;
            }
            return true;
        }
        else {
            if ($(input).val().trim() == '') {
                return false;
            }
            return true;
        }
    }

    function showValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).addClass('alert-validate');
    }

    function hideValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).removeClass('alert-validate');
    }

})(jQuery);