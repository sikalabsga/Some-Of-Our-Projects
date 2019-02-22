<?php

/*
https://sikalabs.00webhostapp.com/api/update.php
*/ 
 
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");
header("Connection: close");
 
//Creating Array for JSON response
$response = array();
 
// Check if we got the field from the mobile user
if (isset($_POST['Id']) && isset($_POST['time']) && isset($_POST['every'])) {
 
    $method = "PUT";
    $id_err = $time_err = $every_err = '';
 
    // Include database config class
    $filepath = realpath (dirname(__FILE__));
    require_once($filepath."/db_connect.php");
 
    // Connecting to database
    $db = new DB_CONNECT();

        //validate data
    $id = $db->test_input($_POST['Id']);
    $time = $db->test_input($_POST['time']);
    $every = $db->test_input($_POST['every']);

    // check if integer
    if (!filter_var($id, FILTER_VALIDATE_INT)){
            $id_err = "Invalid";
    }
    // check if only contains letters and whitespace
    if (!preg_match("/^[a-zA-Z ]*$/", $every)){
            $every_err = "Invalid";
    }
    // check if time variable contains only number and colon character in the formats 0:00 or 00:00
    if(!preg_match("/^(?:2[0-3]|[01][0-9]|[0-9]):[0-5][0-9]$/", $time)){

        $time_err = "Invalid";
    }

    //Check for errors and if there are none insert submitted data into database
    if($id_err =='' and $time_err == '' and $every_err == ''){

            // Fire SQL query to update schedule data by id
            $result = mysql_query("UPDATE Schedules SET time='$time', every='$every' WHERE Id = '$id'");
         
            // Check for succesfull execution of query and no results found
            if ($result) {
                // Successful schedule update
                $response["success"] = 1;
                $response["message"] = "Schedule updated successfully.";
                $request_result = mysql_query("INSERT INTO Requests(Method,Id) VALUES('$method','$id' )");
         
                // Send JSON response
                echo json_encode($response);
            } else {
                $response["success"] = 0;
                $response["message"] = "Invalid data";
                echo json_encode($response);         
            }

    }
 

} else {
    // If required parameter is missing
    $response["success"] = 0;
    $response["message"] = "Parameter(s) are missing. Please check the request";
 
    // Show JSON response
    echo json_encode($response);
}


?>