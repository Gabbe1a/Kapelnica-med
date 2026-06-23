<?php
header('Content-Type: application/json');
require_once 'db.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Метод не разрешен']);
    exit;
}

$name = trim($_POST['name'] ?? '');
$email = trim($_POST['email'] ?? '');
$phone = trim($_POST['phone'] ?? '');

// 1. Валидация
if (empty($name) || empty($email) || empty($phone)) {
    echo json_encode(['success' => false, 'message' => 'Пожалуйста, заполните все поля']);
    exit;
}

if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    echo json_encode(['success' => false, 'message' => 'Пожалуйста, введите корректный email']);
    exit;
}

$phone_cleaned = preg_replace('/[^0-9+]/', '', $phone);
if (strlen($phone_cleaned) < 10) {
    echo json_encode(['success' => false, 'message' => 'Пожалуйста, введите корректный номер телефона']);
    exit;
}

try {
    // 2. Проверка на спам: 5 минут
    $stmt = $pdo->prepare("
        SELECT id FROM requests 
        WHERE (name = :name OR email = :email OR phone = :phone) 
        AND created_at > (NOW() - INTERVAL 5 MINUTE)
    ");
    $stmt->execute(['name' => $name, 'email' => $email, 'phone' => $phone]);
    
    if ($stmt->fetch()) {
        echo json_encode(['success' => false, 'message' => 'Вы уже оставляли заявку недавно. Попробуйте через 5 минут.']);
        exit;
    }

    // Вставка в БД с защитой от SQL-инъекций (через PDO prepare)
    $stmt = $pdo->prepare("INSERT INTO requests (name, email, phone) VALUES (:name, :email, :phone)");
    $stmt->execute(['name' => $name, 'email' => $email, 'phone' => $phone]);

    echo json_encode(['success' => true, 'message' => 'Заявка успешно отправлена!']);
} catch (PDOException $e) {
    echo json_encode(['success' => false, 'message' => 'Произошла ошибка базы данных. Попробуйте позже.']);
}
?>
