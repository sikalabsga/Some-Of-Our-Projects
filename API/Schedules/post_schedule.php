<?php

 
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");
header("Connection: close");
 
//Creating Array for JSON response
$response = array();

$method = "POST";
$id_err = $action_err = $time_err = $every_err = $turn_err = '';
 
// Check if we got the field from the mobile phone user
if (isset($_POST['Id']) && isset($_POST['action']) && isset($_POST['time']) && isset($_POST['every']) && isset($_POST['turn'])) {
    
 
    // Include data base connect class
    $filepath = realpath (dirname(__FILE__));
    require_once($filepath."/db_connect.php");
 
 
    // Connecting to database 
    $db = new DB_CONNECT();

        //validate data
    $id = $db->test_input($_POST['Id']);
    $action= $_POST['action'];
    $time = $db->test_input($_POST['time']);
    $every = $db->test_input($_POST['every']);
    $turn = $db->test_input($_POST['turn']);

    // check if integer
    if (!filter_var($id, FILTER_VALIDATE_INT)){
            $id_err = "Invalid";
    }

    // check if only contains letters and whitespace
    if (!preg_match("/^[a-zA-Z _]*$/", $action)){
            $action_err = "Invalid";
    }

    // check if only contains letters and whitespace
    if (!preg_match("/^[a-zA-Z ]*$/", $every)){
            $every_err = "Invalid";
    }

    // check if only contains letters and whitespace
    if (!preg_match("/^[a-zA-Z ]*$/", $turn)){
            $turn_err = "Invalid";
    }
    // check if time variable contains only number and colon character in the formats 0:00 or 00:00
    if(!preg_match("/^(?:2[0-3]|[01][0-9]|[0-9]):[0-5][0-9]$/", $time)){

        $time_err = "Invalid";
    }

    //Check for errors and if there are none insert submitted data into database
    if ($id_err =='' and $action_err == '' and $time_err == '' and $every_err == '' and $turn_err == ''){

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

    }else{
        $response["success"] = 0;
        $response["message"] = "Invalid data, fuck off"; 
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