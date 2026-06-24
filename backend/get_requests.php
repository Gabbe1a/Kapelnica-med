<?php
header('Content-Type: text/html; charset=utf-8');
require_once 'db.php';

$stmt = $pdo->query("SELECT * FROM requests ORDER BY id DESC");
$requests = $stmt->fetchAll();

echo "<h2>Список заявок</h2>";
echo "<table border='1' cellpadding='10' style='border-collapse: collapse; font-family: sans-serif;'>";
echo "<tr style='background: #f4f4f4;'><th>ID</th><th>Имя</th><th>Email</th><th>Телефон</th><th>Дата</th></tr>";

foreach ($requests as $r) {
    echo "<tr>";
    echo "<td>{$r['id']}</td>";
    echo "<td>" . htmlspecialchars($r['name']) . "</td>";
    echo "<td>" . htmlspecialchars($r['email']) . "</td>";
    echo "<td>" . htmlspecialchars($r['phone']) . "</td>";
    echo "<td>{$r['created_at']}</td>";
    echo "</tr>";
}
echo "</table>";
?>
