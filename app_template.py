from flask import Flask, request, session
import random
import time

import base64

def check_auth(username, password):
    return password == "cuby2026"

def authenticate():
    return "Для доступа к теме 'Мои кейсы' введите пароль", 401, {"WWW-Authenticate": 'Basic realm="My Cases"'}


app = Flask(__name__)
app.secret_key = 'devops-secret-key-2026'

# ============================================
# БАЗА ВОПРОСОВ (248)
# ============================================

questions = [
    {"id": 1, "topic": "Linux", "question": "Как посмотреть логи systemd-сервиса в реальном времени?", "options": ["systemctl logs -f", "journalctl -u <service> -f", "tail -f /var/log/syslog", "dmesg -w"], "correct": "journalctl -u <service> -f"},
    {"id": 2, "topic": "Linux", "question": "Как ограничить CPU для systemd-сервиса?", "options": ["CPULimit=80", "CPUQuota=80%", "LimitCPU=80", "CPU=80%"], "correct": "CPUQuota=80%"},
    {"id": 3, "topic": "Linux", "question": "Как перезагрузить конфигурацию systemd после изменения файла?", "options": ["systemctl restart", "systemctl reload", "systemctl daemon-reload", "systemctl update"], "correct": "systemctl daemon-reload"},
    {"id": 4, "topic": "Linux", "question": "Как посмотреть список всех активных сервисов systemd?", "options": ["systemctl list", "systemctl status", "systemctl list-units --type=service", "systemctl show"], "correct": "systemctl list-units --type=service"},
    {"id": 5, "topic": "Linux", "question": "Какая команда показывает использование диска в человеко-читаемом формате?", "options": ["du -h", "df -h", "ls -lh", "fdisk -l"], "correct": "df -h"},
    {"id": 6, "topic": "Linux", "question": "Как посмотреть, какие порты слушает сервер?", "options": ["netstat -tlnp", "iptables -L", "ss -s", "tcpdump"], "correct": "netstat -tlnp"},
    {"id": 7, "topic": "Linux", "question": "Как найти процесс, который ест 100% CPU?", "options": ["htop (нажать P)", "ls -l", "ps aux", "kill -9"], "correct": "htop (нажать P)"},
    {"id": 8, "topic": "Linux", "question": "Что делает команда 'chmod +x script.sh'?", "options": ["Удаляет файл", "Делает файл исполняемым", "Копирует файл", "Переименовывает файл"], "correct": "Делает файл исполняемым"},
    {"id": 9, "topic": "Linux", "question": "Как посмотреть размер папки?", "options": ["ls -la", "du -sh", "df -h", "find . -size"], "correct": "du -sh"},
    {"id": 10, "topic": "Linux", "question": "Как посмотреть историю команд в Bash?", "options": ["history", "cat ~/.bash_history", "Оба варианта", "Ни один"], "correct": "Оба варианта"},
    {"id": 11, "topic": "Linux", "question": "Что такое inode?", "options": ["Структура с метаданными файла", "IP адрес", "Сетевое соединение", "Тип файловой системы"], "correct": "Структура с метаданными файла"},
    {"id": 12, "topic": "Linux", "question": "Как применить права 755 к папке рекурсивно?", "options": ["chmod 755 *", "chmod -R 755 ./", "chmod 755 -R", "chmod 755"], "correct": "chmod -R 755 ./"},
    {"id": 13, "topic": "Linux", "question": "Что такое cron?", "options": ["Сервис для мониторинга", "Планировщик задач", "Система логирования", "База данных"], "correct": "Планировщик задач"},
    {"id": 14, "topic": "Linux", "question": "Как посмотреть последние 10 строк лога?", "options": ["head -10 file", "tail -10 file", "less file", "grep -10 file"], "correct": "tail -10 file"},
    {"id": 15, "topic": "Linux", "question": "Что такое swap?", "options": ["Место на диске для расширения RAM", "Тип процессора", "Сетевое соединение", "Системный вызов"], "correct": "Место на диске для расширения RAM"},
    {"id": 16, "topic": "Linux", "question": "Как убить процесс по имени?", "options": ["kill <pid>", "pkill <name>", "killall <name>", "Оба варианта pkill и killall"], "correct": "Оба варианта pkill и killall"},
    {"id": 17, "topic": "Linux", "question": "Что делает команда 'grep -r pattern /path'?", "options": ["Ищет файлы по имени", "Ищет паттерн в файлах рекурсивно", "Удаляет файлы с паттерном", "Заменяет паттерн"], "correct": "Ищет паттерн в файлах рекурсивно"},
    {"id": 18, "topic": "Linux", "question": "Как посмотреть загрузку CPU в реальном времени?", "options": ["top", "htop", "ps aux", "Все варианты"], "correct": "Все варианты"},
    {"id": 19, "topic": "Linux", "question": "Что такое SSH?", "options": ["Протокол удалённого доступа", "Сетевой файрвол", "Система логирования", "База данных"], "correct": "Протокол удалённого доступа"},
    {"id": 20, "topic": "Linux", "question": "Как создать systemd-сервис?", "options": ["Создать файл в /etc/systemd/system/*.service", "Запустить systemd-create", "Использовать init.d", "Все варианты"], "correct": "Создать файл в /etc/systemd/system/*.service"},
    {"id": 21, "topic": "Linux", "question": "Что делает команда 'ps aux'?", "options": ["Показывает все процессы", "Удаляет процессы", "Создает процессы", "Останавливает процессы"], "correct": "Показывает все процессы"},
    {"id": 22, "topic": "Linux", "question": "Как посмотреть версию ядра Linux?", "options": ["uname -r", "kernel --version", "version", "cat /proc/version"], "correct": "uname -r"},
    {"id": 23, "topic": "Linux", "question": "Как посмотреть загрузку памяти?", "options": ["free -h", "top", "htop", "Все варианты"], "correct": "Все варианты"},
    {"id": 24, "topic": "Networks", "question": "Чем отличается TCP от UDP?", "options": ["TCP быстрее, UDP надёжнее", "TCP надежный с подтверждением, UDP быстрый без подтверждения", "TCP для веб-сайтов, UDP для файлов", "Одинаковые"], "correct": "TCP надежный с подтверждением, UDP быстрый без подтверждения"},
    {"id": 25, "topic": "Networks", "question": "Что такое reverse proxy?", "options": ["Сервер для кеширования", "Сервер, перенаправляющий запросы на внутренние сервера", "Балансировщик нагрузки", "Файрвол"], "correct": "Сервер, перенаправляющий запросы на внутренние сервера"},
    {"id": 26, "topic": "Networks", "question": "Какой порт у HTTPS?", "options": ["80", "443", "22", "8080"], "correct": "443"},
    {"id": 27, "topic": "Networks", "question": "Что такое DNS?", "options": ["Превращает домен в IP-адрес", "Система шифрования", "База данных", "Язык программирования"], "correct": "Превращает домен в IP-адрес"},
    {"id": 28, "topic": "Networks", "question": "Что происходит при вводе https://site.com?", "options": ["DNS → TCP → TLS → HTTP", "HTTP → DNS → TCP", "TLS → TCP → DNS", "TCP → HTTP → DNS"], "correct": "DNS → TCP → TLS → HTTP"},
    {"id": 29, "topic": "Networks", "question": "Чем отличается HTTP от HTTPS?", "options": ["HTTPS использует порт 80", "HTTPS шифрует данные (TLS/SSL)", "HTTP быстрее", "Это одно и то же"], "correct": "HTTPS шифрует данные (TLS/SSL)"},
    {"id": 30, "topic": "Networks", "question": "Что такое 502 Bad Gateway?", "options": ["Сервер не найден", "Шлюз не получил ответ от бэкенда", "Нет доступа", "Слишком много запросов"], "correct": "Шлюз не получил ответ от бэкенда"},
    {"id": 31, "topic": "Networks", "question": "Какой порт у SSH?", "options": ["22", "23", "21", "25"], "correct": "22"},
    {"id": 32, "topic": "Networks", "question": "Что такое VLAN?", "options": ["Виртуальная локальная сеть", "Тип маршрутизатора", "Протокол шифрования", "Система мониторинга"], "correct": "Виртуальная локальная сеть"},
    {"id": 33, "topic": "Networks", "question": "Что такое NAT?", "options": ["Преобразование сетевых адресов", "Протокол туннелирования", "Система обнаружения вторжений", "Тип файрвола"], "correct": "Преобразование сетевых адресов"},
    {"id": 34, "topic": "Networks", "question": "Как проверить, открыт ли порт на сервере?", "options": ["telnet host port", "nc -zv host port", "nmap host -p port", "Все варианты"], "correct": "Все варианты"},
    {"id": 35, "topic": "Networks", "question": "Что такое CIDR?", "options": ["Формат записи IP-сетей", "Протокол маршрутизации", "Тип DNS записи", "Система шифрования"], "correct": "Формат записи IP-сетей"},
    {"id": 36, "topic": "Networks", "question": "Какой протокол используется для ping?", "options": ["TCP", "UDP", "ICMP", "ARP"], "correct": "ICMP"},
    {"id": 37, "topic": "Networks", "question": "Что такое SSL/TLS?", "options": ["Протокол шифрования", "Система аутентификации", "Сетевой протокол", "База данных"], "correct": "Протокол шифрования"},
    {"id": 38, "topic": "Networks", "question": "Что такое HTTP/2?", "options": ["Новая версия HTTP с мультиплексированием", "Система кеширования", "Протокол шифрования", "Тип сервера"], "correct": "Новая версия HTTP с мультиплексированием"},
    {"id": 39, "topic": "Networks", "question": "Что такое 'subnet' (подсеть)?", "options": ["Логическое разделение IP-сети", "Тип маршрутизатора", "Сетевой протокол", "Система шифрования"], "correct": "Логическое разделение IP-сети"},
    {"id": 40, "topic": "Networks", "question": "Что такое 'TLS handshake'?", "options": ["Обмен ключами для шифрования", "Тип соединения", "Сетевой протокол", "Аутентификация"], "correct": "Обмен ключами для шифрования"},
    {"id": 41, "topic": "CI/CD", "question": "Что делает GitHub Actions?", "options": ["Хостит код", "Запускает авто-тесты и деплой при push/PR", "Управляет пользователями", "Отслеживает баги"], "correct": "Запускает авто-тесты и деплой при push/PR"},
    {"id": 42, "topic": "CI/CD", "question": "Как настроить Webhook для авто-деплоя?", "options": ["GitHub → Webhook → HTTP-запрос на сервер", "Написать Dockerfile", "Настроить firewall", "Создать базу данных"], "correct": "GitHub → Webhook → HTTP-запрос на сервер"},
    {"id": 43, "topic": "CI/CD", "question": "Чем отличается Git от GitHub?", "options": ["Git — язык программирования", "Git — локальная система контроля версий, GitHub — облачный хостинг", "Git — база данных", "GitHub — IDE"], "correct": "Git — локальная система контроля версий, GitHub — облачный хостинг"},
    {"id": 44, "topic": "CI/CD", "question": "Что такое CI/CD?", "options": ["Непрерывная интеграция и непрерывная доставка", "Система контроля версий", "Язык программирования", "База данных"], "correct": "Непрерывная интеграция и непрерывная доставка"},
    {"id": 45, "topic": "CI/CD", "question": "Что делает команда 'git pull'?", "options": ["Отправляет изменения на сервер", "Загружает изменения с сервера и сливает их", "Создает новую ветку", "Удаляет файлы"], "correct": "Загружает изменения с сервера и сливает их"},
    {"id": 46, "topic": "CI/CD", "question": "Что такое Pull Request?", "options": ["Запрос на вливание кода в основную ветку", "Команда git", "Тип ошибки", "Система мониторинга"], "correct": "Запрос на вливание кода в основную ветку"},
    {"id": 47, "topic": "CI/CD", "question": "Как откатить последний коммит в Git?", "options": ["git reset --hard HEAD~1", "git delete commit", "git remove", "git undo"], "correct": "git reset --hard HEAD~1"},
    {"id": 48, "topic": "CI/CD", "question": "Что такое Jenkins?", "options": ["CI/CD сервер", "База данных", "Файрвол", "IDE"], "correct": "CI/CD сервер"},
    {"id": 49, "topic": "CI/CD", "question": "Чем отличается git merge от git rebase?", "options": ["Merge создает коммит слияния, rebase переписывает историю", "Rebase создает коммит слияния, merge переписывает историю", "Они одинаковые", "Ни один"], "correct": "Merge создает коммит слияния, rebase переписывает историю"},
    {"id": 50, "topic": "CI/CD", "question": "Что такое Git Flow?", "options": ["Модель ветвления", "Команда git", "Система мониторинга", "База данных"], "correct": "Модель ветвления"},
    {"id": 51, "topic": "CI/CD", "question": "Как создать новую ветку в Git?", "options": ["git branch new-branch", "git checkout -b new-branch", "Оба варианта", "Ни один"], "correct": "Оба варианта"},
    {"id": 52, "topic": "CI/CD", "question": "Что делает 'git stash'?", "options": ["Удаляет изменения", "Временно сохраняет изменения", "Коммитит изменения", "Переключает ветку"], "correct": "Временно сохраняет изменения"},
    {"id": 53, "topic": "CI/CD", "question": "Что такое GitLab CI?", "options": ["Встроенная CI/CD система в GitLab", "Язык программирования", "База данных", "IDE"], "correct": "Встроенная CI/CD система в GitLab"},
    {"id": 54, "topic": "CI/CD", "question": "Как посмотреть историю коммитов?", "options": ["git log", "git history", "git show", "git diff"], "correct": "git log"},
    {"id": 55, "topic": "CI/CD", "question": "Что такое 'git cherry-pick'?", "options": ["Применяет указанный коммит в текущую ветку", "Удаляет коммит", "Создает новую ветку", "Объединяет ветки"], "correct": "Применяет указанный коммит в текущую ветку"},
    {"id": 56, "topic": "CI/CD", "question": "Как разрешить конфликт в Git?", "options": ["Вручную отредактировать файлы, затем add + commit", "git merge --abort", "git rebase --skip", "Все варианты"], "correct": "Вручную отредактировать файлы, затем add + commit"},
    {"id": 57, "topic": "CI/CD", "question": "Что такое Git Hooks?", "options": ["Скрипты, запускаемые при определенных событиях", "Система мониторинга", "База данных", "IDE"], "correct": "Скрипты, запускаемые при определенных событиях"},
    {"id": 58, "topic": "CI/CD", "question": "Что делает 'git push --force'?", "options": ["Принудительно отправляет изменения, перезаписывая историю", "Отправляет изменения без проверки", "Удаляет удаленный репозиторий", "Ничего не делает"], "correct": "Принудительно отправляет изменения, перезаписывая историю"},
    {"id": 59, "topic": "CI/CD", "question": "Что такое artifacts в CI/CD?", "options": ["Результаты сборки (файлы, логи, бинарники)", "Система контроля версий", "Сетевой протокол", "Тип сервера"], "correct": "Результаты сборки (файлы, логи, бинарники)"},
    {"id": 60, "topic": "CI/CD", "question": "Что такое pipeline?", "options": ["Последовательность шагов CI/CD", "База данных", "Тип сервера", "Язык программирования"], "correct": "Последовательность шагов CI/CD"},
    {"id": 61, "topic": "CI/CD", "question": "Что такое 'rollback' в CI/CD?", "options": ["Откат к предыдущей версии", "Новый деплой", "Запуск тестов", "Сборка проекта"], "correct": "Откат к предыдущей версии"},
    {"id": 62, "topic": "CI/CD", "question": "Что такое 'cache' в GitHub Actions?", "options": ["Кеширование зависимостей между запусками", "Хранение логов", "Тип экшена", "Система мониторинга"], "correct": "Кеширование зависимостей между запусками"},
    {"id": 63, "topic": "Docker", "question": "Что такое Docker?", "options": ["Виртуальная машина", "Система контейнеризации", "Язык программирования", "База данных"], "correct": "Система контейнеризации"},
    {"id": 64, "topic": "Docker", "question": "Чем отличается контейнер от виртуальной машины?", "options": ["Контейнер легче и использует ядро хоста", "Контейнер тяжелее", "Это одно и то же", "ВМ легче"], "correct": "Контейнер легче и использует ядро хоста"},
    {"id": 65, "topic": "Docker", "question": "Какая команда собирает Docker образ?", "options": ["docker build", "docker create", "docker run", "docker start"], "correct": "docker build"},
    {"id": 66, "topic": "Docker", "question": "Что делает 'docker-compose up -d'?", "options": ["Останавливает все контейнеры", "Запускает все контейнеры из docker-compose.yml в фоне", "Удаляет контейнеры", "Собирает образы"], "correct": "Запускает все контейнеры из docker-compose.yml в фоне"},
    {"id": 67, "topic": "Docker", "question": "Как посмотреть запущенные контейнеры?", "options": ["docker ps", "docker list", "docker show", "docker containers"], "correct": "docker ps"},
    {"id": 68, "topic": "Docker", "question": "Как остановить контейнер?", "options": ["docker stop <id>", "docker kill <id>", "docker rm <id>", "docker pause <id>"], "correct": "docker stop <id>"},
    {"id": 69, "topic": "Docker", "question": "Что такое Docker Compose?", "options": ["Инструмент для многоконтейнерных приложений", "Язык разметки", "База данных", "Веб-сервер"], "correct": "Инструмент для многоконтейнерных приложений"},
    {"id": 70, "topic": "Docker", "question": "Что такое Dockerfile?", "options": ["Файл с инструкциями для сборки образа", "Файл с конфигурацией сети", "Файл с логами", "Файл с данными"], "correct": "Файл с инструкциями для сборки образа"},
    {"id": 71, "topic": "Docker", "question": "Как удалить все неиспользуемые образы и контейнеры?", "options": ["docker system prune -a", "docker rm -a", "docker rmi -a", "docker clean all"], "correct": "docker system prune -a"},
    {"id": 72, "topic": "Docker", "question": "Что такое volume в Docker?", "options": ["Механизм сохранения данных вне контейнера", "Тип сети", "Контейнер с БД", "Образ Docker"], "correct": "Механизм сохранения данных вне контейнера"},
    {"id": 73, "topic": "Docker", "question": "Как посмотреть логи контейнера?", "options": ["docker logs <id>", "docker logs -f <id>", "Оба варианта", "Ни один"], "correct": "Оба варианта"},
    {"id": 74, "topic": "Docker", "question": "Что такое Docker Hub?", "options": ["Регистр хранения Docker образов", "Инструмент оркестрации", "Система мониторинга", "Тип сети"], "correct": "Регистр хранения Docker образов"},
    {"id": 75, "topic": "Docker", "question": "Что делает 'docker exec'?", "options": ["Запускает команду внутри работающего контейнера", "Удаляет контейнер", "Останавливает контейнер", "Создает образ"], "correct": "Запускает команду внутри работающего контейнера"},
    {"id": 76, "topic": "Docker", "question": "Как ограничить ресурсы контейнера?", "options": ["--memory=512m --cpus=0.5", "--limit-mem=512", "--res=512", "Нельзя"], "correct": "--memory=512m --cpus=0.5"},
    {"id": 77, "topic": "Docker", "question": "Что такое Docker Swarm?", "options": ["Инструмент оркестрации контейнеров", "База данных", "Веб-сервер", "Язык программирования"], "correct": "Инструмент оркестрации контейнеров"},
    {"id": 78, "topic": "Docker", "question": "Что такое 'multi-stage build' в Docker?", "options": ["Многоэтапная сборка для уменьшения образа", "Тип контейнера", "Сеть Docker", "Система мониторинга"], "correct": "Многоэтапная сборка для уменьшения образа"},
    {"id": 79, "topic": "Docker", "question": "Что делает 'docker push'?", "options": ["Отправляет образ в реестр", "Загружает образ", "Удаляет образ", "Создает контейнер"], "correct": "Отправляет образ в реестр"},
    {"id": 80, "topic": "Kubernetes", "question": "Что такое Kubernetes?", "options": ["Оркестратор контейнеров", "База данных", "Язык программирования", "CI/CD система"], "correct": "Оркестратор контейнеров"},
    {"id": 81, "topic": "Kubernetes", "question": "Что такое Pod в Kubernetes?", "options": ["Группа контейнеров", "Физический сервер", "Сеть", "База данных"], "correct": "Группа контейнеров"},
    {"id": 82, "topic": "Kubernetes", "question": "Что делает kubectl?", "options": ["CLI для управления K8s", "Сервер баз данных", "Система мониторинга", "Веб-сервер"], "correct": "CLI для управления K8s"},
    {"id": 83, "topic": "Kubernetes", "question": "Что такое Deployment?", "options": ["Ресурс для управления подами", "База данных", "Тип сети", "Система мониторинга"], "correct": "Ресурс для управления подами"},
    {"id": 84, "topic": "Kubernetes", "question": "Что такое Service в K8s?", "options": ["Балансирует трафик к подам", "База данных", "Сеть", "Тип пода"], "correct": "Балансирует трафик к подам"},
    {"id": 85, "topic": "Kubernetes", "question": "Что такое Ingress?", "options": ["Управляет внешним доступом к сервисам", "Тип пода", "База данных", "Система мониторинга"], "correct": "Управляет внешним доступом к сервисам"},
    {"id": 86, "topic": "Kubernetes", "question": "Что такое ConfigMap?", "options": ["Хранит конфигурацию", "База данных", "Тип сети", "Система мониторинга"], "correct": "Хранит конфигурацию"},
    {"id": 87, "topic": "Kubernetes", "question": "Что такое 'kubelet'?", "options": ["Агент на узле, управляющий подам", "CLI для K8s", "База данных", "Система мониторинга"], "correct": "Агент на узле, управляющий подам"},
    {"id": 88, "topic": "Kubernetes", "question": "Что такое 'etcd'?", "options": ["Хранилище данных кластера K8s", "База данных", "Система логирования", "Тип пода"], "correct": "Хранилище данных кластера K8s"},
    {"id": 89, "topic": "Terraform", "question": "Что такое Terraform?", "options": ["Инструмент IaC (Infrastructure as Code)", "CI/CD система", "База данных", "Веб-сервер"], "correct": "Инструмент IaC (Infrastructure as Code)"},
    {"id": 90, "topic": "Terraform", "question": "Что такое 'terraform plan'?", "options": ["Показывает изменения до применения", "Применяет изменения", "Удаляет инфраструктуру", "Создает план работ"], "correct": "Показывает изменения до применения"},
    {"id": 91, "topic": "Terraform", "question": "Что такое состояние (state) в Terraform?", "options": ["Файл с информацией о ресурсах", "Система мониторинга", "База данных", "Логи"], "correct": "Файл с информацией о ресурсах"},
    {"id": 92, "topic": "Terraform", "question": "Чем отличается Terraform от Ansible?", "options": ["Terraform для управления инфраструктурой, Ansible для конфигурации", "Они одинаковые", "Terraform для конфигурации, Ansible для инфраструктуры", "Ни чем"], "correct": "Terraform для управления инфраструктурой, Ansible для конфигурации"},
    {"id": 93, "topic": "Terraform", "question": "Что такое провайдер в Terraform?", "options": ["Плагин для взаимодействия с API (AWS, GCP, Azure)", "Тип ресурса", "Система мониторинга", "База данных"], "correct": "Плагин для взаимодействия с API (AWS, GCP, Azure)"},
    {"id": 94, "topic": "Terraform", "question": "Как импортировать существующий ресурс?", "options": ["terraform import <address> <id>", "terraform add", "terraform create", "terraform load"], "correct": "terraform import <address> <id>"},
    {"id": 95, "topic": "Terraform", "question": "Что делает 'terraform destroy'?", "options": ["Уничтожает всю инфраструктуру", "Сохраняет состояние", "Применяет изменения", "Показывает план"], "correct": "Уничтожает всю инфраструктуру"},
    {"id": 96, "topic": "Monitoring", "question": "Что такое Prometheus?", "options": ["Система мониторинга и метрик", "База данных", "Веб-сервер", "CI/CD система"], "correct": "Система мониторинга и метрик"},
    {"id": 97, "topic": "Monitoring", "question": "Что такое Grafana?", "options": ["Инструмент визуализации дашбордов", "Система логирования", "База данных", "CI/CD система"], "correct": "Инструмент визуализации дашбордов"},
    {"id": 98, "topic": "Monitoring", "question": "Что такое экспортёр в Prometheus?", "options": ["Сборщик метрик со сторонних систем", "Дашборд", "База данных", "CI/CD система"], "correct": "Сборщик метрик со сторонних систем"},
    {"id": 99, "topic": "Monitoring", "question": "Что такое SLO?", "options": ["Service Level Objective — целевой уровень обслуживания", "Система логирования", "База данных", "Тип метрики"], "correct": "Service Level Objective — целевой уровень обслуживания"},
    {"id": 100, "topic": "Monitoring", "question": "Что такое Alertmanager?", "options": ["Управляет уведомлениями в Prometheus", "Система мониторинга", "База данных", "Веб-сервер"], "correct": "Управляет уведомлениями в Prometheus"},
    {"id": 101, "topic": "Monitoring", "question": "Что такое healthcheck?", "options": ["Проверка доступности сервиса", "Система мониторинга", "База данных", "CI/CD система"], "correct": "Проверка доступности сервиса"},
    {"id": 102, "topic": "Monitoring", "question": "Что такое трейсинг (tracing)?", "options": ["Отслеживание запросов в распределённых системах", "Система мониторинга", "База данных", "CI/CD система"], "correct": "Отслеживание запросов в распределённых системах"},
    {"id": 103, "topic": "Monitoring", "question": "Что такое 'metrics' в мониторинге?", "options": ["Числовые показатели состояния системы", "Логи", "Трейсы", "События"], "correct": "Числовые показатели состояния системы"},
    {"id": 104, "topic": "Monitoring", "question": "Что такое 'dashboard'?", "options": ["Панель визуализации метрик", "База данных", "Система алертов", "Сетевой протокол"], "correct": "Панель визуализации метрик"},
    {"id": 105, "topic": "Databases", "question": "Что такое SQL?", "options": ["Язык запросов к базам данных", "База данных", "Сервер БД", "CI/CD система"], "correct": "Язык запросов к базам данных"},
    {"id": 106, "topic": "Databases", "question": "Чем отличается PostgreSQL от MySQL?", "options": ["PostgreSQL — объектно-реляционная, MySQL — реляционная", "Они одинаковые", "PostgreSQL быстрее", "MySQL — ORM"], "correct": "PostgreSQL — объектно-реляционная, MySQL — реляционная"},
    {"id": 107, "topic": "Databases", "question": "Что такое JOIN?", "options": ["Объединение таблиц", "Создание индекса", "Удаление данных", "Создание БД"], "correct": "Объединение таблиц"},
    {"id": 108, "topic": "Databases", "question": "Как сделать резервное копирование PostgreSQL?", "options": ["pg_dump dbname > backup.sql", "psql dump", "backup postgres", "pg_backup"], "correct": "pg_dump dbname > backup.sql"},
    {"id": 109, "topic": "Databases", "question": "Что такое индекс в БД?", "options": ["Ускоряет поиск данных", "Тип данных", "Система логирования", "CI/CD система"], "correct": "Ускоряет поиск данных"},
    {"id": 110, "topic": "Security", "question": "Что такое Fail2ban?", "options": ["Блокирует IP после неудачных попыток входа", "Файрвол", "Система мониторинга", "Антивирус"], "correct": "Блокирует IP после неудачных попыток входа"},
    {"id": 111, "topic": "Security", "question": "Как запретить вход по паролю в SSH?", "options": ["PasswordAuthentication no", "PermitRootLogin no", "AllowUsers no", "DisablePassword yes"], "correct": "PasswordAuthentication no"},
    {"id": 112, "topic": "Security", "question": "Что такое SSL/TLS?", "options": ["Протокол шифрования", "Система мониторинга", "База данных", "CI/CD система"], "correct": "Протокол шифрования"},
    {"id": 113, "topic": "Security", "question": "Что такое Let's Encrypt?", "options": ["Бесплатный центр сертификации SSL", "Антивирус", "Файрвол", "CI/CD система"], "correct": "Бесплатный центр сертификации SSL"},
    {"id": 114, "topic": "Security", "question": "Что такое DDoS атака?", "options": ["Перегрузка сервера запросами", "Кража данных", "Вирус", "Атака на пароль"], "correct": "Перегрузка сервера запросами"},
    {"id": 115, "topic": "Security", "question": "Как защитить SSH?", "options": ["Использовать ключи, запретить пароль, сменить порт", "Никак", "Поставить антивирус", "Выключить сеть"], "correct": "Использовать ключи, запретить пароль, сменить порт"},
    {"id": 116, "topic": "Security", "question": "Что такое OWASP?", "options": ["Стандарт безопасности веб-приложений", "Антивирус", "База данных", "CI/CD система"], "correct": "Стандарт безопасности веб-приложений"},
    {"id": 117, "topic": "Security", "question": "Что такое 'HTTPS'?", "options": ["HTTP с шифрованием", "Сетевой протокол", "База данных", "Система мониторинга"], "correct": "HTTP с шифрованием"},
    {"id": 118, "topic": "Security", "question": "Что такое 'API key'?", "options": ["Ключ для аутентификации API", "Пароль", "Сертификат", "Токен"], "correct": "Ключ для аутентификации API"},
    {"id": 119, "topic": "My Cases", "question": "Как вы починили 502 Bad Gateway на Container Packer?", "options": ["Перезапустил Nginx", "Ограничил CPU через CPUQuota=80% в systemd", "Добавил больше памяти", "Обновил Python"], "correct": "Ограничил CPU через CPUQuota=80% в systemd"},
    {"id": 120, "topic": "My Cases", "question": "Почему перестал работать Webhook и как вы исправили?", "options": ["GitHub изменил API", "Порт 9000 заблокировал хостинг, перевел на HTTPS через Nginx", "Слетели права доступа", "Закончилось место"], "correct": "Порт 9000 заблокировал хостинг, перевел на HTTPS через Nginx"},
    {"id": 121, "topic": "My Cases", "question": "Какой уникальный опыт вы получили на линии 102?", "options": ["Работа с критически важной системой 24/7", "Настройка маршрутизаторов", "Программирование на C++", "Администрирование Windows"], "correct": "Работа с критически важной системой 24/7"},
    {"id": 122, "topic": "My Cases", "question": "Какой стек использует Container Packer?", "options": ["Django + MySQL", "Streamlit + Nginx + systemd", "Node.js + MongoDB", "PHP + Apache"], "correct": "Streamlit + Nginx + systemd"},
    {"id": 123, "topic": "My Cases", "question": "Как вы настроили мониторинг для Container Packer?", "options": ["Prometheus + Grafana", "Beszel + Telegram-алерты", "Zabbix", "Nagios"], "correct": "Beszel + Telegram-алерты"},
    {"id": 124, "topic": "My Cases", "question": "Что вы внедрили в CRM Planfix?", "options": ["Учет ИТ-оборудования и ITSM-процессы", "Чат-бот", "Онлайн-магазин", "Биллинг"], "correct": "Учет ИТ-оборудования и ITSM-процессы"},
    {"id": 125, "topic": "My Cases", "question": "Какой CI/CD вы используете в Container Packer?", "options": ["Jenkins", "GitLab CI", "GitHub Actions + Webhook", "TeamCity"], "correct": "GitHub Actions + Webhook"},
    {"id": 126, "topic": "My Cases", "question": "Какой VPS провайдер заблокировал порт 9000?", "options": ["hoster.by", "kamatera.com", "fornex.com", "digitalocean.com"], "correct": "fornex.com"},
    {"id": 127, "topic": "My Cases", "question": "Какой домен использует Container Packer?", "options": ["autolot25.ddns.net", "packer.cuby.by", "trainer.ddns.net", "aigenerator.myvnc.com"], "correct": "packer.cuby.by"},
    {"id": 128, "topic": "My Cases", "question": "Как часто настроен ределивер в GitHub Actions?", "options": ["Каждый час", "Каждые 6 часов", "Раз в день", "Раз в неделю"], "correct": "Каждые 6 часов"},
    {"id": 129, "topic": "My Cases", "question": "Какая итоговая надёжность системы Container Packer?", "options": ["90-95%", "95-97%", "97-99%", "99.9%"], "correct": "97-99%"},
    {"id": 130, "topic": "My Cases", "question": "Что вы использовали для асинхронного ответа вебхука?", "options": ["celery", "threading", "asyncio", "multiprocessing"], "correct": "threading"},
    {"id": 131, "topic": "My Cases", "question": "Какой язык использует Auto Inventory System?", "options": ["Python (Flask)", "Python (Django)", "Node.js", "Go"], "correct": "Python (Flask)"},
    {"id": 132, "topic": "My Cases", "question": "Какой домен у AI Post Generator?", "options": ["aigenerator.ddns.net", "aigenerator.myvnc.com", "ai.cuby.by", "generator.ai"], "correct": "aigenerator.myvnc.com"},
    {"id": 133, "topic": "My Cases", "question": "Что вы используете для мониторинга серверов?", "options": ["Prometheus", "Zabbix", "Beszel", "Datadog"], "correct": "Beszel"},
    {"id": 134, "topic": "My Cases", "question": "Какой домен у DevOps Interview Trainer?", "options": ["trainer.ddns.net", "trainer.myvnc.com", "devops.cuby.by", "interview.ai"], "correct": "trainer.ddns.net"},
    {"id": 135, "topic": "My Cases", "question": "Сколько вопросов в DevOps Interview Trainer?", "options": ["50", "100", "150", "248"], "correct": "248"},
    {"id": 136, "topic": "My Cases", "question": "Какой стек использует DevOps Interview Trainer?", "options": ["Flask + Nginx", "Django + Apache", "Node.js + Express", "Go + Nginx"], "correct": "Flask + Nginx"},
    {"id": 137, "topic": "My Cases", "question": "Что вы использовали для управления версиями Container Packer?", "options": ["Git", "SVN", "Mercurial", "Perforce"], "correct": "Git"},
    {"id": 138, "topic": "My Cases", "question": "Какой сервер использует Container Packer?", "options": ["VPS на Fornex", "AWS", "Google Cloud", "Azure"], "correct": "VPS на Fornex"},
    {"id": 139, "topic": "My Cases", "question": "Какой сервис используете для Telegram уведомлений?", "options": ["Telegram Bot API", "Webhook", "Long Polling", "Все варианты"], "correct": "Telegram Bot API"},
    {"id": 140, "topic": "My Cases", "question": "Что используете для асинхронного вебхука?", "options": ["threading", "asyncio", "celery", "multiprocessing"], "correct": "threading"},
    {"id": 141, "topic": "My Cases", "question": "Какая команда перезапускает сервис container-packer?", "options": ["sudo systemctl restart container-packer", "sudo service restart", "sudo restart", "sudo reload"], "correct": "sudo systemctl restart container-packer"},
    {"id": 142, "topic": "My Cases", "question": "Что делает скрипт deploy.sh в Container Packer?", "options": ["git pull + systemctl restart", "docker build", "npm install", "python setup.py"], "correct": "git pull + systemctl restart"},
    {"id": 143, "topic": "My Cases", "question": "Как часто запускается ределивер в GitHub Actions для Container Packer?", "options": ["Каждый час", "Каждые 6 часов", "Раз в день", "Раз в неделю"], "correct": "Каждые 6 часов"},
    {"id": 144, "topic": "My Cases", "question": "На каком языке написан скрипт ределивера в Container Packer?", "options": ["Python", "Bash", "JavaScript (Node.js, Octokit)", "Go"], "correct": "JavaScript (Node.js, Octokit)"},
    {"id": 145, "topic": "My Cases", "question": "Какой статус код считается неудачным для вебхука в ределивере?", "options": ["200-299", "300-399", "Меньше 200 или больше 299", "Только 500"], "correct": "Меньше 200 или больше 299"},
    {"id": 146, "topic": "My Cases", "question": "Какой флаг в ределивере проверяет, что доставка ещё не переотправлялась?", "options": ["redelivered", "retry", "redelivery", "attempt"], "correct": "redelivery"},
    {"id": 147, "topic": "Systemd", "question": "Что делает параметр StartLimitIntervalSec в systemd?", "options": ["Задаёт интервал для подсчёта перезапусков", "Задаёт таймаут запуска", "Ограничивает CPU", "Ограничивает память"], "correct": "Задаёт интервал для подсчёта перезапусков"},
    {"id": 148, "topic": "Systemd", "question": "Что делает параметр StartLimitBurst в systemd?", "options": ["Максимальное число перезапусков за интервал", "Скорость запуска", "Приоритет процесса", "Лимит памяти"], "correct": "Максимальное число перезапусков за интервал"},
    {"id": 149, "topic": "Monitoring", "question": "Как часто cron проверяет вебхук в Container Packer?", "options": ["Каждую минуту", "Каждые 5 минут", "Каждые 15 минут", "Каждый час"], "correct": "Каждые 5 минут"},
    {"id": 150, "topic": "Monitoring", "question": "Сколько времени занимает восстановление вебхука в Container Packer?", "options": ["1-2 секунды", "5-6 секунд", "10-11 секунд", "Минута"], "correct": "5-6 секунд"},
    {"id": 151, "topic": "Monitoring", "question": "Сколько времени занимает восстановление приложения (Streamlit) в Container Packer?", "options": ["1-2 секунды", "5-6 секунд", "10-11 секунд", "Минута"], "correct": "10-11 секунд"},
    {"id": 152, "topic": "My Cases", "question": "При каком заполнении диска приходит Telegram-уведомление в Container Packer?", "options": ["Более 50%", "Более 75%", "Более 85%", "Более 95%"], "correct": "Более 85%"},
    {"id": 153, "topic": "My Cases", "question": "Как называется Telegram-бот для уведомлений в Container Packer?", "options": ["ContainerBot", "PackerBot", "AutoInventoryBot", "DeployBot"], "correct": "AutoInventoryBot"},
    {"id": 154, "topic": "My Cases", "question": "Какой порт слушает вебхук в Container Packer?", "options": ["80", "443", "8080", "9000"], "correct": "9000"},
    {"id": 155, "topic": "My Cases", "question": "Какой порт слушает Streamlit-приложение в Container Packer?", "options": ["80", "443", "8501", "9000"], "correct": "8501"},
    {"id": 156, "topic": "Docker", "question": "Что такое Dockerfile?", "options": ["Файл с инструкциями для сборки образа", "Файл с конфигурацией сети", "Файл с логами", "Файл с данными"], "correct": "Файл с инструкциями для сборки образа"},
    {"id": 157, "topic": "Docker", "question": "Какая команда собирает Docker образ из Dockerfile?", "options": ["docker create", "docker build", "docker run", "docker start"], "correct": "docker build"},
    {"id": 158, "topic": "CI/CD", "question": "Что такое ределивер в контексте GitHub Webhook?", "options": ["Повторная отправка неудачных доставок", "Отмена доставки", "Проверка статуса", "Логирование"], "correct": "Повторная отправка неудачных доставок"},
    {"id": 159, "topic": "CI/CD", "question": "Какой инструмент используется в ределивере для работы с GitHub API?", "options": ["axios", "request", "Octokit", "fetch"], "correct": "Octokit"},
    {"id": 160, "topic": "Linux", "question": "Что делает команда 'systemctl daemon-reload'?", "options": ["Перезагружает systemd", "Перечитывает конфигурацию systemd", "Перезапускает все сервисы", "Останавливает systemd"], "correct": "Перечитывает конфигурацию systemd"},
    {"id": 161, "topic": "Linux", "question": "Какой лимит CPU установлен для Container Packer в systemd?", "options": ["50%", "80%", "100%", "200%"], "correct": "80%"},
    {"id": 162, "topic": "Linux", "question": "Какой лимит памяти установлен для Container Packer в systemd?", "options": ["256MB", "512MB", "800MB", "1GB"], "correct": "800MB"},
    {"id": 163, "topic": "Security", "question": "Какой порт закрыт от внешнего мира в Container Packer?", "options": ["443", "80", "8501", "9000"], "correct": "8501"},
    {"id": 164, "topic": "Monitoring", "question": "Какой endpoint используется для healthcheck вебхука?", "options": ["/health", "/status", "/ping", "/check"], "correct": "/health"},
    {"id": 165, "topic": "Git", "question": "Какая команда отменяет последний коммит, сохраняя изменения в рабочей директории?", "options": ["git reset --soft HEAD~1", "git reset --hard HEAD~1", "git revert HEAD", "git checkout HEAD~1"], "correct": "git reset --soft HEAD~1"},
    {"id": 166, "topic": "Git", "question": "Что делает команда 'git revert'?", "options": ["Удаляет коммит из истории", "Создаёт новый коммит, отменяющий изменения", "Перемещает указатель ветки", "Очищает рабочую директорию"], "correct": "Создаёт новый коммит, отменяющий изменения"},
    {"id": 167, "topic": "Kubernetes", "question": "Что такое readinessProbe в Kubernetes?", "options": ["Проверяет, готов ли под принимать трафик", "Проверяет, жив ли контейнер", "Проверяет диск", "Проверяет сеть"], "correct": "Проверяет, готов ли под принимать трафик"},
    {"id": 168, "topic": "Kubernetes", "question": "Что такое livenessProbe в Kubernetes?", "options": ["Проверяет, жив ли контейнер, и перезапускает его при падении", "Проверяет готовность к трафику", "Проверяет диск", "Проверяет сеть"], "correct": "Проверяет, жив ли контейнер, и перезапускает его при падении"},
    {"id": 169, "topic": "CI/CD", "question": "Что такое GitHub Actions runner?", "options": ["Агент, который выполняет jobs", "Сервер баз данных", "Система мониторинга", "Веб-сервер"], "correct": "Агент, который выполняет jobs"},
    {"id": 170, "topic": "CI/CD", "question": "Что такое self-hosted runner?", "options": ["Собственный сервер для GitHub Actions", "Облачный runner", "Виртуальная машина", "Docker контейнер"], "correct": "Собственный сервер для GitHub Actions"},
    {"id": 171, "topic": "My Cases", "question": "Какой домен у DevOps Interview Trainer?", "options": ["trainer.ddns.net", "trainer.myvnc.com", "devops.cuby.by", "interview.ai"], "correct": "trainer.ddns.net"},
    {"id": 172, "topic": "My Cases", "question": "Какой фреймворк используется в DevOps Interview Trainer?", "options": ["Django", "Flask", "FastAPI", "Express"], "correct": "Flask"},
    {"id": 173, "topic": "My Cases", "question": "Какой скрипт отвечает за деплой в Container Packer?", "options": ["deploy.sh", "webhook.py", "start.sh", "update.sh"], "correct": "deploy.sh"},
    {"id": 174, "topic": "My Cases", "question": "Какая команда перезапускает вебхук при сбое?", "options": ["sudo systemctl restart webhook", "sudo restart webhook", "sudo webhook restart", "sudo service webhook restart"], "correct": "sudo systemctl restart webhook"},
    {"id": 175, "topic": "My Cases", "question": "Какой сервис обрабатывает асинхронные запросы от GitHub?", "options": ["Flask", "Streamlit", "Webhook на Python", "Nginx"], "correct": "Webhook на Python"},
    {"id": 176, "topic": "My Cases", "question": "Что делает параметр MemoryMax в systemd?", "options": ["Ограничивает память сервиса", "Увеличивает память", "Задаёт swap", "Ничего не делает"], "correct": "Ограничивает память сервиса"},
    {"id": 177, "topic": "My Cases", "question": "Какой алгоритм используется для упаковки коробок?", "options": ["3D bin packing", "2D bin packing", "Genetic algorithm", "Greedy algorithm"], "correct": "3D bin packing"},
    {"id": 178, "topic": "My Cases", "question": "Какой порт использует Nginx для HTTPS?", "options": ["80", "443", "8080", "8443"], "correct": "443"},
    {"id": 179, "topic": "Scripting", "question": "Какая библиотека Python используется для создания веб-приложений в Auto Inventory System?", "options": ["Django", "Flask", "FastAPI", "Tornado"], "correct": "Flask"},
    {"id": 180, "topic": "Scripting", "question": "Какой фреймворк Python используется в AI Post Generator для веб-интерфейса?", "options": ["Flask", "Django", "Streamlit", "FastAPI"], "correct": "Streamlit"},
    {"id": 181, "topic": "Scripting", "question": "Как в Python создать асинхронный ответ вебхука, чтобы не блокировать GitHub?", "options": ["asyncio", "threading", "multiprocessing", "celery"], "correct": "threading"},
    {"id": 182, "topic": "Scripting", "question": "Какая библиотека используется для работы с Telegram Bot API в Container Packer?", "options": ["requests", "python-telegram-bot", "telebot", "Все варианты"], "correct": "Все варианты"},
    {"id": 183, "topic": "Scripting", "question": "Как в Python отправить HTTP-запрос к API?", "options": ["requests.get()", "urllib.request", "http.client", "Все варианты"], "correct": "Все варианты"},
    {"id": 184, "topic": "Scripting", "question": "Какая библиотека используется в ределивере для работы с GitHub API?", "options": ["axios", "requests", "Octokit", "fetch"], "correct": "Octokit"},
    {"id": 185, "topic": "Scripting", "question": "Как в JavaScript (Node.js) установить пакет через npm?", "options": ["npm install <package>", "npm add <package>", "npm get <package>", "npm download <package>"], "correct": "npm install <package>"},
    {"id": 186, "topic": "Scripting", "question": "Какой инструмент используется для запуска JavaScript-скрипта в ределивере?", "options": ["node script.js", "npm run script", "js script.js", "javascript script.js"], "correct": "node script.js"},
    {"id": 187, "topic": "Scripting", "question": "Какая библиотека Python используется для мониторинга и проверки здоровья вебхука?", "options": ["requests", "urllib", "http.client", "Все варианты"], "correct": "Все варианты"},
    {"id": 188, "topic": "Scripting", "question": "Как в Python получить переменные окружения?", "options": ["os.environ.get('KEY')", "os.getenv('KEY')", "Оба варианта", "Ни один"], "correct": "Оба варианта"},
    {"id": 189, "topic": "Scripting", "question": "Как в Node.js получить переменные окружения?", "options": ["process.env.KEY", "system.env.KEY", "os.getenv('KEY')", "environment.KEY"], "correct": "process.env.KEY"},
    {"id": 190, "topic": "Scripting", "question": "Как в Python отправить сообщение в Telegram через Bot API?", "options": ["requests.post(url, json=data)", "telegram.send()", "bot.send_message()", "api.call()"], "correct": "requests.post(url, json=data)"},
    {"id": 191, "topic": "Scripting", "question": "Какая структура данных в Python используется для хранения вопросов в тренажёре?", "options": ["Список словарей (list of dicts)", "Массив", "JSON", "XML"], "correct": "Список словарей (list of dicts)"},
    {"id": 192, "topic": "Scripting", "question": "Как в Python запустить shell-команду и получить вывод?", "options": ["subprocess.run()", "os.system()", "os.popen()", "Все варианты"], "correct": "Все варианты"},
    {"id": 193, "topic": "Scripting", "question": "Как в Python создать простой HTTP-сервер для вебхука?", "options": ["http.server", "flask", "fastapi", "Все варианты"], "correct": "Все варианты"},
    {"id": 194, "topic": "Scripting", "question": "Как в Node.js выполнить HTTP-запрос к API?", "options": ["axios.get()", "fetch()", "http.request()", "Все варианты"], "correct": "Все варианты"},
    {"id": 195, "topic": "Scripting", "question": "Какой менеджер пакетов используется в проекте ределивера?", "options": ["npm", "yarn", "pnpm", "Все варианты"], "correct": "npm"},
    {"id": 196, "topic": "Scripting", "question": "Как в Python обработать ошибку при HTTP-запросе?", "options": ["try/except", "if response.status_code != 200", "Оба варианта", "Ни один"], "correct": "Оба варианта"},
    {"id": 197, "topic": "Scripting", "question": "Как в JavaScript распарсить JSON-ответ от API?", "options": ["JSON.parse()", "response.json()", "Оба варианта", "Ни один"], "correct": "Оба варианта"},
    {"id": 198, "topic": "Scripting", "question": "Какой фреймворк Python используется в DevOps Interview Trainer?", "options": ["Django", "Flask", "FastAPI", "Streamlit"], "correct": "Flask"},
    {"id": 199, "topic": "My Cases", "question": "Какая компания производит мобильные микрофабрики (MMF) для строительства домов?", "options": ["Cuby", "Tesla", "SpaceX", "Amazon"], "correct": "Cuby"},
    {"id": 200, "topic": "My Cases", "question": "Какая штаб-квартира у компании Cuby?", "options": ["Минск, Беларусь", "Москва, Россия", "Уилмингтон, Делавэр, США", "Лондон, Великобритания"], "correct": "Уилмингтон, Делавэр, США"},
    {"id": 201, "topic": "My Cases", "question": "Какова оценка компании Cuby после последнего раунда финансирования (Series B)?", "options": ["$100 млн", "$257.5 млн", "$500 млн", "$1 млрд"], "correct": "$257.5 млн"},
    {"id": 202, "topic": "My Cases", "question": "Какой принцип Cuby помогает сократить количество строительных отходов?", "options": ["Быстрая сборка", "Цифровой раскрой материалов", "Ручной труд", "Использование бетона"], "correct": "Цифровой раскрой материалов"},
    {"id": 203, "topic": "My Cases", "question": "Какую задачу решает Container Packer в компании Cuby?", "options": ["Упаковка коробок в контейнеры", "Учёт сотрудников", "Бухгалтерия", "Маркетинг"], "correct": "Упаковка коробок в контейнеры"},
    {"id": 204, "topic": "My Cases", "question": "Сколько рабочих требуется для сборки дома по технологии Cuby?", "options": ["10-15", "20-30", "4 неквалифицированных", "1 квалифицированный"], "correct": "4 неквалифицированных"},
    {"id": 205, "topic": "My Cases", "question": "За сколько дней собирается дом по технологии Cuby?", "options": ["7 дней", "14 дней", "30 дней", "60 дней"], "correct": "30 дней"},
    {"id": 206, "topic": "My Cases", "question": "Какой тип контейнеров поддерживает Container Packer?", "options": ["10ft, 20ft", "20ft, 20HC, 40ft, 40HC", "Только 40ft", "Все размеры"], "correct": "20ft, 20HC, 40ft, 40HC"},
    {"id": 207, "topic": "My Cases", "question": "Какой AI-инструмент вы используете для DevOps задач?", "options": ["Только ChatGPT", "Только GitHub Copilot", "DeepSeek + ChatGPT + Copilot", "Никакой"], "correct": "DeepSeek + ChatGPT + Copilot"},
    {"id": 208, "topic": "My Cases", "question": "Как вы учились DevOps?", "options": ["На курсах", "По книгам", "Сразу на практике с AI (DeepSeek)", "На работе"], "correct": "Сразу на практике с AI (DeepSeek)"},
    {"id": 209, "topic": "My Cases", "question": "Какой инструмент мониторинга вы используете для серверов?", "options": ["Prometheus", "Zabbix", "Beszel", "Datadog"], "correct": "Beszel"},
    {"id": 210, "topic": "My Cases", "question": "Как часто вы получаете уведомления о деплое в Telegram?", "options": ["Никогда", "При каждом успешном деплое", "Только при ошибках", "Раз в день"], "correct": "При каждом успешном деплое"},
    {"id": 211, "topic": "My Cases", "question": "Какой VPS провайдер используется для Container Packer?", "options": ["hoster.by", "kamatera.com", "fornex.com", "digitalocean.com"], "correct": "fornex.com"},
    {"id": 212, "topic": "My Cases", "question": "Какой домен у DevOps Interview Trainer?", "options": ["trainer.ddns.net", "trainer.myvnc.com", "devops.cuby.by", "interview.ai"], "correct": "trainer.ddns.net"},
    {"id": 213, "topic": "My Cases", "question": "Какую роль вы выполняете в проекте Container Packer?", "options": ["Пишу алгоритм упаковки", "Настраиваю CI/CD, деплой, мониторинг", "Дизайн UI", "Маркетинг"], "correct": "Настраиваю CI/CD, деплой, мониторинг"},
    {"id": 214, "topic": "My Cases", "question": "Какую библиотеку вы установили для ускорения NumPy?", "options": ["CUDA", "OpenBLAS", "TensorFlow", "PyTorch"], "correct": "OpenBLAS"},
    {"id": 215, "topic": "My Cases", "question": "Сколько времени занимает компоновка контейнера после оптимизации?", "options": ["30 секунд", "2-3 минуты", "6-7 минут", "10 минут"], "correct": "2-3 минуты"},
    {"id": 216, "topic": "My Cases", "question": "Что показывает ошибка 502 Bad Gateway?", "options": ["Сервер не найден", "Шлюз не получил ответ от бэкенда", "Нет доступа", "Слишком много запросов"], "correct": "Шлюз не получил ответ от бэкенда"},
    {"id": 217, "topic": "My Cases", "question": "Как вы исправили 502 Bad Gateway в Container Packer?", "options": ["Перезапустил Nginx", "Ограничил CPU через CPUQuota=80%", "Добавил больше памяти", "Обновил Python"], "correct": "Ограничил CPU через CPUQuota=80%"},
    {"id": 218, "topic": "My Cases", "question": "Какой порт слушает вебхук в Container Packer?", "options": ["80", "443", "8080", "9000"], "correct": "9000"},
    {"id": 219, "topic": "My Cases", "question": "Какой порт слушает Streamlit-приложение в Container Packer?", "options": ["80", "443", "8501", "9000"], "correct": "8501"},
    {"id": 220, "topic": "My Cases", "question": "Какой параметр systemd ограничивает использование CPU?", "options": ["MemoryMax", "CPUQuota", "LimitCPU", "CPUMax"], "correct": "CPUQuota"},
    {"id": 221, "topic": "My Cases", "question": "Какой параметр systemd ограничивает использование памяти?", "options": ["MemoryMax", "RAMLimit", "MemoryQuota", "MemMax"], "correct": "MemoryMax"},
    {"id": 222, "topic": "My Cases", "question": "Как часто cron проверяет вебхук в Container Packer?", "options": ["Каждую минуту", "Каждые 5 минут", "Каждые 15 минут", "Каждый час"], "correct": "Каждые 5 минут"},
    {"id": 223, "topic": "My Cases", "question": "Сколько времени занимает восстановление вебхука при падении?", "options": ["1-2 секунды", "5-6 секунд", "10-11 секунд", "Минута"], "correct": "5-6 секунд"},
    {"id": 224, "topic": "My Cases", "question": "Сколько времени занимает восстановление приложения (Streamlit) при падении?", "options": ["1-2 секунды", "5-6 секунд", "10-11 секунд", "Минута"], "correct": "10-11 секунд"},
    {"id": 225, "topic": "My Cases", "question": "Как часто запускается ределивер в GitHub Actions?", "options": ["Каждый час", "Каждые 6 часов", "Раз в день", "Раз в неделю"], "correct": "Каждые 6 часов"},
    {"id": 226, "topic": "My Cases", "question": "На каком языке написан скрипт ределивера?", "options": ["Python", "Bash", "JavaScript (Node.js, Octokit)", "Go"], "correct": "JavaScript (Node.js, Octokit)"},
    {"id": 227, "topic": "My Cases", "question": "Какой инструмент используется в ределивере для работы с GitHub API?", "options": ["axios", "requests", "Octokit", "fetch"], "correct": "Octokit"},
    {"id": 228, "topic": "My Cases", "question": "Как называется Telegram-бот для уведомлений в Container Packer?", "options": ["ContainerBot", "PackerBot", "AutoInventoryBot", "DeployBot"], "correct": "AutoInventoryBot"},
    {"id": 229, "topic": "My Cases", "question": "При каком заполнении диска приходит Telegram-уведомление?", "options": ["Более 50%", "Более 75%", "Более 85%", "Более 95%"], "correct": "Более 85%"},
    {"id": 230, "topic": "My Cases", "question": "Какой фреймворк используется в DevOps Interview Trainer?", "options": ["Django", "Flask", "FastAPI", "Streamlit"], "correct": "Flask"},
    {"id": 231, "topic": "My Cases", "question": "Как вы настраиваете мониторинг серверов?", "options": ["Prometheus", "Zabbix", "Beszel + Telegram-алерты", "Nagios"], "correct": "Beszel + Telegram-алерты"},
    {"id": 232, "topic": "My Cases", "question": "Что вы внедрили в CRM Planfix для учёта?", "options": ["Учет ИТ-оборудования и ITSM-процессы", "Чат-бот", "Онлайн-магазин", "Биллинг"], "correct": "Учет ИТ-оборудования и ITSM-процессы"},
    {"id": 233, "topic": "My Cases", "question": "Какой уникальный опыт вы получили на линии 102?", "options": ["Работа с критически важной системой 24/7", "Настройка маршрутизаторов", "Программирование на C++", "Администрирование Windows"], "correct": "Работа с критически важной системой 24/7"},
    {"id": 234, "topic": "My Cases", "question": "Какой подход к обучению вы используете?", "options": ["Читаю книги", "Смотрю видео", "Сразу применяю на практике с AI", "Хожу на курсы"], "correct": "Сразу применяю на практике с AI"},
    {"id": 235, "topic": "My Cases", "question": "Какой ваш главный инструмент для DevOps?", "options": ["VS Code", "PyCharm", "Терминал + bash + AI", "Git GUI"], "correct": "Терминал + bash + AI"},
    {"id": 236, "topic": "My Cases", "question": "Какую версию Python вы используете после оптимизации?", "options": ["3.10", "3.11", "3.12", "3.13.13"], "correct": "3.13.13"},
    {"id": 237, "topic": "My Cases", "question": "Какую компанию вы выбрали для работы и почему?", "options": ["Обычную IT-компанию", "Cuby — стройка будущего как IT-проект", "Банк", "Госструктуру"], "correct": "Cuby — стройка будущего как IT-проект"},
    {"id": 238, "topic": "My Cases", "question": "Какой формат работы вы рассматриваете?", "options": ["Только офис", "Только удалённо", "Гибридный", "Не важно"], "correct": "Гибридный"},
    {"id": 239, "topic": "My Cases", "question": "Как вы относитесь к использованию AI в работе?", "options": ["AI заменит инженеров", "AI — инструмент, который усиливает инженера", "AI вреден", "Никак"], "correct": "AI — инструмент, который усиливает инженера"},
    {"id": 240, "topic": "My Cases", "question": "Какую зарплату вы ожидаете?", "options": ["2000 BYN", "2500 BYN", "от 3000 BYN в зависимости от задач", "5000 BYN"], "correct": "от 3000 BYN в зависимости от задач"},
    {"id": 241, "topic": "My Cases", "question": "Как вы объясните DevOps бабушке?", "options": ["Чинят компьютеры", "Настраивают серверы", "Автоматизируют конвейер разработки, как конвейер на заводе", "Пишут код"], "correct": "Автоматизируют конвейер разработки, как конвейер на заводе"},
    {"id": 242, "topic": "My Cases", "question": "Что такое SRE?", "options": ["Site Reliability Engineering — подход к надёжности", "Software Development", "System Administration", "Security Engineering"], "correct": "Site Reliability Engineering — подход к надёжности"},
    {"id": 243, "topic": "My Cases", "question": "Какая ваша цель на ближайший год?", "options": ["Остаться на месте", "Вырасти до Middle DevOps", "Уйти в разработку", "Уйти в управление"], "correct": "Вырасти до Middle DevOps"},
    {"id": 244, "topic": "My Cases", "question": "Какой ваш любимый проект?", "options": ["Auto Inventory", "AI Post Generator", "Container Packer", "DevOps Interview Trainer"], "correct": "Container Packer"},
    {"id": 245, "topic": "My Cases", "question": "Что вам больше всего нравится в DevOps?", "options": ["Писать код", "Настраивать серверы", "Автоматизация и видеть результат", "Документация"], "correct": "Автоматизация и видеть результат"},
    {"id": 246, "topic": "My Cases", "question": "Что такое вайбкодинг (vibe coding)?", "options": ["Программирование в хорошем настроении", "Разработка с активным использованием AI и нейросетей", "Быстрое прототипирование", "Кодинг под музыку"], "correct": "Разработка с активным использованием AI и нейросетей"},
    {"id": 247, "topic": "My Cases", "question": "Какой AI вы используете чаще всего?", "options": ["ChatGPT", "GitHub Copilot", "DeepSeek", "Claude"], "correct": "DeepSeek"},
    {"id": 248, "topic": "My Cases", "question": "Как вы попали в DevOps?", "options": ["Через курсы", "Через книги", "Через практику с AI и DeepSeek", "Через работу"], "correct": "Через практику с AI и DeepSeek"},
]

