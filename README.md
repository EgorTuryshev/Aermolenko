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