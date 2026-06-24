<?php
require_once __DIR__ . '/config.php';
require_once __DIR__ . '/db.php';

if ($tg_bot_token === 'ВАШ_ТОКЕН_БОТА' || empty($tg_bot_token)) {
    echo "Bot token not configured. Please edit config.php.\n";
    while(true) { sleep(60); }
}

// 1. Создаем таблицу для подписчиков
$pdo->exec("CREATE TABLE IF NOT EXISTS tg_subscribers (
    chat_id BIGINT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)");

// 2. Обновляем таблицу заявок для поддержки статусов и комментариев
try {
    $pdo->exec("ALTER TABLE requests ADD COLUMN status VARCHAR(20) DEFAULT 'new'");
} catch (Exception $e) {}
try {
    $pdo->exec("ALTER TABLE requests ADD COLUMN comment TEXT DEFAULT NULL");
} catch (Exception $e) {}

$last_update_id = 0;
echo "Telegram CRM Bot started polling...\n";

function tgRequest($method, $data) {
    global $tg_bot_token;
    $url = "https://api.telegram.org/bot{$tg_bot_token}/{$method}";
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, is_array($data) ? json_encode($data) : $data);
    curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 5);
    $res = curl_exec($ch);
    curl_close($ch);
    return json_decode($res, true);
}

function renderMessageText($req) {
    $status_emoji = $req['status'] === 'processed' ? '✅' : '🚨';
    $status_text = $req['status'] === 'processed' ? 'ОБРАБОТАНА' : 'Новая';
    
    $text = "{$status_emoji} <b>Заявка #{$req['id']}!</b>\n\n"
          . "👤 <b>Имя:</b> " . htmlspecialchars($req['name']) . "\n"
          . "📞 <b>Телефон:</b> <code>" . htmlspecialchars($req['phone']) . "</code>\n"
          . "✉️ <b>Email:</b> " . htmlspecialchars($req['email']) . "\n\n"
          . "ℹ️ <i>Статус: {$status_text}</i>";
          
    if (!empty($req['comment'])) {
        $text .= "\n💬 <b>Комментарий:</b> " . htmlspecialchars($req['comment']);
    }
    return $text;
}

