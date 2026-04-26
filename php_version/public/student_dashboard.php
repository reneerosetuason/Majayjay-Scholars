<?php
require_once '../config/database.php';
require_once '../includes/session.php';

requireStudent();

$conn = getDBConnection();

// Get student info
$stmt = $conn->prepare("SELECT first_name FROM users WHERE user_id = ?");
$stmt->bind_param("i", $_SESSION['user_id']);
$stmt->execute();
$result = $stmt->get_result();
$student = $result->fetch_assoc();
$first_name = $student['first_name'] ?? $_SESSION['email'];
$stmt->close();

// Check if renewals are open
$stmt = $conn->prepare("SELECT is_open FROM renewal_settings WHERE id = 1");
$stmt->execute();
$result = $stmt->get_result();
$renewal_setting = $result->fetch_assoc();
$renewal_open = $renewal_setting ? (bool)$renewal_setting['is_open'] : false;
$stmt->close();

// Check if student has approved application
$stmt = $conn->prepare("SELECT status FROM application WHERE user_id = ? ORDER BY submission_date DESC LIMIT 1");
$stmt->bind_param("i", $_SESSION['user_id']);
$stmt->execute();
$result = $stmt->get_result();
$app_status = $result->fetch_assoc();
$has_approved_application = $app_status && $app_status['status'] === 'approved';
$stmt->close();

closeDBConnection($conn);
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: #f7fafc;
            font-family: 'Inter', sans-serif;
            color: #2d3748;
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        .header {
            background: white;
            padding: 40px;
            border-radius: 24px;
            margin-bottom: 30px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        }
        .header h2 {
            font-size: 2rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .scholarship-section {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
        }
        .scholarship-card {
            background: white;
            padding: 40px;
            border-radius: 24px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            text-align: center;
            transition: 0.3s;
        }
        .scholarship-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 8px 30px rgba(102, 126, 234, 0.15);
        }
        .icon {
            font-size: 64px;
            margin-bottom: 24px;
        }
        h3 {
            color: #2d3748;
            font-size: 1.5rem;
            margin-bottom: 12px;
        }
        p {
            color: #718096;
            margin-bottom: 28px;
        }
        .action-btn {
            display: inline-block;
            padding: 14px 32px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 12px;
            font-weight: 600;
            transition: 0.3s;
        }
        .action-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
        }
        .action-btn:disabled {
            background: #cbd5e0;
            cursor: not-allowed;
            box-shadow: none;
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
            font-weight: 600;
        }
        .alert {
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .alert-success {
            background: #d4edda;
            color: #155724;
        }
        .alert-error {
            background: #fee;
            color: #c62828;
        }
    </style>
</head>
<body>
    <a href="logout.php" class="logout-btn">Logout</a>
    
    <div class="container">
        <div class="header">
            <h2>Welcome, <?php echo htmlspecialchars($first_name); ?> 🎓</h2>
        </div>
        
        <?php
        $flash = getFlash();
        if ($flash):
        ?>
        <div class="alert alert-<?php echo $flash['type']; ?>">
            <?php echo htmlspecialchars($flash['message']); ?>
        </div>
        <?php endif; ?>
        
        <div class="scholarship-section">
            <!-- Apply Card -->
            <div class="scholarship-card">
                <div class="icon">📝</div>
                <h3>Apply Now</h3>
                <p>Gusto mo ba maging scholar ni mayor? Apply Now!</p>
                <a href="apply.php" class="action-btn">Apply for Scholarship</a>
            </div>
            
            <!-- Renew Card -->
            <div class="scholarship-card">
                <div class="icon">🔄</div>
                <h3>Renew</h3>
                <?php if (!$has_approved_application): ?>
                    <p style="color: #f56565; font-weight: 600;">⚠️ You must have an approved application first</p>
                    <button class="action-btn" disabled>Not Eligible</button>
                <?php elseif (!$renewal_open): ?>
                    <p style="color: #f56565; font-weight: 600;">⚠️ Renewals are currently closed</p>
                    <button class="action-btn" disabled>Closed</button>
                <?php else: ?>
                    <p>Renew your scholarship application</p>
                    <a href="renew.php" class="action-btn">Renew Now</a>
                <?php endif; ?>
            </div>
            
            <!-- My Applications Card -->
            <div class="scholarship-card">
                <div class="icon">📋</div>
                <h3>My Applications</h3>
                <p>View your application status and history</p>
                <a href="my_applications.php" class="action-btn">View Applications</a>
            </div>
        </div>
    </div>
</body>
</html>
