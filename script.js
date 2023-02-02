function formDetail() {
    var cname = document.getElementById('cname').value;
    var course = document.getElementById('course').value;
    var mobile = document.getElementById('mobile').value;
    var mail = document.getElementById('mail').value;

    var data = {
        "name": cname,
        "course": course,
        "mobile": mobile,
        "mail": mail
    }
    console.log(data);
}