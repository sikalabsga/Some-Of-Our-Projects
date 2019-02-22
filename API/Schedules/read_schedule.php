<?php

/*
https://sikalabs.00webhostapp.com/api/specific.php?id=3
*/
 
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");
 
//Creating Array for JSON response
$response = array();
 
// Include data base connect class
$filepath = realpath (dirname(__FILE__));
require_once($filepath."/db_connect.php");
 
 // Connecting to database
$db = new DB_CONNECT();
 
// Check if we got the field from the user
if (isset($_POST["Id"])) {
    $id = $_POST["Id"];
 
     // Fire SQL query to get weather data by id
    $result = mysql_query("SELECT *FROM Schedules WHERE Id = '$id'");
    
    //If returned result is not empty
    if (!empty($result)) {
 
        // Check for succesfull execution of query and no results found
        if (mysql_num_rows($result) > 0) {
            
            // Storing the returned array in response
            $result = mysql_fetch_array($result);
            
            // temperoary user array
            $Schedule = array();
            $Schedule["Id"] = $result["Id"];
            $Schedule["action"] = $result["action"];
            $Schedule["time"] = $result["time"];
            $Schedule["every"] = $result["every"];
            $Schedule["turn"] = $result["turn"];
          
            $response["success"] = 1;
 
            $response["Schedule"] = array();
            
            // Push all the items 
            array_push($response["Schedule"], $Schedule);
 
            // Show JSON response
            echo json_encode($response);
        } else {
            // If no data is found
            $response["success"] = 0;
            $response["message"] = "No Schedule data found";
 
            // Show JSON response
            echo json_encode($response);
        }
    } else {
        // If no data is found
        $response["success"] = 0;
        $response["message"] = "No Schedule data found";
 
        // Show JSON response
        echo json_encode($response);
    }
} else {
    // If required parameter is missing
    $response["success"] = 0;
    $response["message"] = "Parameter(s) are missing. Please check the request";
 
    // echoing JSON response
    echo json_encode($response);
}
?>