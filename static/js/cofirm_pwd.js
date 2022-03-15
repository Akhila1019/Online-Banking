function ValidationEvent() {
    var pwd = document.getElementById("password").value;
    var confirm_pwd = document.getElementById("confirm_password").value;
    var passw = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,20}$/;
    if (pwd != '' && confirm_pwd != '') {
        if(pwd.match(passw)){
            if(confirm_pwd.match(passw)){
                if(confirm_pwd == pwd){
                    alert("Successfull!");
                    return true;
                }
                else{
                    alert("Password mismatch!");
                    return false;
                }
            }
            else{
                alert("Password must be between 6 to 20 characters which should contain at least one numeric digit, one uppercase and one lowercase letter!");
                return false;
            }
        }
        else{
            alert("Password must be between 6 to 20 characters which should contain at least one numeric digit, one uppercase and one lowercase letter!");
            return false;
        }
    }
}