## Backend

Deploy [backend/main.py](/Users/anupriyomandal/Documents/AI/x-app-sentiment/backend/main.py) to Railway as a Python service.

1. Set `OPENAI_API_KEY`
2. Set `DATABASE_URL`
3. Optional: set `REDIS_URL`
4. Start command:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

5. First deploy behavior:

```text
If the articles table is empty, the backend automatically runs an initial seed for up to 100 articles per brand.
```

6. Hourly Railway job:

Create a second Railway service or cron job in the same project with this command:

```bash
python -m backend.jobs.run_pipeline
```

Schedule it hourly in Railway's scheduler UI.

7. Monitoring ingestion progress:

Open this endpoint on your backend while a seed or cron job is running:

```bash
/pipeline-status
```

It returns brand-wise progress including `fetched`, `processed`, `added`, and overall run totals.

## Frontend

Deploy `frontend` to Vercel.

1. Set `NEXT_PUBLIC_API_BASE_URL` to your Railway backend URL
2. Build command:

```bash
npm run build
```

3. Output is handled by Next.js automatically

## Database

Run the SQL migration in [backend/migrations/001_initial_schema.sql](/Users/anupriyomandal/Documents/AI/x-app-sentiment/backend/migrations/001_initial_schema.sql) against PostgreSQL before first deploy.

## Preview Seeding

For a manual one-off ingest locally or on Railway shell:

```bash
python -m backend.jobs.run_pipeline
```
