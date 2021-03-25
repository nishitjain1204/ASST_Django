const webcamElement = document.getElementById('webcam');

const canvasElement = document.getElementById('canvas');

const snapSoundElement = document.getElementById('snapSound');

const webcam = new Webcam(webcamElement, 'user', canvasElement, snapSoundElement);


$("#webcam-switch").change(function () {
    if (this.checked) {
        $('.md-modal').addClass('md-show');
        webcam.start()
            .then(result => {
                cameraStarted();
                console.log("webcam started");
            })
            .catch(err => {
                console.log(err);
                displayError();
            });
    }
    else {
        cameraStopped();
        webcam.stop();
        console.log("webcam stopped");
    }
});

$('#cameraFlip').click(function () {

    webcam.flip();
    webcam.start();
});

$('#closeError').click(function () {
    $("#webcam-switch").prop('checked', false).change();
});

function displayError(err = '') {
    if (err != '') {
        
        $("#errorMsg").html(err);
    }
    console.log(err);
    $("#errorMsg").removeClass("d-none");
}

function cameraStarted() {
    $("#cameraControls").removeClass("d-none");
    $("#errorMsg").addClass("d-none");
    $('.flash').hide();
    $("#take-photo").removeClass('d-none');
    $("#webcam-caption").html("on");
    $("#webcam-control").removeClass("webcam-off");
    $("#webcam-control").addClass("webcam-on");
    $(".webcam-container").removeClass("d-none");
    if (webcam.webcamList.length > 1) {
        $("#cameraFlip").removeClass('d-none');
    }
    $("#wpfront-scroll-top-container").addClass("d-none");
    window.scrollTo(0, 0);
    $('body').css('overflow-y', 'hidden');
}

function cameraStopped() {
    $("#errorMsg").addClass("d-none");
    $("#wpfront-scroll-top-container").removeClass("d-none");
    $("#webcam-control").removeClass("webcam-on");
    $("#webcam-control").addClass("webcam-off");
    $("#cameraFlip").addClass('d-none');
    $(".webcam-container").addClass("d-none");
    $("#webcam-caption").html("Click to Start Camera");
    $('.md-modal').removeClass('md-show');
    $("#take-photo").addClass('d-none');

}



$("#take-photo").click(function () {
    $("#image_list").removeClass('d-none');
    beforeTakePhoto();
    let picture = webcam.snap();

    document.querySelector('#download-photo').href = picture;
    var img = document.createElement('img');
    img.src = picture;
    img.className = 'clicked_photo';
    if (img.src != "data:,") {
        console.log(img.src);
        document.getElementById('image_list').appendChild(img);

    }


    afterTakePhoto();
});

$("#download-photo").click(function () {
    beforeTakePhoto();
    let picture = document.querySelector('#download-photo').href;
    let image_list = document.getElementById('#image_list');
    let images = document.getElementsByClassName('clicked_photo');
    let data = '';
    var i;
    for (i = 0; i < images.length; i++) {
        data += images[i].src + ' '
    }
    console.log(data);
    // console.log('picture'+picture);
    $('#id_image_data').val(data);
    $('#createForm').submit();
    afterTakePhoto();
});

function beforeTakePhoto() {
    $('.flash')
        .show()

        .fadeOut(500)
        .css({ 'opacity': 0.7 });
    // window.scrollTo(0, 0); 
    $('#webcam-control').addClass('d-none');
    $('#cameraControls').addClass('d-none');
}

function afterTakePhoto() {
    // webcam.stop();
    var img = document.createElement("img");
    // $('#canvas').removeClass('d-none');
    // $('#take-photo').addClass('d-none');
    $('#exit-app').removeClass('d-none');
    $('#download-photo').removeClass('d-none');
    $('#image_list').removeClass('d-none');
    $('#resume-camera').removeClass('d-none');
    $('#cameraControls').removeClass('d-none');
}

function removeCapture() {
    $('#canvas').addClass('d-none');
    $('#webcam-control').removeClass('d-none');
    $('#cameraControls').removeClass('d-none');
    $('#take-photo').removeClass('d-none');
    $('#exit-app').addClass('d-none');
    $('#download-photo').addClass('d-none');
    $('#resume-camera').addClass('d-none');
}

$("#resume-camera").click(function () {
    webcam.stream()
        .then(facingMode => {
            removeCapture();
        });
});

$("#exit-app").click(function () {
    removeCapture();
    var a = $('#image_list');
    // $(a).remove();
    $("#image_list").addClass('d-none');

    $("#webcam-switch").prop("checked", false).change();
});