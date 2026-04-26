<?php
// Start session if not already started
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

// Check if user is logged in
function isLoggedIn() {
    return isset($_SESSION['user_id']);
}

// Check user type
function getUserType() {
    return isset($_SESSION['user_type']) ? strtolower($_SESSION['user_type']) : '';
}

// Check if user is admin
function isAdmin() {
    return getUserType() === 'admin';
}

// Check if user is mayor
function isMayor() {
    return getUserType() === 'mayor';
}

// Check if user is student
function isStudent() {
    return getUserType() === 'student';
}

// Redirect if not logged in
function requireLogin() {
    if (!isLoggedIn()) {
        header('Location: /php_version/public/login.php');
        exit();
    }
}

// Redirect if not admin
function requireAdmin() {
    requireLogin();
    if (!isAdmin()) {
        $_SESSION['error'] = 'Access denied!';
        header('Location: /php_version/public/login.php');
        exit();
    }
}

// Redirect if not mayor
function requireMayor() {
    requireLogin();
    if (!isMayor()) {
        $_SESSION['error'] = 'Access denied!';
        header('Location: /php_version/public/login.php');
        exit();
    }
}

// Redirect if not student
function requireStudent() {
    requireLogin();
    if (!isStudent()) {
        $_SESSION['error'] = 'Access denied!';
        header('Location: /php_version/public/login.php');
        exit();
    }
}

// Set flash message
function setFlash($type, $message) {
    $_SESSION['flash_type'] = $type;
    $_SESSION['flash_message'] = $message;
}

// Get and clear flash message
function getFlash() {
    if (isset($_SESSION['flash_message'])) {
        $type = $_SESSION['flash_type'] ?? 'info';
        $message = $_SESSION['flash_message'];
        unset($_SESSION['flash_type']);
        unset($_SESSION['flash_message']);
        return ['type' => $type, 'message' => $message];
    }
    return null;
}

// Logout user
function logout() {
    session_destroy();
    header('Location: /php_version/public/login.php');
    exit();
}
?>
