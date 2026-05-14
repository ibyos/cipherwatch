# DomainSentry — Brand Protection SaaS

## Опис продукту
Сервіс моніторингу брендів в інтернеті. Автоматично знаходить:
- Typosquatting домени (похожі на ваш бренд)
- Домени які використовують ваш товарний знак
- Нових конкурентів які клонують ваш бренд
- Фейкові соціальні сторінки

## Модель монетизації
- Free: 1 домен, 1 перевірка на день
- Pro ($9.99/mo): 10 доменів, щоденні сканування, alerts
- Business ($29.99/mo): 50 доменів, API доступ, пріоритетна підтримка

## MVP Stack
- Backend: Python (FastAPI)
- Frontend: HTML/CSS/JS (static, deployable)
- Database: SQLite (для MVP)
- Notifications: Email + Webhook
- Deployment: Self-hosted або cloud

## Revenue Target
- 100 клієнтів Pro → $999/mo → ~$12k/рік
- 20 клієнтів Business → $580/mo
- Launch: 6 місяців до $5k/mo

## Конкуренти
- DomainTools (дорого)
- WhoisXML API (технічний)
- Комбайни без моніторингу реального часу

## Unique Value Proposition
Простий, дешевий, автоматизований моніторинг для малих бізнесів які не можуть собі дозволити Enterprise рішення.

## Перші кроки MVP
1. [x] Концепт та бізнес-план
2. [ ] Сканер typosquatting (Python)
3. [ ] Веб-інтерфейс
4. [ ] Система alerts
5. [ ] Лендінг сторінка
6. [ ] Деплой

---

## Roadmap v0.2

### 1. Whois Lookup
```python
import whois
w = whois.whois('g0ogle.com')
print(w.creation_date, w.registrar, w.name_servers)
```

### 2. Enhanced Scanner Features
- DNS A/AAAA/MX/NS records
- SSL certificate info
- GeoIP location
- Registrar info
- Age estimation (older = more legitimate)
- Suspiciousness score (0-100)

### 3. Marketing Strategy

**Target Audience:**
- Small business owners ($1k-$50k/mo revenue)
- E-commerce founders
- Ukrainian IT companies (patriotic angle + practical)
- Cybersecurity teams at SMBs

**Channels:**
- Product Hunt launch
- Indie Hackers
- Twitter/X — cybersecurity niche accounts
- Reddit r/entrepreneur, r/smallbusiness
- LinkedIn — brand protection posts
- Hacker News

**Positioning:**
"DomainSentry finds squatters, copycats and lookalike domains before they hurt your brand — without the $50k/year enterprise contract."

**Early Adopter Plan:**
- Free tier is generous — gets people in
- 50 free Pro accounts for first 50 signups
- Community beta program

**Monetization Timeline:**
- Month 1: MVP + landing page
- Month 2: Auth + email alerts
- Month 3: Telegram bot
- Month 4: API access + webhooks
- Month 6: 50 paying customers = $500/mo
- Month 12: 200 paying customers = $2k/mo

### 4. Competitive Analysis

| Feature | DomainSentry | DomainTools | WhoisXML |
|---------|-------------|-------------|----------|
| Price | $9.99/mo | $299/mo | pay-per-query |
| Real-time scan | ✅ | ❌ | ✅ |
| Telegram alerts | ✅ | ❌ | ❌ |
| API | Pro+ | Enterprise | ✅ |
| Simplicity | 10/10 | 3/10 | 5/10 |
