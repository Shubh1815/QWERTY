Html5Qrcode.getCameras().then(devices => {
    if (!devices || !devices.length) {
        return;
    }
    let cameraId = devices[0].id;
    const html5QrCode = new Html5Qrcode("camera");

    document.getElementById("scan").addEventListener('click', () => {
        html5QrCode.start(
        cameraId,
        {
            fps: 10,
            qrbox: document.getElementById("camera").clientWidth

        },
        qrCodeMessage => {
            console.log(`QR Code detected: ${qrCodeMessage}`);
            enrollment_no.value = qrCodeMessage;
            student_data();
        },
        errorMessage => { })
        .catch(err => {
            console.log(`Unable to start scanning, error: ${err}`);
        });
    })

    document.getElementById("stop-scan").addEventListener('click', () => {
        html5QrCode.stop();
    })

}).catch(err => {
    console.log(err);
});

