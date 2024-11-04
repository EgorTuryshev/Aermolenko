# Руководство по Развертыванию Проекта

## Содержание

1. [Введение](#введение)
2. [Предварительные требования](#предварительные-требования)
3. [Начало работы](#начало-работы)
   - [Установка Node.js](#установка-nodejs)
   - [Клонирование репозитория](#клонирование-репозитория)
   - [Установка зависимостей](#установка-зависимостей)
   - [Запуск проекта](#запуск-проекта)
4. [Работа с проектом](#работа-с-проектом)
   - [Доска задач](#доска-задач)
   - [Git Workflow](#git-workflow)
   - [Компоненты](#компоненты)
5. [Дополнительные рекомендации](#дополнительные-рекомендации)
   - [Плагины для VS Code](#плагины-для-vs-code)
   - [Запуск в WSL](#запуск-в-wsl)
6. [Развертывание фронтенда](#развертывание-фронтенда)
   - [Развертывание с помощью Nginx](#развертывание-с-помощью-nginx)
   - [Развертывание с помощью Docker](#развертывание-с-помощью-docker)
7. [Развертывание бекенда](#развертывание-бекенда)
8. [Подготовка и импорт данных в БД](#подготовка-и-импорт-данных-в-бд)
9. [Документация API](#подробная-документация-по-api)

## Введение

Добро пожаловать в руководство по развертыванию нашего проекта!

## Предварительные требования

Перед началом работы убедитесь, что у вас установлены следующие инструменты:

- **Node.js** (версия 16.x или выше)
- **Git**
- **Visual Studio Code** (рекомендуется)

## Начало работы

### Установка Node.js

Если у вас не установлен Node.js, скачайте и установите его с [официального сайта](https://nodejs.org/en/download/).

Вы также можете использовать [Node Version Manager (nvm)](https://github.com/nvm-sh/nvm) для управления версиями Node.js:

```bash
# Установка nvm (для Linux и macOS)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.4/install.sh | bash

# Установка Node.js версии 16
nvm install 16
nvm use 16
```

### Клонирование репозитория

Клонируйте репозиторий проекта:

```bash
git clone git@github.com:Daniil11ru/data-management-homework-frontend.git
cd data-management-homework-frontend
```

### Установка зависимостей

Выполните команду для установки всех необходимых зависимостей:

```bash
npm install
```

### Запуск проекта

Запустите проект в режиме разработки:

```bash
npm start
```

Приложение будет доступно по адресу `http://localhost:3000/`.

## Работа с проектом

### Доска задач

Доска с задачами находится [здесь](https://github.com/users/Daniil11ru/projects/2/views/1). Выбирайте задачи по вкусу из файла задания, самостоятельно заносите их на доску, обновляйте статус и назначайте себя ответственным.

### Git Workflow

- **Не пушим в ветку `main`**.
- Создавайте отдельные ветки для каждой задачи или группы задач:

  ```bash
  git checkout -b feature/название-задачи
  ```

- После завершения работы создавайте Pull Request:

  ```bash
  git add .
  git commit -m "Описание изменений"
  git push origin feature/название-задачи
  ```

Подробная инструкция доступна [здесь](https://www.youtube.com/watch?v=8lGpZkjnkt4).

### Компоненты

- Используйте компоненты из директории `./components/material/`.
- Для создания новых компонентов используйте библиотеку [`@mui/material`](https://mui.com/material-ui/getting-started/overview/).

## Дополнительные рекомендации

### Плагины для VS Code

Рекомендуемые расширения:

- [ESLint](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint)
- [Node.js Modules Intellisense](https://marketplace.visualstudio.com/items?itemName=leizongmin.node-module-intellisense)
- [Prettier - Code Formatter](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode)

### Запуск в WSL

Для пользователей Windows рекомендуется запускать проект в [WSL](https://learn.microsoft.com/en-us/windows/dev-environment/javascript/nodejs-on-wsl). Это позволит работать в Linux-среде, сохраняя удобство Windows.

Примерная инструкция:

1. Установите WSL и дистрибутив Linux (например, Ubuntu).
2. В WSL терминале перейдите в папку проекта.
3. Установите зависимости и запустите проект как обычно.

## Развертывание фронтенда

### Развертывание с помощью Nginx

1. **Сборка проекта**:

   ```bash
   npm run build
   ```

2. **Настройка Nginx** (конфигурация примерная и может отличаться):

   Создайте файл конфигурации, например, `/etc/nginx/sites-available/yourproject`:

   ```nginx
    server {
        listen 80;
        server_name yourdomain.com;

        root /var/www/yourproject/build;
        index index.html index.htm;

        location / {
            try_files $uri /index.html;
        }

        # Решение проблемы CORS для взаимодействия с API
        location /api/ {
            proxy_pass http://backend_api_server_address;  # Укажите адрес вашего API сервера
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            # Добавление заголовков для разрешения CORS
            add_header 'Access-Control-Allow-Origin' '*';
            add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, PUT, DELETE';
            add_header 'Access-Control-Allow-Headers' 'Authorization, Content-Type, Accept';
            add_header 'Access-Control-Allow-Credentials' 'true';

            # Обработка preflight-запросов
            if ($request_method = OPTIONS) {
                add_header 'Access-Control-Allow-Origin' '*';
                add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, PUT, DELETE';
                add_header 'Access-Control-Allow-Headers' 'Authorization, Content-Type, Accept';
                add_header 'Access-Control-Allow-Credentials' 'true';
                return 204;
            }
        }
    }
   ```

3. **Активируйте конфигурацию и перезапустите Nginx**:

   ```bash
   sudo ln -s /etc/nginx/sites-available/yourproject /etc/nginx/sites-enabled/
   sudo systemctl restart nginx
   ```

### Развертывание с помощью Docker

1. **Создайте `Dockerfile`**(конфигурация примерная и может отличаться):

   ```dockerfile
   # Стадия 1: Сборка
   FROM node:16 AS build
   WORKDIR /app
   COPY package*.json ./
   RUN npm install
   COPY . .
   RUN npm run build

   # Стадия 2: Запуск
   FROM nginx:stable-alpine
   COPY --from=build /app/build /usr/share/nginx/html
   EXPOSE 80
   CMD ["nginx", "-g", "daemon off;"]
   ```

2. **Соберите и запустите Docker-контейнер**:

   ```bash
   docker build -t yourproject .
   docker run -d -p 80:80 yourproject
   ```

#### Использование docker-compose

1. **Создайте `docker-compose.yml`**:

   ```yaml
   version: '3'
   services:
     app:
       build: .
       ports:
         - '80:80'
   ```

2. **Запустите контейнеры**:

   ```bash
   docker-compose up -d
   ```

## Развертывание бекенда

### Предварительные требования

Перед началом развертывания бекенда убедитесь, что у вас установлены следующие компоненты:

- **Nginx**
- **PHP** (рекомендуется версия 8.2)
- **PHP-FPM**
- **Git**

### Шаги по развертыванию

#### 1. Клонирование репозитория

Склонируйте репозиторий бекенда на ваш сервер:

```bash
git clone git@github.com:yourname/backend.git /var/www/html/aermolenko
```

#### 2. Установка зависимостей

Перейдите в директорию проекта и установите необходимые зависимости с помощью Composer:

```bash
cd /var/www/html/aermolenko
composer install
```

> **Примечание:** Убедитесь, что Composer установлен на вашем сервере. Если нет, установите его, следуя [официальной инструкции](https://getcomposer.org/download/).

#### 3. Настройка прав доступа

Установите правильные права доступа для директорий:

```bash
sudo chown -R www-data:www-data /var/www/html/aermolenko
sudo find /var/www/html/aermolenko -type f -exec chmod 644 {} \;
sudo find /var/www/html/aermolenko -type d -exec chmod 755 {} \;
```

#### 4. Настройка Nginx

Создайте или отредактируйте файл конфигурации Nginx для вашего бекенда. Ниже приведена примерная конфигурация:

```nginx
server {
    listen 80;
    server_name _;

    root /var/www/html;
    index index.html index.nginx-debian.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /uploads/logo/ {
        alias /var/www/html/aermolenko/public/uploads/logo/;
        autoindex off;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_pass_header Access-Control-Allow-Origin;
        proxy_pass_header Access-Control-Allow-Methods;
        proxy_pass_header Access-Control-Allow-Headers;
        proxy_pass_header Access-Control-Allow-Credentials;

        if ($request_method = OPTIONS) {
            add_header Access-Control-Allow-Origin *;
            add_header Access-Control-Allow-Methods "GET, POST, OPTIONS, DELETE, PUT";
            add_header Access-Control-Allow-Headers "Authorization, Content-Type, X-Requested-With";
            add_header Access-Control-Allow-Credentials true;
            return 204;
        }
    }
}

server {
    listen 8080;
    server_name _;

    root /var/www/html/aermolenko/public;
    index index.php;

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/run/php/php8.2-fpm.sock;
    }

    location ~ /\.ht {
        deny all;
    }
}
```

##### Пояснение конфигурации

- **Первый серверный блок** (порт 80):
  - Обрабатывает запросы к фронтенду.
  - Проксирует запросы к API на бэкенд, работающий на порту 8080.
  - Настраивает CORS для корректного взаимодействия фронтенда с бэкендом.
  - Обрабатывает запросы к статическим файлам, таким как логотипы.

- **Второй серверный блок** (порт 8080):
  - Обрабатывает запросы к бэкенду.
  - Настраивает обработку PHP-файлов через PHP-FPM.
  - Защищает скрытые файлы и директории (например, `.htaccess`).

#### 5. Активация конфигурации и перезапуск Nginx

Сохраните конфигурационный файл (обычно в директории `/etc/nginx/sites-available/`) и создайте символическую ссылку в `/etc/nginx/sites-enabled/`:

```bash
sudo ln -s /etc/nginx/sites-available/your_backend_conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

> **Примечание:** Замените `your_backend_conf` на имя вашего конфигурационного файла.

#### 6. Проверка работы PHP-FPM

Убедитесь, что PHP-FPM запущен и слушает сокет `php8.2-fpm.sock`:

```bash
sudo systemctl status php8.2-fpm
```

Если сервис не запущен, запустите его:

```bash
sudo systemctl start php8.2-fpm
```

#### 7. Настройка переменных окружения

Скопируйте файл переменных окружения и настройте необходимые параметры (например, доступ к базе данных):

```bash
cp .env.example .env
nano .env
```

#### 8. Тестирование приложения

Откройте браузер и перейдите по адресу вашего сервера, чтобы убедиться, что бэкенд работает корректно.

### Решение возможных проблем

- **Ошибка 502 Bad Gateway**:
  - Проверьте, что PHP-FPM запущен и сокет указан правильно в конфигурации Nginx.
  - Убедитесь, что пользователь, под которым работает Nginx, имеет доступ к сокету PHP-FPM.

- **Проблемы с правами доступа**:
  - Проверьте права на директории и файлы в проекте.
  - Убедитесь, что веб-сервер имеет доступ к необходимым файлам и директориям.

- **Ошибки при работе с API**:
  - Проверьте настройки CORS в конфигурации Nginx.
  - Убедитесь, что бэкенд корректно обрабатывает запросы и возвращает ожидаемые ответы.

### Дополнительные рекомендации

- **Мониторинг логов**:
  - Логи Nginx обычно находятся в `/var/log/nginx/error.log` и `/var/log/nginx/access.log`.
  - Логи PHP-FPM можно найти в `/var/log/php8.2-fpm.log` или в указанном в конфигурации месте.

- **Обновление зависимостей**:
  - Регулярно обновляйте зависимости проекта с помощью Composer.
  - Перед обновлением убедитесь в совместимости новых версий пакетов.

- **Безопасность**:
  - Отключите отображение ошибок в продакшен-среде.
  - Защитите конфигурационные файлы и скрытые директории от доступа извне.

---
# Подготовка и импорт данных в БД

## 1. Загрузка данных в Excel

У нас есть три входных файла - agents_k_import.csv, productsale_k_import.xlsx и products_short_k_import.txt

Переварить первые два файла Excel сможет сам, а вот с текстовым придется побороться. Есть два варианта победить - по-умному и по-простому.

Вариант 1: по-умному.
1. Открываем новый xlsx-файл. Переходим на вкладку "Данные".
2. На верхней панели слева выбираем опцию "Получить данные". Выбираем пункт "Из файла", подпункт "Из тектсового/CSV-файла".
3. Проводник любезно предложит выбрать нужный файл и нажать кнопку "Импорт".
4. В открывшемся окне видим предпросмотр того, каким образом Excel закинет данные из файла в ячейки.
5. Если в окне мы видим язык древних шизов, значит у нас съехала ~~крыша~~ кодировка. Фиксится выбором UTF-8 Юникода тут же (см. ниже).

![!schizo](https://github.com/user-attachments/assets/3f180985-9440-48c6-8223-e2018e610c03)

6. Если всё совсем плохо, то могут не определиться разделители. В данном случае выбираем в этом же окне в выпадающем меню "Разделитель" запятую.
7. Если на экране видим картину как на картине снизу, то нажимаем кнопку "Загрузить".

![!notschizo](https://github.com/user-attachments/assets/3aa25e5d-db22-496a-b265-740722a5e224)

8. Поздравляем себя с завершением этого этапа подготовки данных:
![!good1](https://github.com/user-attachments/assets/1e9ee55a-da3f-406c-8d27-fa9f6b278d41)

9. Сохраните получившийся файл с названием **ProductsImport.xlsx**

Вариант 2: по-простому.
1. Открываем новый xlsx-файл.
2. Открываем products_short_k_import.txt.
3. В products_short_k_import.txt смело жмем Ctrl + A. Еще смелее жмем Ctrl + C.
4. Переходим в xlsx-файл, выбираем ячейку А1 и жмем Ctrl + V. Не паникуем.
5. Переходим на вкладку "Данные", опция "Текст по столбцам".
6. В появившемся окне выбираем формат данных "с разделителями", жмем "Далее".
7. Символом-разделителем выбираем запятую, сверяемся с образцом в нижней части окна. Если все выглядит нормально - жмем "Готово".
8. Поздравляем себя с завершением этого этапа подготовки данных:
![!good2](https://github.com/user-attachments/assets/59688acc-a766-493f-8d77-ad96c47b7b26)

9. Сохраните получившийся файл с названием **ProductsImport.xlsx**

## 2. Создание чистых файлов

Изучите схему БД, представленную ниже:

![schema](https://github.com/user-attachments/assets/c026b928-6b76-4ce5-a611-d127853c68ae)

В реузльтате выполнения этого этапа у вас должно получиться **11 файлов, названия которых соответствуют названиям таблиц в формате [имя таблицы]Ready.xlsx**

Если вы уже посчитали количество таблиц, то у вас возникнет вопрос - почему файлов должно быть 11, если всего таблиц 14?
Ответ очень простой - таблицы History содержат в себе историю операций с различными объектами. Так как мы только поднимаем проект, то никакой истории у нас быть не может.

Некоторые таблицы вам придется заполнить самостоятельно - это таблицы Supplier, Shop, Material и MaterialType. Здесь нужно только убедиться, что в ячейках xlsx-файла находятся соответсвующие полям таблицы типы данных, т.е. в ячейках ID не должно быть текста - только числовые значения. Смысловое качество заполнения зависит исключительно от вашей совести - оригинальные авторы сего проекта продают мягко-твердые игрушки из плутония.

### 2.1 Очистка входных данных

Нам повезло - бардак есть только в файле agents_k_import.csv, причем бардак относительно опрятный. Нас интересуют столбцы "Электронная почта агента", "Телефон агента" и "Приоритет".

1. Осмотрите столбец "Электронная почта агента". Как можно заметить, некоторые агенты предоставили нам свои ящики с префиксом "email: ". Его нужно удалить.
2. Для этого выберите весь столбец и нажмите Ctrl + F. В открывшемся окне переключитесь на вкладку "Заменить". В поле "Найти:" введите "email: ". Поле "Заменить на:" оставьте пустым.
3. Нажмите "Заменить все". Еще раз осмотрите столбец и убедитесь, что все адреса электронной почты теперь приведены к единому виду.
4. Проделайте аналогичные операции со столбцами "Телефон агента" и "Приоритет". В столбце "Телефон" должны остаться только допустимые в телефонных номерах символы, в столбце "Приоритет" - только цифры.

### 2.2 Созадние файлов с данными для таблиц

Общие рекомендации:
- Всегда сначала копируйте входные данные на другой лист, прежде чем проводить с ними какие-либо махинации.
- Определитесь с начальным значением ID, с которого будет начинаться нумерация позиций в каждой таблице ( т.е. 0, 1, 2 и т.д. / 10, 11, 12 и т.д. / 100, 101, 102 и т.д.).
- В полях image может содержаться ссылка на любое изображение, однако нужно учитывать заданный в схеме БД максимальный размер поля.
- ***Дальнейшие инструкции подразумевают, что файлы SupplierReady, ShopReady, MaterialReady и MaterialTypeReady вами уже созданы***.

**AgentTypeReady**
1. Создайте новый xlsx-файл с соответствующим названием и задайте заголовки столбцов.
2. Скопируйте столбец "Тип агента" файла agents_k_import в столбец "Title".
3. Выделите скопированный столбец и перейдите на вкладку "Данные"
4. Удалите дубликаты, воспользовавшись соответсвующей опцией в разделе "Работа с данными" верхней панели.
5. Назначьте ID каждой позиции в таблице.

**AgentReady**
1. Создайте новый xlsx-файл с соответствующим названием и задайте заголовки столбцов.
2. Скопируйте столбцы из файла agents_k_import в соответсвующие столбцы файла AgentReady.
3. Назначьте ID каждой позиции в таблице.

В столбце "AgentTypeID" пока что действительно должны находиться буквенные названия типа агента. Это будет исправлено позднее.

**MaterialSupplerReady**
1. Создайте новый xlsx-файл с соответствующим названием и задайте заголовки столбцов.
2. Сопоставьте ID материалов из файла MaterialReady c ID поставщиков из файла SupplierReady. Сопоставления могут быть произвольными.

**ProductTypeReady**
1. Создайте новый xlsx-файл с соответствующим названием и задайте заголовки столбцов.
2. Скопируйте столбец "Тип продукции" файла ProductsImport в столбец "Title".
3. Выделите скопированный столбец и перейдите на вкладку "Данные"
4. Удалите дубликаты, воспользовавшись соответсвующей опцией в разделе "Работа с данными" верхней панели.
5. Назначьте ID каждой позиции в таблице.
6. В столбце "DefectedPercent" укажите произвольные числовые значения, определяющие процент брака для каждого вида материала

**ProductReady**
1. Создайте новый xlsx-файл с соответствующим названием и задайте заголовки столбцов.
2. Скопируйте столбцы из файла ProductsImport в соответсвующие столбцы файла ProductReady
3. Назначьте ID каждой позиции в таблице.

Аналогично AgentReady, в столбце "ProductTypeID" пока что оставьте текст.

**ProductMaterialReady**
1. Создайте новый xlsx-файл с соответствующим названием и задайте заголовки столбцов.
2. Сопоставьте ID материалов из файла MaterialReady c ID продуктов из файла ProductReady. Сопоставления могут быть произвольными.

**ProductSaleReady**
Здесь придется немного повозиться.

1. Создайте новый xlsx-файл с соответствующим названием и задайте заголовки столбцов.
2. В столбцы SaleDate и ProductCount скопируйте соответсвующие столбцы из файла productsale_k_import.
3. Создайте новый лист. Скопируйте на него данные из файла productsale_k_import (кроме даты и количества) строго в том же порядке, в каком они указаны в файле. Должно получиться примерно следующее:
![!psale1](https://github.com/user-attachments/assets/a954dd14-0e33-4932-84a7-905284e4ede5)

4. Откройте файл AgentReady и скопируйте из него столбцы ID и Title:
![!psale2](https://github.com/user-attachments/assets/3577e2cc-d64e-48ab-8fb4-f642142de104)

5. Выделите ячейку B2. Вставьте в неё следующую формулу:
```
   =ВПР(A2;$D$2:$E$101;2;ЛОЖЬ)
```
6. Распространите формулу до ячейки B101. Должно получиться примерно так:
![!psale3](https://github.com/user-attachments/assets/0c0bef68-edb3-453b-98e8-6a5d947e9854)

7. Откройте файл ProductReady и скопируйте из него столбы ID  и Title:
![!psale4](https://github.com/user-attachments/assets/6cda158b-14bd-4089-b52e-c9a14c30a8a2)

9. Выделите ячейку H2. Вставьте в неё следующую формулу:
```
   =ВПР(G2;$J$2:$K$51;2;ЛОЖЬ)
```
9. Распространите формулу до ячейки H101. Должно получиться примерно так:
![!psale5](https://github.com/user-attachments/assets/2e76ccdd-8a04-4358-a4f8-7159ce4cc2d1)

10. Скопируйте ячейки В2-В101 в столбец "AgentID" и ячейки H2-H101 в столбец "ProductID"
11. Назначьте ID каждой позиции в таблице.

### Готово. Вы великолепны.
   
## Доработка файлов

После получения всех файлов c чистыми данными (c окончанием Ready.xlsx) необходимо доработать некоторые из них.

В таблице "AgentReady" есть столбец "agentTypeId", в котором ожидается нахождение уникальных идентификаторов (чисел), а не названий, которые находятся сейчас.

Для решения данной проблемы сделайте следующее:
1. Создайте файл "Rename.xlsx";
2. Назовите лист в созданном файле "agentTypeId";
3. В ячейке A1 впишите "old" и, начиная с ячейки "A2", вставьте значения из таблицы "AgentTypeReady" из столбца "Title";
4. В ячейке B1 впишите "new" и, начиная с ячейки "A2", вставьте значения из таблицы "AgentTypeReady" из столбца "Id";
5. Откройте скрипт “rename.py” и измените значения следующих переменных:
   - Переменной “rename_path” присвойте значение полного пути расположения файла "Rename.xlsx";
   - Переменной “path” присвойте значение пути к файлу "AgentReady.xlsx" (без самого названия файла);
   - Переменной “file” присвойте значение "AgentReady.xlsx";
   - Переменной “sheet” присвойте значение "agentTypeId";
   - Переменной “column_index” присвойте значение 2;
     
   Пример содержимого скрипта:
   
```
rename_path = 'D:\\data\\rename.xlsx'
path = 'D:\\data\\'
file = 'AgentReady.xlsx'
sheet = 'Sheet1'
column_index = 2
```

6. Выполните скрипт.

После выполнения скрипта в папке с файлом "AgentReady.xlsx" появится новый файл "update_AgentReady.xlsx" с корректным содержимым столбца "agentTypeId".

Далее выполните аналогичный алгоритм для файла "ProductReady" (переменной “column_index” присвоить значение 2) без создания нового файла "Rename.xlsx", а добавления в него нового листа "ProductTypeID".

 ### Примечание: аналогичного результата можно добиться с помощью поэтапной замены значений в файлах ("ctrl + H") или с помощью регулярных выражений для замен.

## Создание SQL-скриптов

После получения доработанных файлов можно приступать к созданию sql-запросов на их основе.

Для создания sql-запросов сделайте следующее:
1. Откройте скрипт “excel_to_sql.py” и измените значения следующих переменных:
   - Переменной “excel_folder” присвойте значение расположения папки, в которой хранятся все файлы с данными для базы данных;
   - Перменной “dict” присвойте списком значения названий всех файлов с данными, в формате {‘название_файла_xlsx’: {‘table’: ‘название_таблицы_в_бд’, ‘sheet’: ‘название_листа_файла_xlsx’}, …};
Итоговое значение переменной может выглядить следующим образом:
```
dict = {
   'update_AgentReady.xlsx': {'table': 'Agent', 'sheet': 'AgentReady'},
   'AgentTypeReady.xlsx': {'table': 'AgentType', 'sheet': 'Лист1'},
   'MaterialReady.xlsx': {'table': 'Material', 'sheet': 'Лист1'},
   'MaterialSupplier.xlsx': {'table': 'MaterialSupplier', 'sheet': 'MaterialSupplier'},
   'MaterialTypeReady.xlsx': {'table': 'MaterialType', 'sheet': 'Лист1'},
   'ProductMaterial.xlsx': {'table': 'ProductMaterial', 'sheet': 'Лист1'},
   'update_ProductReady.xlsx': {'table': 'Product', 'sheet': 'ProductReady'},
   'ProductSaleReady.xlsx': {'table': 'ProductSale', 'sheet': 'Лист1'},
   'ProductTypeReady.xlsx': {'table': 'ProductType', 'sheet': 'ProductTypeReady'},
   'ShopReady.xlsx': {'table': 'Shop', 'sheet': 'ShopReady'},
   'SupplierReady.xlsx': {'table': 'Supplier', 'sheet': 'Лист1'}
}
```
3. Запустите скрипт.
   
После выполнения скрипта в указанной в переменной папке появится несколько файлов типа "название_таблицы_inserts.sql".

## Импорт данных в БД

После создания всех sql-запросов, их необходимо выполнить.

Для выполнения запросов в базу данных будет использоваться ‘DBeaver’, который необходимо скачать, установить и запустить.

После запуска ‘DBeaver’, сделайте следующее:
1. Выполните подключение к развернутой базе данных с уже созданныеми таблицами;
2. В панели инструментов выберите "Редактор SQL" -> "Загрузить SQL скрпит" -> Выбрать файл "*_insert.sql";
3. Выполните загруженный SQL скрипт.
После выполнения скрипта в базе данных добавятся все значения в конкретной таблице.

Для выгрузки всех данных необходимо аналогичным образом выполнить все созданные SQL скрипты.

### Важно!
Из-за существования связей между таблицами некоторые данные не получится выгрузить, до выгрузки других, поэтому рекомендуется выполнять SQL скрипты в следующем порядке:
1. MaterialType
2. ProductType
3. AgentType
4. Agent
5. Shop
6. Supplier
7. Material
8. MaterialSupplier
9. ProductSale
10. Product
11. ProductMaterial


# Подробная документация по API

## 1. /agents

### GET /agents

**Описание:**  
Возвращает список всех агентов с дополнительной информацией.

**Параметры:**  
Нет.

**Возвращаемые данные:**  
Массив объектов агентов, каждый из которых содержит следующие поля:

- **ID** (int): Уникальный идентификатор агента.
- **Title** (string): Название агента.
- **AgentTypeID** (int): Идентификатор типа агента.
- **Address** (string): Адрес агента.
- **INN** (string): ИНН агента.
- **KPP** (string): КПП агента.
- **DirectorName** (string): Имя директора.
- **Phone** (string): Телефонный номер агента.
- **Email** (string): Электронная почта агента.
- **Logo** (string): Имя файла логотипа (не полный путь).
- **Priority** (int): Приоритет агента.
- **AgentType** (string): Название типа агента.
- **SalesCount** (int): Количество продаж, совершенных агентом.
- **TotalSales** (float): Общая сумма продаж.
- **Discount** (int): Размер скидки, основанный на общей сумме продаж.

**Примеры ответов:**

- **Успех:**  
  Возвращает массив агентов с перечисленными выше полями.

- **Ошибка:**  
  404, если агенты не найдены.

---

### GET /agents/{id}

**Описание:**  
Возвращает детальную информацию об агенте по указанному `id`.

**Параметры:**

- **id** (в URL): Идентификатор агента для получения детальной информации.

**Возвращаемые данные:**  
Объект с информацией об агенте, содержащий следующие поля:

- **ID** (int): Уникальный идентификатор агента.
- **Title** (string): Название агента.
- **AgentTypeID** (int): Идентификатор типа агента.
- **Address** (string): Адрес агента.
- **INN** (string): ИНН агента.
- **KPP** (string): КПП агента.
- **DirectorName** (string): Имя директора.
- **Phone** (string): Телефонный номер агента.
- **Email** (string): Электронная почта агента.
- **Logo** (string): Имя файла логотипа (не полный путь).
- **Priority** (int): Приоритет агента.
- **SalesCount** (int): Количество продаж.
- **TotalSales** (float): Общая сумма продаж.
- **Discount** (int): Скидка в процентах.

**Примеры ответов:**

- **Успех:**  
  Возвращает объект агента с перечисленными выше полями.

- **Ошибка:**  
  404, если агент не найден.

---

### POST /agents

**Описание:**  
Создает нового агента.

**Тело запроса:**  
JSON-объект, содержащий следующие **обязательные** поля:

- **name** (string): Название агента.
- **agent_type** (int): ID типа агента.
- **phone** (string): Телефонный номер.
- **priority** (int): Приоритет агента.
- **inn** (string): ИНН агента.

**Необязательные поля:**

- **address** (string): Адрес агента.
- **kpp** (string): КПП агента.
- **director_name** (string): Имя директора.
- **email** (string): Электронная почта.
- **logo** (string): Имя файла логотипа (не полный путь).

**Примеры ответов:**

- **Успех:**

  ```json
  {
    "success": true,
    "agent_id": <новый_ID_агента>
  }
  ```

- **Ошибка:**  
  400, если отсутствуют обязательные поля.

---

### PUT /agents/{id}

**Описание:**  
Обновляет информацию об агенте по указанному `id`.

**Параметры:**

- **id** (в URL): Идентификатор агента.

**Тело запроса:**  
JSON-объект, содержащий любые из следующих полей:

- **name** (string): Название агента.
- **agent_type** (int): ID типа агента.
- **address** (string): Адрес агента.
- **inn** (string): ИНН агента.
- **kpp** (string): КПП агента.
- **director_name** (string): Имя директора.
- **phone** (string): Телефонный номер.
- **email** (string): Электронная почта.
- **logo** (string): Имя файла логотипа (не полный путь).
- **priority** (int): Приоритет агента.

**Примеры ответов:**

- **Успех:**

  ```json
  {
    "success": true
  }
  ```

- **Ошибка:**  
  400, если не передано ни одно поле для обновления.

---

### DELETE /agents/{id}

**Описание:**  
Удаляет агента по указанному `id`.

**Параметры:**

- **id** (в URL): Идентификатор агента.

**Примеры ответов:**

- **Успех:**

  ```json
  {
    "success": true
  }
  ```

- **Ошибка:**  
  403, если у агента есть история продаж.

---

### POST /agents/priority

**Описание:**  
Обновляет приоритет для нескольких агентов одновременно.

**Тело запроса:**  
JSON-объект с **обязательными** полями:

- **agentIds** (array of int): Массив ID агентов для обновления приоритета.
- **newPriority** (int): Новый уровень приоритета.

**Примеры ответов:**

- **Успех:**

  ```json
  {
    "success": true
  }
  ```

- **Ошибка:**  
  400, если отсутствуют обязательные параметры.

---

## 2. /agent-types

### GET /agent-types

**Описание:**  
Возвращает список доступных типов агентов.

**Параметры:**  
Нет.

**Возвращаемые данные:**  
Массив объектов с полями:

- **ID** (int): Идентификатор типа агента.
- **Title** (string): Название типа агента.

---

## 3. /agents/{agent_id}/sales

### GET /agents/{agent_id}/sales

**Описание:**  
Возвращает историю продаж для указанного агента.

**Параметры:**

- **agent_id** (в URL): Идентификатор агента.

**Возвращаемые данные:**  
Список продаж агента, каждый элемент включает:

- **SaleDate** (string): Дата продажи.
- **Product** (string): Название продукта.
- **ProductCount** (int): Количество проданных единиц.

**Примеры ответов:**

- **Успех:**  
  Массив объектов с историей продаж.

- **Ошибка:**  
  404, если продажи не найдены.

---

## 4. /sales

### POST /sales

**Описание:**  
Добавляет новую запись о продаже.

**Тело запроса:**  
JSON-объект, содержащий **обязательные** поля:

- **agent_id** (int): ID агента.
- **product_id** (int): ID продукта.
- **product_count** (int): Количество проданных продуктов.
- **sale_date** (string, опционально): Дата продажи (если не указана, используется текущая дата).

**Примеры ответов:**

- **Успех:**

  ```json
  {
    "success": true
  }
  ```

- **Ошибка:**  
  400, если отсутствуют обязательные поля.

---

### DELETE /sales/{id}

**Описание:**  
Удаляет запись о продаже по указанному `id`.

**Параметры:**

- **id** (в URL): Идентификатор продажи.

**Примеры ответов:**

- **Успех:**

  ```json
  {
    "success": true
  }
  ```

---

## 5. /products

### GET /products

**Описание:**  
Возвращает список всех продуктов.

**Параметры:**  
Нет.

**Возвращаемые данные:**  
Массив объектов продуктов с полями:

- **ID** (int): Идентификатор продукта.
- **Title** (string): Название продукта.

---
