# GitHub Secrets Setup

Для автоматичного deploy потрібно додати секрети в GitHub:

## Railway
1. Зайди на https://github.com/ibyos/cipherwatch/settings/secrets/actions
2. "New repository secret":
   - `RAILWAY_TOKEN` — твій Railway API token
   - `RAILWAY_PROJECT_ID` — ID проекту з Railway

## Vercel (альтернатива)
1. https://vercel.com/account/tokens
2. Створи token → додай як `VERCEL_TOKEN`

## Railway Token отримання
Потрібно створити новий токен на railway.com
(Той що дав раніше — не працює, можливо для старого railway.app)
