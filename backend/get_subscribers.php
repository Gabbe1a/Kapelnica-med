<?php
header('Content-Type: text/html; charset=utf-8');
require_once 'db.php';

$stmt = $pdo->query("SELECT * FROM tg_subscribers ORDER BY created_at DESC");
$subscribers = $stmt->fetchAll();

echo "<h2>Список подписчиков Telegram-бота</h2>";
echo "<table border='1' cellpadding='10' style='border-collapse: collapse; font-family: sans-serif;'>";
echo "<tr style='background: #f4f4f4;'><th>Chat ID</th><th>Дата подписки</th></tr>";

foreach ($subscribers as $s) {
    echo "<tr>";
    echo "<td>" . htmlspecialchars($s['chat_id']) . "</td>";
    echo "<td>{$s['created_at']}</td>";
    echo "</tr>";
}
echo "</table>";
?>
