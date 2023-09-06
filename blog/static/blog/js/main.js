
function readURL(input) {
    if (input.files && input.files[0]) {
        console.log("ooooooo")
       
        var reader = new FileReader();

        reader.onload = function (e) {
            console.log("ooooooo")
            $('#blah').attr('src', e.target.result);
        }

        reader.readAsDataURL(input.files[0]);
    }
}

$("#id_image").change(function(){
    readURL(this);
});
function readURL2(input) {
    if (input.files && input.files[0]) {
        console.log("ooooooo")
       
        var reader = new FileReader();

        reader.onload = function (e) {
            console.log("ooooooo")
            $('#blah2').attr('src', e.target.result);
        }

        reader.readAsDataURL(input.files[0]);
    }
}

$("#id_bgimage").change(function(){
    readURL2(this);
});
function myFunction() {
    console.log("dks;kfdsl;kfl;ds")
   document.getElementById("blah").src="desktop-wallpaper-white-backgrounds-plain-https-www-pop-white-background-white-thumbnail.jpg";}
if(window.history.replaceState){

    window.history.replaceState(null,null,window.location.href);

    console.log("jfdsljfkdl")
}
