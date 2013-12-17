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
    resolveSearchLocation(function (resolvedCoordResult,resolvedCoordStatus, resolvedAddrResult, resolvedAddrStatus) {
        console.log("DEBUG : back from callback, just before submit, " +
            "\n resolvedCoordResult = [" + resolvedCoordResult + "], " +
            "\n resolvedCoordStatus = [" + resolvedCoordStatus+ "], " +
            "\n resolvedAddrResult = [" + resolvedAddrResult + "], " +
            "\n resolvedAddrStatus = [" + resolvedAddrStatus + "].");
        if (resolvedCoordStatus != 'OK') {
            var confPopupResponse=confirm("Location cannot be defined for search. \nPress [OK] to use Toronto as default \n" +
                "or press [Cancel] if you wish to put the address or allow access to location via browser.");
            if (confPopupResponse==true){//user pressed OK , mean wants to use hardcoded default
                console.log("DEBUG : before SUBMIT, using Toronto as Default (43.67, -79.39).");
                document.getElementById('coordinatesForSearch').value = '(43.67, -79.39)';
                document.getElementById("mainForm").submit();
            } else {
                console.log("DEBUG : cancel pressed in confirmation message");
            }
            //alert("Did not get the location, put the smart thing there");
        } else {//resolved coordinates are OK
            document.getElementById('coordinatesForSearch').value = resolvedCoordResult;
            console.log("DEBUG : before SUBMIT for case of : resolved coordinates are OK.");
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
        geocoder.geocode({ 'address': address}, function (results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                console.log("DEBUG: google.maps.GeocoderStatus.OK ");
                if (!results[0]) {console.log("DEBUG: no results found ");}//array of results is empty
                myCallbackFunction(results[0].geometry.location, "OK",'placeholder','placeholder');
                console.log("DEBUG:Geocode generated (for user-provided address): " + results[0].geometry.location );
            } else {
                console.log("DEBUG:Geocode was not successful for the following reason: " + status);
                myCallbackFunction("EMPTY", status,'placeholder','placeholder');
            }
        });
    }
    else if (navigator.geolocation) {// address is empty ,get location from browser) - Try HTML5 geolocation
        console.log("DEBUG: inside elsif, address is not typed. BEFORE getCurrentPosition from Browser." );
        navigator.geolocation.getCurrentPosition(function getCurrentPositionSuccessFunction(position) {
            var pos = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
            //insert more custom code here
            document.getElementById("userCurrPosition").value = pos;
            document.getElementById("coordinatesForSearch").value = pos;
            console.log("DEBUG:Coordinate resolved (for browser-based coordinates): [" + pos +"], before defining the address ");

            //find a real street address based on browser-defined geolocation
            geocoder.geocode({'latLng': pos}, function(addrResults, addrStatus) {
                if (addrStatus == google.maps.GeocoderStatus.OK) {
                    console.log("DEBUG:addrStatus = google.maps.GeocoderStatus.OK, addrResults=" + addrResults[1].formatted_address);
                    if (addrResults[1]) {//set the "location" variable to auto-fetched address instead of user-defined
                        var locationBeforeSet = document.getElementById('location').value;

                        document.getElementById('location').value = addrResults[1].formatted_address;//results[1].formatted_address;
                        //var locationAfterSet=document.getElementById('location').value;
                        console.log("DEBUG: location after set = " + document.getElementById('location').value+ " invoking callback for submit" );
                        myCallbackFunction(pos, "OK",addrResults[1].formatted_address,"OK");
                    } else {
                        console.log("DEBUG:inside the else statement - Cannot find address by using the user coordinates");
                        alert('Cannot find address by using the user coordinates');
                    }
                } else {
                    console.log("DEBUG:inside the else statement - GeocoderStatus NOT OK ");
                    alert('Geocoder failed due to: ' + addrStatus + 'while converting coordinates to address');
                }
            });

        }, function getCurrentPositionFailureFunction() {
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




