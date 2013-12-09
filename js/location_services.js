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

function processAndSubmit() {
    console.log("DEBUG : inside processAndSubmit");
    //experimenting with callback: the function is defined here but the value for the function will be sent inside
    resolveSearchLocation(function (resolvedLocationResult,resolvedLocationStatus) {
        console.log("DEBUG : back from callback, just before submit, " +
            "resolvedLocationResult = [" + resolvedLocationResult + "], " +
            "resolvedLocationStatus = [" + resolvedLocationStatus+ "]");
        if (resolvedLocationStatus != 'OK') {
            var r=confirm("Location cannot be defined for search. \nPress OK to use Toronto as default \n" +
                "or press Cancel if you wish to put the address or allow access to location via browser.");
            if (r==true){
                console.log("DEBUG : using Toronto as Default (43.67, -79.39) and Submitting.");
                document.getElementById('coordinatesForSearch').value = '(43.67, -79.39)';
                document.getElementById("mainForm").submit();
            } else {
                console.log("DEBUG : cancel pressed in confirmation message");
            }
            //alert("Did not get the location, put the smart thing there");
        } else {
            document.getElementById('coordinatesForSearch').value = resolvedLocationResult;
            console.log("DEBUG : before SUBMIT");
            document.getElementById("mainForm").submit();
        }
    });
}

//function to resolve the original search location
// by ether using the current location of user utilizing browser capabilities
// or converting the requested location into geocode
function resolveSearchLocation(myCallbackFunction) {
    console.group("DEBUG:inside resolveSearchLocation");
    var address = "";
    if (document.getElementById("location").value != "") { //check that value is empty string
        address = document.getElementById("location").value;
        console.log("DEBUG : captured address is:  " + address);
    }
    else {
        console.log("DEBUG: user-provided location is empty");
    }

    if (address && !('' == address)) { // if the address string is not empty - use GOOGLE API to get loc by addr.
        console.log("DEBUG: address string is not empty. Before use GOOGLE API to get loc by addr. ");
        //duplicate from the above code, need to be refactored after test
        geocoder.geocode({ 'address': address}, function (results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                console.log("DEBUG: google.maps.GeocoderStatus.OK ");
                if (!results[0]) {console.log("DEBUG: no results found ");}//array of results is empty
                myCallbackFunction(results[0].geometry.location, "OK");
                console.log("DEBUG:Geocode generated (for user-provided address): " + results[0].geometry.location );
            } else {
                console.log("DEBUG:Geocode was not successful for the following reason: " + status);
                myCallbackFunction("EMPTY", status);
            }
        });
    }
    else if (navigator.geolocation) {// (address is empty - get location from browser) - Try HTML5 geolocation
        console.log("DEBUG: inside elsif, address is not typed. BEFORE getCurrentPosition from Browser." );
        navigator.geolocation.getCurrentPosition(function (position) {
            var pos = new google.maps.LatLng(position.coords.latitude,
                position.coords.longitude);
            //console.log("DEBUG: Geocode generated:"  + pos);
            //insert more custom code here
            document.getElementById("userCurrPosition").value = pos;
            document.getElementById("coordinatesForSearch").value = pos;
            myCallbackFunction(pos);
        }, function () {
            //handleNoGeolocation(true);
            myCallbackFunction("EMPTY", "Error: The Geolocation service failed to fetch the coordinates from browser.");
        });
    } else {// Browser doesn't support Geolocation
        console.log("DEBUG:Handling NoGeolocation case" );
        //handleNoGeolocation(false);
        myCallbackFunction("", "Error: Your browser doesnt support geolocation.");
    }

    console.groupEnd();
}

function handleNoGeolocation(errorFlag) {
    if (errorFlag) {
        var content = 'Error: The Geolocation service failed.';
        console.log("DEBUG:Error: The Geolocation service failed");
    } else {
        var content = 'Error: Your browser doesnt support geolocation.';
        console.log("DEBUG:Error: Your browser doesnt support geolocation.");
    }

}




