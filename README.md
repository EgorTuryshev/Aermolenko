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
7. [Документация API](#подробная-документация-по-api)

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