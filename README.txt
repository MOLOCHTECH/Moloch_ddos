# 💀 MOLOCH: The Proxy Reaper (v2.0 Socket Edition)

![License: MIT](https://img.shields.io/badge/License-MIT-red.svg)
![Python: 3.x](https://img.shields.io/badge/Python-3.x-blue.svg)

**MOLOCH** — это высокопроизводительный инструмент для стресс-тестирования сетей, переписанный на низкоуровневых сокетах для максимальной скорости. Оптимизирован для работы через SOCKS5 прокси-серверы, что позволяет проводить аудит безопасности, не раскрывая реальный IP-адрес оператора.

---

## 🔥 Особенности (Features)
* **Socket-Level Attack**: Прямая работа с TCP-стеком, что в разы быстрее обычных HTTP-библиотек.
* **Proxy Rotation**: Поддержка SOCKS5 с автоматическим выбором случайного узла из `proxies.txt`.
* **MateBook Optimized**: Код стабильно держит до 5000+ потоков на современных многоядерных процессорах.
* **Live Monitor**: Интерактивная панель управления на базе `Rich` с отображением RPS (запросов в секунду) и статусов сервера.
* **SSL/TLS Support**: Поддержка атак на 443 порт (HTTPS) через защищенные сокеты.

---

## 🛠 Установка и запуск (Installation)

### 1. Клонирование и подготовка
Убедитесь, что у вас установлен Python 3.8+ и менеджер пакетов pip.

```bash
git clone [https://github.com/ВАШ_НИК/moloch-reaper.git](https://github.com/ВАШ_НИК/moloch-reaper.git)
cd moloch-reaper
