

var
  fileInput = document.getElementById('test-image-file'),
  info = document.getElementById('test-file-info'),
  preview = document.getElementById('test-image-preview');
fileInput.addEventListener('change', function () {
  preview.style.backgroundImage = '';
  if (!fileInput.value) {
    info.innerHTML = 'File not selected';
    return;
  }
  var file = fileInput.files[0];
  info.innerHTML = 'File: ' + file.name + '<br>' +
    'Size: ' + file.size + '<br>' +
    'LastModifiedDate: ' + file.lastModifiedDate;
  if (file.type !== 'image/jpeg' && file.type !== 'image/png' && file.type !== 'image/jpg') {
    alert('Unsupported image file');
    return;
  }
  var contenttype = "";
  if (file.type == 'image/jpeg'){
    contenttype = 'image/jpeg';
  }
  if (file.type == 'image/png'){
    contenttype = 'image/png';
  }
  if (file.type == 'image/jpg'){
    contenttype = 'image/jpg';
  }
  var param = {
    "key":file.name,
    "bucket": "photo-album-hw3",
    "Content-Type": contenttype,
    "Accept":file.type
  };
  var reader = new FileReader();
  reader.onload = function (e) {
    var
      data = e.target.result, // 'data:image/jpeg;base64,/9j/4AAQSk...(base64 encoded)...'   
      apigClient = apigClientFactory.newClient(),
      data_base64 = data.replace(/^data:image\/(png|jpg|jpeg);base64,/,"");
    apigClient.uploadBucketKeyPut(
      param,
      data_base64,
      {}
    ).then(function(result){
      alert("Upload Success");
    }).catch(function(result){
      alert("Failed");
    });
    preview.style.backgroundImage = 'url(' + data + ')';
  };
  reader.readAsDataURL(file);
});