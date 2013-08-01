/**
 * Created with PyCharm.
 * User: AlexUser
 * Date: 7/30/13
 * Time: 1:48 AM
 * To change this template use File | Settings | File Templates.
 */


//ALEXK below code is working and generating the correct geocode values
var geocoder = new google.maps.Geocoder();
var resolvedLocation;

function fetchLocation() {
    var address = document.getElementById('street').value + ', '
        + document.getElementById('city').value + ', '
        + document.getElementById('province').value;

    alert('fetching coordinates for address : ' + address);
    //based on sample from https://developers.google.com/maps/documentation/javascript/examples/geocoding-simple
    geocoder.geocode({ 'address': address}, function (results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            alert('Geocode generated: ' + results[0].geometry.location);
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


function getUserLocation() {
    // Try HTML5 geolocation
    if(navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var pos = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
            alert ('Your Identified Location is: ' + pos.toString());
            return pos;
        }, function() {
            handleNoGeolocation(true);
            return null;
        });
    } else {
        // Browser doesn't support Geolocation
        handleNoGeolocation(false);
        return null;
    }
}

function handleNoGeolocation(errorFlag) {
    if (errorFlag) {
        var content = 'Error: The Geolocation service failed.';
    } else {
        var content = 'Error: Your browser doesn\'t support geolocation.';
    }
    alert(content);
//    var options = {
//        map: map,
//        position: new google.maps.LatLng(60, 105),
//        content: content
//    };
//
//    var infowindow = new google.maps.InfoWindow(options);
//    map.setCenter(options.position);
}

