var firebaseConfig = {
    apiKey: "AIzaSyC87WZEoXzppPa1OWotrHglyaUX1zXKJf4",
    authDomain: "regi-a7a96.firebaseapp.com",
    databaseURL: "https://regi-a7a96-default-rtdb.firebaseio.com",
    projectId: "regi-a7a96",
    storageBucket: "regi-a7a96.appspot.com",
    messagingSenderId: "840385202733",
    appId: "1:840385202733:web:2e22506b1872bc3cb546a4",
    measurementId: "G-YEMMTXTW87"
};
firebase.initializeApp(firebaseConfig);
firebase.analytics();


$("#btn-resetPassword").click(function () {
    var auth = firebase.auth();
    var email = $("#email").val();

    if (email != "") {
        auth.sendPasswordResetEmail(email).then(function () {
            window.alert("Email has been sent to you, Please check and verify.");
        })
            .catch(function (error) {
                var errorCode = error.code;
                var errorMessage = error.message;

                console.log(errorCode);
                console.log(errorMessage);

                window.alert("Message : " + errorMessage);
            });
    }

    else {
        window.alert("Please write your email first.");
    }
});