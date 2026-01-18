# tPDwH23qCF-rest-api

# Pre-requisites

1. Having UV installed - https://docs.astral.sh/uv/getting-started/installation/
2. Python 3.13 installed via uv, if not, install it by running `uv python install 3.13`

# How to run
1. run `uv sync` command
2. Activate environment with `source .venv/bin/activate`
3. Execute command `fastapi run`
4. Head into http://0.0.0.0:8000/docs for a detailed explanation of each endpoint.

# Assumptions
- Aggregation is implemented per sensor. Changing to a global aggregation across all sensors is straightforward by adjusting the query logic.
- Each metric value is recorded as a separate row in the metrics table.
- The description wasn't very clear on any default values for the metrics and statistic, so it is required to pass at least one value to this query params.
- Metric values are expected to be numeric.
- No logging/observability is implemented in this exercise.
- Using sqllite for simplicity.

# Suggestions
- FastAPI supports async; this project intentionally uses synchronous endpoints for simplicity and easier testing. Async can be added later if performance/scalability requires it.
- See docs/app_design.png for a proposed AWS architecture focused on scalability, security, performance and reliability.
- Use database migrations like Alembic and connection pooling in a production deployment.
- Add authentication.




# diagram of the present design and aws design