# ============================================
# Flask routes
# ============================================

@app.route('/')
@app.route('/test')
def home():
    session.clear()
    session['start_time'] = time.time()
    session['score'] = 0
    session['current_index'] = 0
    session['topic'] = None
    session['mode'] = None

    topic_counts = {}
    for q in questions:
        topic_counts[q['topic']] = topic_counts.get(q['topic'], 0) + 1

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>DevOps Interview Trainer</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 900px; margin: 50px auto; padding: 20px; background: #f5f5f5; }
            button { background: #007bff; color: white; padding: 10px 20px; margin: 5px; border: none; border-radius: 5px; cursor: pointer; font-size: 14px; }
            button:hover { background: #0056b3; }
            .topic-select { margin: 20px 0; background: white; padding: 20px; border-radius: 10px; }
            h1 { color: #333; }
            .stats { font-size: 14px; color: #666; margin-top: 20px; }
        </style>
    </head>
    <body>
        <h1>DevOps Interview Trainer</h1>
        <p>Тренажёр по Linux, CI/CD, сетям, Docker, K8s, Terraform, мониторингу, безопасности, скриптингу и вашим кейсам.</p>
        <p><strong>Всего вопросов: 248</strong></p>

        <div class="topic-select">
            <h3>По темам</h3>
"""
    topics = [("Linux", "Linux"), ("CI/CD", "CI/CD"), ("Networks", "Сети"), ("Docker", "Docker"),
              ("Kubernetes", "Kubernetes"), ("Terraform", "Terraform"), ("Monitoring", "Мониторинг"),
              ("Databases", "Базы данных"), ("Security", "Безопасность"), ("My Cases", "Мои кейсы"),
              ("Scripting", "Скриптинг")]

    for topic_key, topic_name in topics:
        count = topic_counts.get(topic_key, 0)
        html += f'<form action="/start" method="get" style="display: inline;"><input type="hidden" name="topic" value="{topic_key}"><button type="submit">{topic_name} ({count})</button></form>\n'

    html += """
        </div>

        <div class="topic-select">
            <h3>Случайная тренировка</h3>
            <form action="/start" method="get" style="display: inline;">
                <input type="hidden" name="topic" value="random_public">
                <button type="submit">Случайный тест (20 вопросов, без моих кейсов)</button>
            </form>
            <form action="/start" method="get" style="display: inline;">
                <input type="hidden" name="topic" value="random_with_mycases">
                <button type="submit">Случайный тест (20 вопросов, включая мои кейсы)</button>
            </form>
        </div>

        <div class="stats">
            Статистика: вопросы добавляются и обновляются регулярно
        </div>
    </body>
    </html>
    """
    return html

@app.route('/start')
def start():
    topic = request.args.get('topic', 'random')
    session['start_time'] = time.time()
    session['score'] = 0
    session['current_index'] = 0
    session['topic'] = topic

    # Случайный тест без моих кейсов
    if topic == 'random_public':
        public_questions = [q for q in questions if q['topic'] != 'My Cases']
        if len(public_questions) < 20:
            sampled = public_questions
        else:
            sampled = random.sample(public_questions, 20)
        random.shuffle(sampled)
        session['question_ids'] = [q['id'] for q in sampled]
        session['mode'] = f"Случайный тест без моих кейсов ({len(session['question_ids'])} вопросов)"
        return redirect('/quiz')

    # Случайный тест с моими кейсами (требует пароль)
    if topic == 'random_with_mycases':
        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("Basic "):
            return authenticate()
        encoded = auth[6:]
        decoded = base64.b64decode(encoded).decode("utf-8")
        username, password = decoded.split(":", 1)
        if not check_auth(username, password):
            return authenticate()
        if len(questions) < 20:
            sampled = questions
        else:
            sampled = random.sample(questions, 20)
        random.shuffle(sampled)
        session['question_ids'] = [q['id'] for q in sampled]
        session['mode'] = f"Случайный тест с моими кейсами ({len(session['question_ids'])} вопросов)"
        return redirect('/quiz')

    # Проверка пароля для темы "Мои кейсы"
    if topic == "My Cases" or topic == "my_cases":
        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("Basic "):
            return authenticate()
        encoded = auth[6:]
        decoded = base64.b64decode(encoded).decode("utf-8")
        username, password = decoded.split(":", 1)
        if not check_auth(username, password):
            return authenticate()

    # Обычные темы
    topic_questions = [q for q in questions if q['topic'] == topic]
    random.shuffle(topic_questions)
    if not topic_questions:
        return "Тема не найдена"
    session['question_ids'] = [q['id'] for q in topic_questions]
    name_map = {"Linux": "Linux", "CI/CD": "CI/CD", "Networks": "Сети", "Docker": "Docker",
               "Kubernetes": "Kubernetes", "Terraform": "Terraform", "Monitoring": "Мониторинг",
               "Databases": "Базы данных", "Security": "Безопасность", "My Cases": "Мои кейсы",
               "Scripting": "Скриптинг"}
    session['mode'] = f"{name_map.get(topic, topic)} ({len(session['question_ids'])} вопросов)"

    return redirect('/quiz')
@app.route('/quiz')
def quiz():
    if 'question_ids' not in session or session['current_index'] >= len(session['question_ids']):
        return redirect('/result')

    qid = session['question_ids'][session['current_index']]
    q = next((q for q in questions if q['id'] == qid), None)
    elapsed = int(time.time() - session['start_time'])
    elapsed_min = elapsed // 60
    elapsed_sec = elapsed % 60

    options_html = ""
    for opt in q['options']:
        options_html += f'<label><input type="radio" name="answer" value="{opt}" required> {opt}</label><br><br>'

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Вопрос {session['current_index']+1}</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; background: #f5f5f5; }}
            button {{ background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }}
            .timer {{ font-size: 20px; color: #666; margin-bottom: 20px; }}
            .progress {{ font-size: 14px; color: #888; margin-bottom: 10px; }}
            .question {{ font-size: 18px; font-weight: bold; margin: 20px 0; }}
            .container {{ background: white; padding: 20px; border-radius: 10px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="timer">Время: {elapsed_min}:{elapsed_sec:02d}</div>
            <div class="progress">Прогресс: {session['current_index']+1} / {len(session['question_ids'])} | Счёт: {session['score']} | Режим: {session['mode']}</div>
            <div class="question">Вопрос {session['current_index']+1}: {q['question']}</div>
            <form action="/answer" method="post">
                {options_html}
                <input type="hidden" name="correct" value="{q['correct']}">
                <button type="submit">Ответить</button>
            </form>
        </div>
    </body>
    </html>
    """
    return html

@app.route('/answer', methods=['POST'])
def answer():
    user_answer = request.form.get('answer')
    correct_answer = request.form.get('correct')

    is_correct = (user_answer == correct_answer)
    if is_correct:
        session['score'] += 1

    session['current_index'] += 1

    if session['current_index'] >= len(session['question_ids']):
        return redirect('/result')

    elapsed = int(time.time() - session['start_time'])
    elapsed_min = elapsed // 60
    elapsed_sec = elapsed % 60

    if is_correct:
        result_html = f'<div style="color: green; font-weight: bold; margin: 20px 0;">Верно! +1 балл</div>'
    else:
        result_html = f'<div style="color: red; font-weight: bold; margin: 20px 0;">Неверно! Правильный ответ: {correct_answer}</div>'

    qid = session['question_ids'][session['current_index'] - 1]
    q = next((q for q in questions if q['id'] == qid), None)

    options_html = ""
    for opt in q['options']:
        checked = "checked" if user_answer == opt else ""
        disabled = "disabled"
        label_style = 'style="color: gray;"'
        if opt == correct_answer:
            label_style = 'style="color: green; font-weight: bold;"'
        elif opt == user_answer and user_answer != correct_answer:
            label_style = 'style="color: red; text-decoration: line-through;"'
        options_html += f'<label {label_style}><input type="radio" name="answer" value="{opt}" {checked} {disabled}> {opt}</label><br><br>'

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Результат</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; background: #f5f5f5; }}
            button {{ background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }}
            .timer {{ font-size: 20px; color: #666; margin-bottom: 20px; }}
            .progress {{ font-size: 14px; color: #888; margin-bottom: 10px; }}
            .container {{ background: white; padding: 20px; border-radius: 10px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="timer">Время: {elapsed_min}:{elapsed_sec:02d}</div>
            <div class="progress">Прогресс: {session['current_index']} / {len(session['question_ids'])} | Счёт: {session['score']} | Режим: {session['mode']}</div>
            {result_html}
            <div><strong>Вопрос:</strong> {q['question']}</div><br>
            {options_html}
            <a href="/quiz"><button>Следующий вопрос</button></a>
            <a href="/"><button style="background: #6c757d;">Завершить</button></a>
        </div>
    </body>
    </html>
    """
    return html

@app.route('/result')
def result():
    elapsed = int(time.time() - session['start_time'])
    elapsed_min = elapsed // 60
    elapsed_sec = elapsed % 60
    total = len(session['question_ids'])
    score = session['score']
    percent = (score / total) * 100 if total > 0 else 0

    if percent >= 90:
        grade = "Отлично!"
        color = "#28a745"
    elif percent >= 70:
        grade = "Хорошо!"
        color = "#17a2b8"
    elif percent >= 50:
        grade = "Средне. Нужно подтянуть."
        color = "#ffc107"
    else:
        grade = "Требуется много работы!"
        color = "#dc3545"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Результат теста</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; text-align: center; background: #f5f5f5; }}
            button {{ background: #007bff; color: white; padding: 10px 20px; margin: 5px; border: none; border-radius: 5px; cursor: pointer; }}
            .score {{ font-size: 48px; font-weight: bold; margin: 20px 0; color: {color}; }}
            .stats {{ font-size: 18px; margin: 10px 0; }}
            .container {{ background: white; padding: 30px; border-radius: 10px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Тест завершён!</h1>
            <div class="score">{percent:.0f}%</div>
            <div class="stats">Правильных ответов: {score} из {total}</div>
            <div class="stats">Время прохождения: {elapsed_min} мин {elapsed_sec} сек</div>
            <div class="stats">Режим: {session['mode']}</div>
            <h3>{grade}</h3>
            <a href="/"><button>Главное меню</button></a>
            <a href="/start?topic={session['topic']}"><button>Повторить тест</button></a>
        </div>
    </body>
    </html>
    """
    return html

def redirect(url):
    return f'<meta http-equiv="refresh" content="0;url={url}">'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
