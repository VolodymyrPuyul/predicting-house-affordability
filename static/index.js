// Initialize and add the map
function initMap() {
    // The location of Abu Dhabi
    const abuDhabi = { lat: 24.387, lng: 54.419 };
    // The map, centered at Abu Dhabi
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 10,
        center: abuDhabi,
    });

    // The marker, positioned at Abu Dhabi
    // const marker = new google.maps.Marker({
    //   position: abuDhabi,
    //   map: map,
    // Create the initial InfoWindow.
    let infoWindow = new google.maps.InfoWindow({
        content: "Click the map to select a location!",
        position: abuDhabi,
    });

    infoWindow.open(map);
    // Configure the click listener.
    map.addListener("click", (mapsMouseEvent) => {
        // Close the current InfoWindow.
        infoWindow.close();
        // Create a new InfoWindow.
        infoWindow = new google.maps.InfoWindow({
        position: mapsMouseEvent.latLng,
        });
        console.log(mapsMouseEvent.latLng.lat());
        // Print lat and lng to console
        $.post( "/district", {  
            lat: mapsMouseEvent.latLng.lat(),
            lng: mapsMouseEvent.latLng.lng()
        },
        function(district_info) { 
            var district_info = $.parseJSON(district_info);
            var district_name = district_info["district_name"];
            var district_id = district_info["district_id"]
            document.getElementById("districtCode").value = district_id;
            document.getElementById("openBtn").innerHTML = district_name

        //    console.log($.parseJSON(district_info));
            infoWindow.setContent(
                district_name
            );
            infoWindow.open(map);
    });


    });
    }

// function sleep(milliseconds) {
//     const start = Date.now();
//     while (Date.now() - start < milliseconds);
// }

function openForm() {
    document.getElementById("myForm").style.display = "block";
    var form = document.getElementById("myForm");
    // document.getElementById("open").style.display = "none";
    // When the user clicks anywhere outside of the form, close it
    window.onclick = function(event) {
        if (event.target == form) {
        form.style.display = "none";
    }
  }
    }
    
function closeForm() {
    document.getElementById("myForm").style.display = "none";
    // document.getElementById("open").style.display = "block";
    }

function slider(id, range) {
    document.getElementById(id).innerHTML = document.getElementById(range).value; 
  
    // Update the current slider value (each time you drag the slider handle)
    document.getElementById(range).oninput = function() {
      document.getElementById(id).innerHTML = this.value;
    }
}
