/**
 * Created with PyCharm.
 * Set of JS functions that are dealing with the geo-location and conversions between address and coordinates
 * User: AlexUser
 * Date: 7/30/13
 * Time: 1:48 AM
 * To change this template use File | Settings | File Templates.
 */


//ALEXK below code is working and generating the correct geocode values
var geocoder = new google.maps.Geocoder();
var resolvedLocation;

// function to return the geolocation while taking as input the address from the HTML page and returning the location
function fetchLocation() {
    var address = document.getElementById('street').value + ', '
        + document.getElementById('city').value + ', '
        + document.getElementById('province').value;

    //alert('fetching coordinates for address : ' + address);
    //based on sample from https://developers.google.com/maps/documentation/javascript/examples/geocoding-simple
    geocoder.geocode({ 'address': address}, function (results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            //alert('Geocode generated: ' + results[0].geometry.location);
            document.getElementById('location').value = results[0].geometry.location;
            resolvedLocation = results[0].geometry.location;
        } else {
            alert('Geocode was not successful for the following reason: ' + status);
        }
    });
    document.getElementById('location').value = resolvedLocation;
    // for some reason this piece jumps in execution before the call to geocoder.geocode (...)
    //alert('value of resolvedLocation is : ' + resolvedLocation);
    //alert('value of location is : ' + document.getElementById('location').value);
}


//function to resolve the original search location
// by ether using the current location of user utilizing browser capabilities
// or converting the requested location into geocode
function resolveSearchLocation()
{
    //alert('debug: INSIDE THE resolveSearchLocation! ');

    var address="";
        if ( null != document.getElementById("location") ){ //check that value is not null
            address = document.getElementById("location").value;
            //alert('debug : captured address :  ' + address);
        }
    else{//remove this else in cleanup
            //alert('debug : location is null ');
        }

    if ( address && !(''==address) ){ // if the address string is not empty - use GOOGLE API to get loc by addr.
        //alert('debug : INSIDE THE first IF ');
        //duplicate from the above code, need to be refactored after test
        geocoder.geocode({ 'address': address}, function (results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                //alert('Geocode generated: ' + results[0].geometry.location); //to do :remove this debug message
                document.getElementById('requestedSearchLocation').value = results[0].geometry.location;
                document.getElementById('coordinatesForSearch').value = results[0].geometry.location;
                resolvedLocation = results[0].geometry.location;
            } else {
                alert('Geocode was not successful for the following reason: ' + status);
            }
        });
    }
    else if(navigator.geolocation) {// (address is empty - get location from browser) - Try HTML5 geolocation
        //alert('debug : INSIDE THE ELSIF  ');
        navigator.geolocation.getCurrentPosition(function(position) {
            var pos = new google.maps.LatLng(position.coords.latitude,
                position.coords.longitude);
            //alert('Geocode generated: ' + pos);//to do :remove this debug message
            //insert more custom code here
            document.getElementById("userCurrPosition").value = pos;
            document.getElementById("coordinatesForSearch").value = pos;
        }, function() {
            handleNoGeolocation(true);
        });
    } else {
        //alert('debug : INSIDE THE final else ');
        // Browser doesn't support Geolocation
        handleNoGeolocation(false);
    }

    if ( document.getElementById("coordinatesForSearch").value == "initial")
    {
        alert("coordinatesForSearch=["+ document.getElementById("coordinatesForSearch").value +" ]. Oops, location for search could not be defined. Please either populate the location field or verify that your browser is allowing use of geologation");
        return false;
    }
}

function handleNoGeolocation(errorFlag) {
    if (errorFlag) {
        var content = 'Error: The Geolocation service failed.';
    } else {
        var content = 'Error: Your browser doesn\'t support geolocation.';
    }

}




