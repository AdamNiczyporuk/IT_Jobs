document.addEventListener("DOMContentLoaded", function() {
    var typed = new Typed(".question", {
        strings: ["What are you looking for"],
        typeSpeed: 40,
        showCursor: false,
        onComplete: function() {
            setTimeout(function() {
                var typedDots = new Typed(".question-marks", {
                    strings: ["???"],
                    typeSpeed: 30,
                    loop: true,
                    backSpeed: 50,
                    backDelay: 4000
                });
            }, 500);
        }
    });

    var searchButton = document.getElementById("searchButton");
    if (searchButton) {
        console.log("Search button found");
        searchButton.addEventListener("click", function() {
            var searchQuery = document.getElementById("keywordSearchBar").value;
            var locationQuery = document.getElementById("locationSearchBar").value;
            console.log("Search button clicked");
            // alert(searchQuery + " " + locationQuery);

            fetch('/jobs',{
                method: 'POST',
                headers:{
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    keyword: searchQuery,
                    location: locationQuery
                })
                })
                .then(response => response.json())
                .then(data => {
                    if(data.message){
                        alert(data.message);
                    
                    }
                    else{
                        console.log(data);
                    }
                })
                .catch(error => console.error('Error:', error));
        });
    } else {
        console.log("Search button not found");
    }
});