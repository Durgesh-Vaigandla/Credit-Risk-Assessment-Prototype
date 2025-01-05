
# Credit Risk Assessment API Documentation

## Base URL
```
https://api.creditrisk.example.com/v1
```

## Authentication
All API requests require an API key passed in the header:
```
Authorization: Bearer YOUR_API_KEY
```

## Endpoints

### 1. Get Credit Risk Score
```http
GET /risk-score/{user_id}
```

#### Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| user_id | string | Yes | Unique identifier for the user |

#### Response
```json
{
  "user_id": "12345",
  "risk_score": 85.5,
  "confidence": 0.92,
  "timestamp": "2025-01-05T10:30:00Z",
  "factors": [
    {
      "name": "payment_history",
      "impact": "positive",
      "weight": 0.35
    }
  ]
}
```

### 2. Submit Alternative Data
```http
POST /data/alternative
```

#### Request Body
```json
{
  "user_id": "12345",
  "data_type": "utility_bill",
  "provider": "gas_company",
  "payment_history": [
    {
      "date": "2024-12-01",
      "amount": 50.00,
      "status": "paid",
      "days_late": 0
    }
  ]
}
```

### 3. Update User Profile
```http
PUT /users/{user_id}
```

#### Request Body
```json
{
  "rental_agreement": {
    "monthly_rent": 1200,
    "start_date": "2024-01-01",
    "payment_history": []
  },
  "utility_providers": [
    {
      "type": "electricity",
      "provider_id": "ELEC123"
    }
  ]
}
```

## Rate Limits
- 100 requests per minute per API key
- 1000 requests per hour per API key

## Error Codes
| Code | Description |
|------|-------------|
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Resource Not Found |
| 429 | Too Many Requests |