while (true) {
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
                
                // Обработка текстовых сообщений
                if (isset($update['message']['text']) && isset($update['message']['chat']['id'])) {
                    $chat_id = $update['message']['chat']['id'];
                    $text = trim($update['message']['text']);
                    
                    // Главное меню
                    $main_keyboard = [
                        'keyboard' => [
                            [['text' => '🟢 Активные заявки'], ['text' => '📋 Все заявки']],
                            [['text' => '✅ Обработанные'], ['text' => '💬 С комментариями']]
                        ],
                        'resize_keyboard' => true,
                        'is_persistent' => true
                    ];

                    if ($text === '/start') {
                        $stmt = $pdo->prepare("INSERT IGNORE INTO tg_subscribers (chat_id) VALUES (?)");
                        $stmt->execute([$chat_id]);
                        
                        tgRequest('sendMessage', [
                            'chat_id' => $chat_id,
                            'text' => "✅ CRM-режим активирован.\nВоспользуйтесь меню ниже для управления заявками:",
                            'reply_markup' => $main_keyboard
                        ]);
                    } elseif (preg_match('/^\/manage_(\d+)$/', $text, $matches)) {
                        // Обработка команды /manage_ID
                        $req_id = intval($matches[1]);
                        $stmt = $pdo->prepare("SELECT * FROM requests WHERE id = ?");
                        $stmt->execute([$req_id]);
                        $req = $stmt->fetch(PDO::FETCH_ASSOC);
                        
                        if ($req) {
                            $markup = [ 'inline_keyboard' => [] ];
                            if ($req['status'] === 'new') {
                                $markup['inline_keyboard'][] = [['text' => '✅ Отметить обработанной', 'callback_data' => "close_{$req['id']}"]];
                            }
                            $markup['inline_keyboard'][] = [['text' => '💬 Оставить комментарий', 'callback_data' => "comment_{$req['id']}"]];

                            tgRequest('sendMessage', [
                                'chat_id' => $chat_id,
                                'text' => renderMessageText($req),
                                'parse_mode' => 'HTML',
                                'reply_markup' => $markup
                            ]);
                        } else {
                            tgRequest('sendMessage', ['chat_id' => $chat_id, 'text' => "Заявка не найдена."]);
                        }
                    }
                    
                    // Обработка кнопок меню
                    $query = null;
                    $header_msg = "";
                    if ($text === '🟢 Активные заявки') {
                        $query = "SELECT * FROM requests WHERE status='new' ORDER BY id DESC LIMIT 15";
                        $header_msg = "🟢 <b>Последние 15 активных заявок:</b>";
                    } elseif ($text === '📋 Все заявки') {
                        $query = "SELECT * FROM requests ORDER BY id DESC LIMIT 15";
                        $header_msg = "📋 <b>Последние 15 заявок:</b>";
                    } elseif ($text === '✅ Обработанные') {
                        $query = "SELECT * FROM requests WHERE status='processed' ORDER BY id DESC LIMIT 15";
                        $header_msg = "✅ <b>Последние 15 обработанных заявок:</b>";
                    } elseif ($text === '💬 С комментариями') {
                        $query = "SELECT * FROM requests WHERE comment IS NOT NULL AND comment != '' ORDER BY id DESC LIMIT 15";
                        $header_msg = "💬 <b>Последние 15 заявок с комментариями:</b>";
                    }

                    if ($query) {
                        $reqs = $pdo->query($query)->fetchAll(PDO::FETCH_ASSOC);
                        if (empty($reqs)) {
                            tgRequest('sendMessage', [
                                'chat_id' => $chat_id,
                                'text' => "🤷‍♂️ По этому запросу заявок не найдено.",
                                'reply_markup' => $main_keyboard
                            ]);
                        } else {
                            $msg = $header_msg . "\n\n";
                            foreach ($reqs as $req) {
                                $status_emoji = $req['status'] === 'new' ? '🔴' : '✅';
                                $comment = empty($req['comment']) ? '<i>нет</i>' : htmlspecialchars($req['comment']);
                                $phone = htmlspecialchars($req['phone']);
                                $name = htmlspecialchars($req['name']);
                                
                                $msg .= "{$status_emoji} <b>#{$req['id']}</b> | {$name} | <code>{$phone}</code>\n";
                                $msg .= "📝 Коммент: {$comment}\n";
                                $msg .= "👉 Управление: /manage_{$req['id']}\n\n";
                            }
                            
                            tgRequest('sendMessage', [
                                'chat_id' => $chat_id, 
                                'text' => $msg, 
                                'parse_mode' => 'HTML', 
                                'reply_markup' => $main_keyboard
                            ]);
                        }
                    }
                    
                    // Обработка ответа (ForceReply) для комментария
                    if (isset($update['message']['reply_to_message']['text'])) {
                        $reply_text = $update['message']['reply_to_message']['text'];
                        if (preg_match('/Введите комментарий для заявки #(\d+):/', $reply_text, $matches)) {
                            $req_id = intval($matches[1]);
                            $comment = $text;
                            
                            $pdo->prepare("UPDATE requests SET comment = ? WHERE id = ?")->execute([$comment, $req_id]);
                            
                            // Получаем обновленную заявку и отправляем подтверждение
                            $req = $pdo->query("SELECT * FROM requests WHERE id = $req_id")->fetch(PDO::FETCH_ASSOC);
                            if ($req) {
                                $markup = [ 'inline_keyboard' => [] ];
                                if ($req['status'] === 'new') {
                                    $markup['inline_keyboard'][] = [['text' => '✅ Отметить обработанной', 'callback_data' => "close_{$req['id']}"]];
                                }
                                $markup['inline_keyboard'][] = [['text' => '💬 Изменить комментарий', 'callback_data' => "comment_{$req['id']}"]];

                                tgRequest('sendMessage', [
                                    'chat_id' => $chat_id,
                                    'text' => "✅ Комментарий к заявке #{$req_id} сохранен!\n\n" . renderMessageText($req),
                                    'parse_mode' => 'HTML',
                                    'reply_markup' => $markup
                                ]);
                            }
                        }
                    }
                }
                
                // Обработка нажатий на кнопки
                if (isset($update['callback_query'])) {
                    $cq = $update['callback_query'];
                    $cq_id = $cq['id'];
                    $chat_id = $cq['message']['chat']['id'];
                    $message_id = $cq['message']['message_id'];
                    $data = $cq['data'];

                    if (strpos($data, 'close_') === 0) {
                        $req_id = intval(substr($data, 6));
                        $pdo->exec("UPDATE requests SET status='processed' WHERE id=$req_id");
                        
                        // Получаем актуальные данные заявки
                        $req = $pdo->query("SELECT * FROM requests WHERE id = $req_id")->fetch(PDO::FETCH_ASSOC);
                        
                        // Обновляем сообщение (убираем кнопку "Закрыть", оставляем только комментарий)
                        tgRequest('editMessageText', [
                            'chat_id' => $chat_id,
                            'message_id' => $message_id,
                            'text' => renderMessageText($req),
                            'parse_mode' => 'HTML',
                            'reply_markup' => [
                                'inline_keyboard' => [
                                    [ ['text' => '💬 Оставить комментарий', 'callback_data' => "comment_{$req_id}"] ]
                                ]
                            ]
                        ]);
                        
                        tgRequest('answerCallbackQuery', ['callback_query_id' => $cq_id, 'text' => 'Заявка обработана!']);
                    }
                    
                    if (strpos($data, 'comment_') === 0) {
                        $req_id = intval(substr($data, 8));
                        tgRequest('sendMessage', [
                            'chat_id' => $chat_id,
                            'text' => "Введите комментарий для заявки #{$req_id}:",
                            'reply_markup' => [
                                'force_reply' => true,
                                'selective' => true
                            ]
                        ]);
                        tgRequest('answerCallbackQuery', ['callback_query_id' => $cq_id]);
                    }
                }
            }
        }
    }
    sleep(1);
}
