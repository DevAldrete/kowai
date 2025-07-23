# KowAI Backend - Docker Quick Start

This Docker Compose setup provides a complete development and deployment environment for the KowAI backend.

## Quick Start

1. **Copy environment template**:
   ```bash
   cp .env.docker .env
   ```

2. **Edit `.env` file** and add your API keys:
   - `OPENAI_API_KEY` - Get from [OpenAI Platform](https://platform.openai.com/api-keys)
   - `ANTHROPIC_API_KEY` - Get from [Anthropic Console](https://console.anthropic.com/)
   - `APPWRITE_*` - Get from your [Appwrite Console](https://cloud.appwrite.io/)
   - `SECRET_KEY` - Generate with: `openssl rand -hex 32`

3. **Start all services**:
   ```bash
   docker-compose up -d
   ```

4. **Verify deployment**:
   ```bash
   curl http://localhost:8000/health
   ```

## Services

- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **MariaDB**: localhost:3306
- **Redis**: localhost:6379  
- **Prefect UI**: http://localhost:4200

## Development Commands

```bash
# View logs
docker-compose logs -f kowai-backend

# Restart backend only
docker-compose restart kowai-backend

# Stop all services
docker-compose down

# Rebuild and restart
docker-compose up --build -d

# Access database
docker-compose exec mariadb mysql -u kowai_user -p kowai

# Access Redis CLI
docker-compose exec redis redis-cli
```

## Production Deployment

For production:
1. Set `DEBUG=false` in `.env`
2. Use a strong `SECRET_KEY`
3. Remove the volume mount in `docker-compose.yml`:
   ```yaml
   # volumes:
   #   - ./app:/app/app:ro
   ```
4. Use proper secrets management instead of `.env` files

## Troubleshooting

- **Database connection issues**: Wait for MariaDB to fully initialize (30-60 seconds)
- **API key errors**: Ensure all required keys are set in `.env`
- **Permission errors**: Run `docker-compose down -v` to reset volumes