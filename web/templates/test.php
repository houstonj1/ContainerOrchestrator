<?php
  $output=shell_exec("sudo python /home/jahousto/ContainerOrchestrator/bin/list_images.py");
  $result = json_decode($output,true);
  foreach($result as $key => $value) {
    echo "$key   :   $value</br>";
  }
?>
