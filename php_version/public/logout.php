<?php
require_once '../includes/session.php';

session_destroy();
setFlash('info', 'Logged out successfully.');
header('Location: login.php');
exit();
?>
