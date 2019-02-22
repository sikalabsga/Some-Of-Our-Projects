<?php

/*
https://sikalabs.00webhostapp.com/api/read_all.php
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
 
 // Fire SQL query to get all data from weather
$result = mysql_query("SELECT *FROM Requests") or die(mysql_error());
 
// Check for succesfull execution of query and no results found
if (mysql_num_rows($result) > 0) {
    
	// Storing the returned array in response
    $response["request"] = array();
 
	// While loop to store all the returned response in variable
    while ($row = mysql_fetch_array($result)) {
        // temperoary user array
        $request = array();
        $request["Method"] = $row["Method"];
        $request["Id"] = $row["Id"];
        $Id = $row["Id"];
		
		// Push all the items 
        array_push($response["request"], $request);
    }
    // On success
    $response["success"] = 1;
 
    // Show JSON response
    echo json_encode($response);
    $result_clear = mysql_query("DELETE FROM Requests WHERE Id='$Id'");
    
    if($result_clear){
        //

    }

}	
else 
{
    // If no data is found
	$response["success"] = 0;
    $response["message"] = "No Data Posted";
 
    // Show JSON response
    echo json_encode($response);
}

?>