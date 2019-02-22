<?php

/*
https://sikalabs.00webhostapp.com/api/update.php
*/ 
 
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");
header("Connection: close");
 
//Creating Array for JSON response
$response = array();
 
// Check if we got the field from the user
if (isset($_POST['Id']) && isset($_POST['time']) && isset($_POST['every'])) {
 
    $id = $_POST['Id'];
    $time= $_POST['time'];
    $every= $_POST['every'];
    
    $method = "PUT";
 
    // Include data base connect class
    $filepath = realpath (dirname(__FILE__));
    require_once($filepath."/db_connect.php");
 
    // Connecting to database
    $db = new DB_CONNECT();
 
    // Fire SQL query to update weather data by id
    $result = mysql_query("UPDATE Schedules SET time='$time', every='$every' WHERE Id = '$id'");
 
    // Check for succesfull execution of query and no results found
    if ($result) {
        // successfully updation of temp (temperature)
        $response["success"] = 1;
        $response["message"] = "Schedule updated successfully.";
        $request_result = mysql_query("INSERT INTO Requests(Method,Id) VALUES('$method','$id' )");
 
        // Show JSON response
        echo json_encode($response);
    } else {
 
    }
} else {
    // If required parameter is missing
    $response["success"] = 0;
    $response["message"] = "Parameter(s) are missing. Please check the request";
 
    // Show JSON response
    echo json_encode($response);
}


?>