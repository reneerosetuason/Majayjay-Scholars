<?php
require_once '../config/database.php';
require_once '../includes/session.php';

requireMayor();

$conn = getDBConnection();

// Get mayor's name
$stmt = $conn->prepare("SELECT first_name, last_name FROM users WHERE user_id = ?");
$stmt->bind_param("i", $_SESSION['user_id']);
$stmt->execute();
$result = $stmt->get_result();
$mayor = $result->fetch_assoc();
$name = $mayor ? $mayor['first_name'] . ' ' . $mayor['last_name'] : $_SESSION['email'];
$stmt->close();

// Get all active applications
$stmt = $conn->prepare("SELECT scholarship_type, status FROM application WHERE archived = FALSE OR archived IS NULL");
$stmt->execute();
$result = $stmt->get_result();
$applications = $result->fetch_all(MYSQLI_ASSOC);
$stmt->close();

// Get all active renewals
$stmt = $conn->prepare("SELECT status FROM renew WHERE archived = FALSE OR archived IS NULL");
$stmt->execute();
$result = $stmt->get_result();
$renewals = $result->fetch_all(MYSQLI_ASSOC);
$stmt->close();

// Get renewal status
$stmt = $conn->prepare("SELECT is_open FROM renewal_settings WHERE id = 1");
$stmt->execute();
$result = $stmt->get_result();
$renewal_setting = $result->fetch_assoc();
$renewal_open = $renewal_setting ? (bool)$renewal_setting['is_open'] : false;
$stmt->close();

// Filter new applications
$new_apps = array_filter($applications, function($app) {
    return $app['scholarship_type'] === 'new';
});

// Count by status
function countByStatus($items, $status) {
    return count(array_filter($items, function($item) use ($status) {
        return strtolower($item['status']) === strtolower($status);
    }));
}

closeDBConnection($conn);
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mayor Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: #f7fafc;
            font-family: 'Inter', sans-serif;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 40px;
        }
        .header-card {
            background: white;
            padding: 40px;
            border-radius: 24px;
            margin-bottom: 30px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        }
        .header-card h2 {
            font-size: 32px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 25px;
            margin-bottom: 40px;
        }
        .stat-card {
            background: white;
            padding: 24px;
            border-radius: 16px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            transition: 0.3s;
        }
        .stat-card:hover {
            transform: translateY(-8px);
        }
        .stat-card .number {
            font-size: 36px;
            font-weight: 700;
            margin-bottom: 8px;
        }
        .stat-card .label {
            color: #666;
            font-size: 13px;
            text-transform: uppercase;
        }
        .stat-card.total .number { color: #667eea; }
        .stat-card.approved .number { color: #48bb78; }
        .stat-card.pending .number { color: #ffa500; }
        .stat-card.rejected .number { color: #f56565; }
        .section-title {
            font-size: 22px;
            font-weight: 700;
            margin: 40px 0 20px;
        }
        .renewal-toggle-btn {
            padding: 12px 24px;
            color: white;
            border: none;
            border-radius: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: 0.3s;
        }
        .btn-close {
            background: linear-gradient(135deg, #f56565 0%, #e53e3e 100%);
        }
        .btn-open {
            background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        }
        .nav-links {
            margin-top: 20px;
        }
        .nav-links a {
            display: inline-block;
            padding: 10px 20px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            margin-right: 10px;
        }
        .logout-btn {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 10px 20px;
            background: #f56565;
            color: white;
            text-decoration: none;
            border-radius: 8px;
        }
    </style>
</head>
<body>
    <a href="logout.php" class="logout-btn">Logout</a>
    
    <div class="container">
        <div class="header-card">
            <h2>Welcome, <?php echo htmlspecialchars($name); ?>! 🎓</h2>
            <p>Overview of scholarship applications and renewals</p>
        </div>
        
        <div class="section-title">📝 New Scholarship Applications</div>
        
        <div class="stats-grid">
            <div class="stat-card total">
                <div class="number"><?php echo count($new_apps); ?></div>
                <div class="label">Total New</div>
            </div>
            <div class="stat-card approved">
                <div class="number"><?php echo countByStatus($new_apps, 'approved'); ?></div>
                <div class="label">Approved</div>
            </div>
            <div class="stat-card pending">
                <div class="number"><?php echo countByStatus($new_apps, 'pending'); ?></div>
                <div class="label">Pending</div>
            </div>
            <div class="stat-card rejected">
                <div class="number"><?php echo countByStatus($new_apps, 'rejected'); ?></div>
                <div class="label">Rejected</div>
            </div>
        </div>
        
        <div class="section-title">🔄 Scholarship Renewals</div>
        
        <form method="POST" action="toggle_renewal.php" style="margin-bottom: 20px;">
            <button type="submit" class="renewal-toggle-btn <?php echo $renewal_open ? 'btn-close' : 'btn-open'; ?>">
                <?php echo $renewal_open ? '🔒 Close Renewals' : '🔓 Open Renewals'; ?>
            </button>
            <span style="margin-left: 15px; color: #718096;">
                Status: <strong style="color: <?php echo $renewal_open ? '#48bb78' : '#f56565'; ?>">
                    <?php echo $renewal_open ? 'Open' : 'Closed'; ?>
                </strong>
            </span>
        </form>
        
        <div class="stats-grid">
            <div class="stat-card total">
                <div class="number"><?php echo count($renewals); ?></div>
                <div class="label">Total Renewals</div>
            </div>
            <div class="stat-card approved">
                <div class="number"><?php echo countByStatus($renewals, 'Approved'); ?></div>
                <div class="label">Approved</div>
            </div>
            <div class="stat-card pending">
                <div class="number"><?php echo countByStatus($renewals, 'Pending'); ?></div>
                <div class="label">Pending</div>
            </div>
            <div class="stat-card rejected">
                <div class="number"><?php echo countByStatus($renewals, 'Rejected'); ?></div>
                <div class="label">Rejected</div>
            </div>
        </div>
        
        <div class="nav-links">
            <a href="mayor_records.php">📁 View Records</a>
            <a href="mayor_scholars.php">🎓 View Scholars</a>
        </div>
    </div>
</body>
</html>
