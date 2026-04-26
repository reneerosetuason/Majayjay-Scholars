<?php
require_once '../config/database.php';
require_once '../includes/session.php';

requireMayor();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $conn = getDBConnection();
    
    // Check if renewal_settings exists
    $stmt = $conn->prepare("SELECT is_open FROM renewal_settings WHERE id = 1");
    $stmt->execute();
    $result = $stmt->get_result();
    $setting = $result->fetch_assoc();
    $stmt->close();
    
    if ($setting) {
        // Toggle the current state
        $new_state = !$setting['is_open'];
        $stmt = $conn->prepare("UPDATE renewal_settings SET is_open = ? WHERE id = 1");
        $stmt->bind_param("i", $new_state);
        $stmt->execute();
        $stmt->close();
    } else {
        // Create initial record
        $stmt = $conn->prepare("INSERT INTO renewal_settings (id, is_open) VALUES (1, TRUE)");
        $stmt->execute();
        $stmt->close();
    }
    
    closeDBConnection($conn);
    setFlash('success', 'Renewal status updated successfully!');
}

header('Location: mayor_dashboard.php');
exit();
?>
