<?php
require_once __DIR__ . '/config.php';
require_once __DIR__ . '/db.php';

if ($tg_bot_token === 'ВАШ_ТОКЕН_БОТА' || empty($tg_bot_token)) {
    echo "Bot token not configured. Please edit config.php.\n";
    // We sleep so the container doesn't restart furiously
    while(true) { sleep(60); }
}

// Создаем таблицу для подписчиков, если ее нет
$pdo->exec("CREATE TABLE IF NOT EXISTS tg_subscribers (
    chat_id BIGINT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)");

$last_update_id = 0;
echo "Telegram Bot started polling...\n";

while (true) {
    // Используем Long Polling
    $url = "https://api.telegram.org/bot{$tg_bot_token}/getUpdates?offset=" . ($last_update_id + 1) . "&timeout=30";
    
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 35);
    $response = curl_exec($ch);
    curl_close($ch);

    if ($response) {
        $updates = json_decode($response, true);
        if (!empty($updates['result'])) {
            foreach ($updates['result'] as $update) {
                $last_update_id = $update['update_id'];
                
                if (isset($update['message']['text']) && isset($update['message']['chat']['id'])) {
                    $chat_id = $update['message']['chat']['id'];
                    $text = trim($update['message']['text']);
                    
                    if ($text === '/start') {
                        // Добавляем подписчика в базу
                        $stmt = $pdo->prepare("INSERT IGNORE INTO tg_subscribers (chat_id) VALUES (?)");
                        $stmt->execute([$chat_id]);
                        
                        // Отправляем приветственное сообщение
                        $msg = "✅ Успешно! Теперь вы будете получать уведомления о новых заявках Kapelnica-Med.";
                        file_get_contents("https://api.telegram.org/bot{$tg_bot_token}/sendMessage?chat_id={$chat_id}&text=" . urlencode($msg));
                        echo "New subscriber: {$chat_id}\n";
                    }
                }
            }
        }
    }
    sleep(1);
}
