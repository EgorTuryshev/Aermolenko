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
7. [Заключение](#заключение)
8. [Документация API](#📄-документация-api)

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

Доска с задачами находится [здесь](https://link-to-task-board). Выбирайте задачи по вкусу из файла задания, самостоятельно заносите их на доску, обновляйте статус и назначайте себя ответственным.

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

Подробная инструкция доступна [здесь](https://nvie.com/posts/a-successful-git-branching-model/).

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

Для пользователей Windows рекомендуется запускать проект в [WSL](https://docs.microsoft.com/ru-ru/windows/wsl/install). Это позволит работать в Linux-среде, сохраняя удобство Windows.

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

## Заключение

Вы успешно настроили и запустили проект!


# 📄 Документация API

## Базовый URL: `http://89.110.118.205/api`

## Структура ответа: Все ответы от API предоставляются в формате JSON.

## Статус коды:
- **200 OK**: Запрос выполнен успешно.
- **201 Created**: Ресурс успешно создан.
- **400 Bad Request**: Неверный запрос или некорректные данные.
- **404 Not Found**: Ресурс не найден.
- **500 Internal Server Error**: Внутренняя ошибка сервера.

---

## 📚 Методы API:

### 1. 📋 Получить всех агентов
***Описание:*** Возвращает список всех агентов.

**URL:** `GET /agents`

**Пример запроса:**  
`GET http://89.110.118.205/api/agents`

**Пример ответа:**
```json
[
  {
    "ID": 1,
    "Title": "Updated Agent",
    "AgentTypeID": 1,
    "Address": "ул. Ленина, д. 1",
    "INN": "1234567890",
    "KPP": "987654321",
    "DirectorName": "Иван Иванов",
    "Phone": "+79991234567",
    "Email": "OLOLOLOLOLOL@.ru",
    "Logo": null,
    "Priority": 5,
    "AgentType": "Оптовый",
    "SalesCount": "67",
    "TotalSales": "10000.00",
    "Discount": 5
  },
  {
    "ID": 2,
    "Title": "Агент Смирнов",
    "AgentTypeID": 2,
    "Address": "ул. Пушкина, д. 5",
    "INN": "2345678901",
    "KPP": "876543210",
    "DirectorName": "Ольга Смирнова",
    "Phone": "+79991234568",
    "Email": "smirnov@example.com",
    "Logo": null,
    "Priority": 5,
    "AgentType": "Розничный",
    "SalesCount": "108",
    "TotalSales": "3550.00",
    "Discount": 0
  }
]
```

---

### 2. 🛠 Создать агента
***Описание:*** Создает нового агента с указанными параметрами.

**URL:** `POST /agents`

**Тело запроса (JSON):**
- `name` _(string)_: имя агента.
- `agent_type` _(integer)_: тип агента (ID).
- `address` _(string)_: адрес агента.
- `inn` _(string)_: ИНН.
- `kpp` _(string)_: КПП.
- `director_name` _(string)_: имя директора.
- `phone` _(string)_: телефон агента.
- `email` _(string)_: email агента.
- `logo` _(string)_: URL логотипа агента.
- `priority` _(integer)_: приоритет агента.

**Пример запроса:**
```json
{
  "name": "Example Agent",
  "agent_type": 1,
  "address": "1234 Main St, City, Country",
  "inn": "1234567890",
  "kpp": "123456789",
  "director_name": "John Doe",
  "phone": "+79991234567",
  "email": "example@agent.com",
  "logo": "http://example.com/logo.png",
  "priority": 5
}
```

**Пример ответа:**
```json
{
  "success": true,
  "id": 5
}
```

---

### 3. 🔍 Получить агента по ID
***Описание:*** Возвращает информацию о конкретном агенте по его ID.

**URL:** `GET /agents/{id}`

**Параметры:**
- `id` _(integer)_: Идентификатор агента.

**Пример запроса:**  
`GET http://89.110.118.205/api/agents/2`

**Пример ответа:**
```json
{
  "ID": 4,
  "Title": "Агент Петрова",
  "AgentTypeID": 2,
  "Address": "ул. Гагарина, д. 12",
  "INN": "4567890123",
  "KPP": "654321098",
  "DirectorName": "Петр Петров",
  "Phone": "+79991234570",
  "Email": "petrov@example.com",
  "Logo": null,
  "Priority": 100,
  "SalesCount": "710",
  "TotalSales": "582975.00",
  "Discount": 25
}
```

---

### 4. 🔄 Обновить агента по ID
***Описание:*** Обновляет информацию о конкретном агенте.

**URL:** `PUT /agents/{id}`

**Параметры:**
- `id` _(integer)_: Идентификатор агента.

**Тело запроса (JSON):**
- Параметры для обновления, например `name`, `email`.

**Пример запроса:**
```json
{
  "name": "Updated Agent",
  "email": "OLOLOLOLOLOL@.ru"
}
```

**Пример ответа:**
```json
{
  "success": true
}
```

---

### 5. ❌ Удалить агента по ID
***Описание:*** Удаляет агента по его ID.

**URL:** `DELETE /agents/{id}`

**Параметры:**
- `id` _(integer)_: Идентификатор агента.

**Пример запроса:**  
`DELETE http://89.110.118.205/api/agents/1`

**Пример ответа:**
```json
{
  "success": true
}
```

---

### 6. 📝 Обновить приоритет агентов
***Описание:*** Обновляет приоритет для нескольких агентов.

**URL:** `POST /agents/priority`

**Тело запроса (JSON):**
- `agentIds` _(array of integers)_: список идентификаторов агентов.
- `newPriority` _(integer)_: новое значение приоритета.

**Пример запроса:**
```json
{
  "agentIds": [1, 2, 3, 4, 5],
  "newPriority": 5
}
```

**Пример ответа:**
```json
{
  "success": true
}
```

---

### 7. 🗂 Получить все типы агентов
***Описание:*** Возвращает список всех возможных типов агентов.

**URL:** `GET /agent-types`

**Пример запроса:**  
`GET http://89.110.118.205/api/agent-types`

**Пример ответа:**
```json
[
  {
    "ID": 1,
    "Title": "Оптовый"
  },
  {
    "ID": 2,
    "Title": "Розничный"
  }
]
```

---

### 8. 📈 Получить историю продаж агента
***Описание:*** Возвращает список всех продаж, совершенных агентом.

**URL:** `GET /agents/{agent_id}/sales`

**Параметры:**
- `agent_id` _(integer)_: Идентификатор агента.

**Пример запроса:**  
`GET http://89.110.118.205/api/agents/1/sales`

**Пример ответа:**
```json
[
  {
    "SaleDate": "2023-01-15",
    "ProductCount": 10,
    "Product": "Ноутбук"
  },
  {
    "SaleDate": "2023-02-10",
    "ProductCount": 50,
    "Product": "Тетрадь"
  }
]
```

---

### 9. 🛒 Создать продажу
***Описание:*** Регистрирует новую продажу для агента.

**URL:** `POST /sales`

**Тело запроса (JSON):**
- `agent_id` _(integer)_: Идентификатор агента.
- `product_id` _(integer)_: Идентификатор продукта.
- `product_count` _(integer)_: Количество проданного товара.

**Пример запроса:**
```json
{
  "agent_id": 1,
  "product_id": 1,
  "product_count": 5
}
```

**Пример ответа:**
```json
{
  "success": true
}
```

---

### 10. ❌ Удалить продажу
***Описание:*** Удаляет запись о продаже по её ID.

**URL:** `DELETE /sales/{id}`

**Параметры:**
- `id` _(integer)_: Идентификатор продажи.

**Пример запроса:**  
`DELETE http://89.110.118.205/api/sales/19`

**Пример ответа:**
```json
{
  "success": true
}
```

---

### 11. 🛒 Получить все продукты
***Описание:*** Возвращает список всех продуктов.

**URL:** `GET /products`

**Пример запроса:**  
`GET http://89.110.118.205/api/products`

**Пример ответа:**
```json
[
  {
    "ID": 1,
    "Title": "Ноутбук",
  },
  {
    "ID": 2,
    "Title": "Тетрадь",
  }
]
```

---