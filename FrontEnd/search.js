var images_div = document.getElementById("image_grp");
var voice_btn = document.getElementById("voice_btn_start");
var search_input = document.getElementById("search_input");
var search_btn = document.getElementById("search_btn");
init();

function init(){
    console.log("connected");
    search_btn.addEventListener("click", function () {
        searchPhotos();
    });

}

function createImagediv(src){
    var div = document.createElement('div');
    div.classList="col-md-3 col-sm-6";
    var child_div = document.createElement('div');
    child_div.classList="thumbnail";
    var image = document.createElement('img');
    image.src = src;
    child_div.appendChild(image);
    div.appendChild(child_div);

    return div;
}

function searchPhotos() {  
    //clear previous photos result
    while(images_div.lastElementChild){
        images_div.removeChild(images_div.lastElementChild);
    }

    // get search input
    var search_text = search_input.value;
    console.log(search_text);

    //send request to backend
    var param = {
        "q": search_text
    };

    var apigClient = apigClientFactory.newClient();
    apigClient.searchGet(
        param,
        "",
        {}
    ).then(function(result){
        //TODO GET image url list, and call createImagediv(src)

        // var src = "https://miro.medium.com/fit/c/262/262/0*HkdY2U3dzajq4z9d.jpg";
        // var div = createImagediv(src);
        // images_div.appendChild(div);
        // console.log(result);
        var resultList = result["data"];
        var i;
        for(i = 0; i < resultList.length; i ++) {
            var tmpsrc = 'https://s3.amazonaws.com/photo-album-hw3/' + resultList[i];
            var div = createImagediv(tmpsrc);
            images_div.appendChild(div);
        }
        
    }).catch(function(result){
        console.log("Search failed");
    });
    //TODO delete the following 3 line

    // var src = "https://miro.medium.com/fit/c/262/262/0*HkdY2U3dzajq4z9d.jpg";
    // var div = createImagediv(src);
    // images_div.appendChild(div);

}