<?php

/*
https://sikalabs.00webhostapp.com/api/delete.php
*/
header('content-type: application/json; charset=utf-8');
header("access-control-allow-origin: *");
header("Connection: Close"); 
//Creating Array for JSON response
$response = array();
 
// Check if we got the field from the IOT device
if (isset($_POST['Id'])) {
    $id = $_POST['Id'];
 
    // Include data base connect class
    $filepath = realpath (dirname(__FILE__));
	require_once($filepath."/db_connect.php");
 
    // Connecting to database 
    $db = new DB_CONNECT();
    
    if($id == 0){

            // Fire SQL query to delete weather data by id
            $result = mysql_query("DELETE FROM Schedules *");
            if ($result) {
                $response["message"] = "Schedule deletion successful.";
                echo json_encode($response);
            }
    }

 
 }   
?>