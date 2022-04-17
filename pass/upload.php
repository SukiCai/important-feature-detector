<?php
$target_dir = "uploads/";
$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);
$uploadOk = 1;
$imageFileType = strtolower(pathinfo($target_file,PATHINFO_EXTENSION));
$csvMimes = array('text/x-comma-separated-values', 'text/comma-separated-values', 'application/octet-stream', 'application/vnd.ms-excel', 'application/x-csv', 'text/x-csv', 'text/csv', 'application/csv', 'application/excel', 'application/vnd.msexcel', 'text/plain');

// Check if has file selected
if (!isset($_FILES['fileToUpload']) || $_FILES['fileToUpload']['error'] == UPLOAD_ERR_NO_FILE) {
  echo "No file selected.";
  $uploadOk = 0;
} else if (isset($_FILES['fileToUpload']['tmp_name'])) {
  $finfo = finfo_open(FILEINFO_MIME_TYPE);
  $mime = finfo_file($finfo, $_FILES['fileToUpload']['tmp_name']);
  if (in_array($mime, $csvMimes) === false) {
    echo 'It is not a CSV.';
    $uploadOk = 0;
  }
  finfo_close($finfo);
  if (file_exists($target_file)) {
  echo "Sorry, file already exists.";
  $uploadOk = 0;
  }
}
// Check file size
if ($_FILES["fileToUpload"]["size"] >= 3000000) {
  echo "Sorry, your file is too large.";
  $uploadOk = 0;
}
// Check if $uploadOk is set to 0 by an error
if ($uploadOk == 0) {
  echo "Sorry, your file was not uploaded.";
// if everything is ok, try to upload file
} else {
  $temp = explode(".", $_FILES["fileToUpload"]["name"]);
  $newfilename = "analyze_target". '.' . end($temp);
  if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_dir . $newfilename)) {
    echo "The file ". htmlspecialchars( basename( $_FILES["fileToUpload"]["name"])). " has been uploaded.";
  } else {
    echo "Sorry, there was an error uploading your file.";
  }
}
?>