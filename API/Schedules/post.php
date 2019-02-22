<?php

 
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");
header("Connection: close");
 
//Creating Array for JSON response
$response = array();

$method = "POST";
 
// Check if we got the field from the user
if (isset($_POST['Id']) && isset($_POST['action']) && isset($_POST['time']) && isset($_POST['every']) && isset($_POST['turn'])) {
 
    $id = $_POST['Id'];
    $action = $_POST['action'];
    $time = $_POST['time'];
    $every = $_POST['every'];
    $turn = $_POST['turn'];

    
 
    // Include data base connect class
    $filepath = realpath (dirname(__FILE__));
	require_once($filepath."/db_connect.php");
 
 
    // Connecting to database 
    $db = new DB_CONNECT();
    // Fire SQL query to insert data in weather
    $result = mysql_query("INSERT INTO Schedules(Id,action,time,every,turn) VALUES('$id','$action','$time','$every','$turn')");
 
    // Check for succesfull execution of query
    if ($result) {
        // successfully inserted 
        $response["success"] = 1;
        $response["message"] = "New schedule inserted.";
        
        
        $request_result = mysql_query("INSERT INTO Requests(Method,Id) VALUES('$method','$id')");
        
 
        // Show JSON response
        echo json_encode($response);
    } else {
        // Failed to insert data in database
        $response["success"] = 0;
        $response["message"] = "Something has been wrong";
 
        // Show JSON response
        echo json_encode($response);
    }
} else {
    // If required parameter is missing
    $response["success"] = 0;
    $response["message"] = "Parameter(s) are missing. Please check the request";
 
    // Show JSON response
    echo json_encode($response);
}
?>