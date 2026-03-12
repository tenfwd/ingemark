# Ingemark Test API

Mini FastAPI aplikacija.

## Start

Pokretanje pomoću DC:

```bash
docker compose -f docker-compose.yml up api
```

## Mini Testovi

Slično i kao API uz napomenu da koriste drugi PG kontejner.

```bash
docker compose -f docker-compose.yml -f docker-compose.test.yml up --abort-on-container-exit tests
```

## Obrazloženja

- FastAPI jer je jednostavan i brz za setupiranje.
- Korištenje Depends za fake provjeru Autha i fetchanje DB connectiona iz poola za svaki request.
- POST endpoint sam napravio da može hendlat jednu ili više poruka odjednom. Možda je overkill, ali mi se učinilo smisleno.
- Krenuo sam od pretpostavke da bi client uvijek slao Chat ID što sam shvatio kao nekakav postojeći Conversation/Message history (stoga je required). S druge strane, BE seta message ID u trenutku primanja poruke (zajedno sa timestampom).
- Nemam naviku koristiti ORM-ove osim ako nije eksplicitno zatraženo stoga pišem funkcije s AsyncPG-om i SQL-om.
- lifespan u main.py za ensuranje da je baza uspješno pokrenuta prije pokretanja api.
- Mali set e2e testova u zasebnom compose fileu.

## Primjeri

```bash
curl -X POST http://localhost:8000/messages/create \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer test-token-123" \
  -d '[
    {
      "chat_id": "123e4567-e89b-12d3-a456-426614174000",
      "content": "Hello, this is my first message",
      "role": "user",
      "rating": true
    },
    {
      "chat_id": "123e4567-e89b-12d3-a456-426614174000",
      "content": "This is a response from AI",
      "role": "ai",
      "rating": null
    }
  ]'
```

```bash
curl -X GET http://localhost:8000/messages \
  -H "Authorization: Bearer test-token-123"
```

```bash
curl -X PUT http://localhost:8000/messages/<message_id> \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer test-token-123" \
  -d '{
    "content": "Updated message content",
    "rating": false
  }'
```