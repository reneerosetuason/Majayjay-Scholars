<?php
require_once '../includes/session.php';

if (isLoggedIn()) {
    $userType = getUserType();
    if ($userType === 'admin') {
        header('Location: admin_dashboard.php');
    } elseif ($userType === 'mayor') {
        header('Location: mayor_dashboard.php');
    } else {
        header('Location: student_dashboard.php');
    }
} else {
    header('Location: login.php');
}
exit();
?>
