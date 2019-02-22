<?php

/*
https://sikalabs.00webhostapp.com/api/delete.php
*/
header('content-type: application/json; charset=utf-8');
header("access-control-allow-origin: *");
 
//Creating Array for JSON response
$response = array();
 
// Check if we got the field from the user
if (isset($_POST['Id'])) {
 
    // Include data base connect class
    $filepath = realpath (dirname(__FILE__));
	require_once($filepath."/db_connect.php");
    $method = "DELETE";
    $id_err = '';
 
    // Connecting to database 
    $db = new DB_CONNECT();
    $id = $db->test_input($_POST['Id']);

        // check if integer
    if (!filter_var($id, FILTER_VALIDATE_INT)){
            $id_err = "Invalid";
    }

    //Check for errors and if there are none insert submitted data into database
    if ( $id_err == ''){

            // Fire SQL query to delete weather data by id
            $result = mysql_query("INSERT INTO Requests(Method, Id) VALUES('$method','$id')");
            if($result){

                $response["success"] = 1;
                $response["message"] = "Delete request successfully";
                echo json_encode($response);
            } else{

                $response["success"] = 0;
                $response["message"] = "Insertion unsuccessful";
                echo json_encode($response);
            }

    }else{

        $response["success"] = 0;
        $response["message"] = "Invalid data";
        echo json_encode($response);
    }

 }else {
    // If required parameter is missing
    $response["success"] = 0;
    $response["message"] = "Parameter(s) are missing. Please check the request";
 
    // Show JSON response
    echo json_encode($response);
}   
?>