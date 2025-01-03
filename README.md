Run everything
```commandline
docker-compose up
```

Run tests

```commandline
docker-compose run app pytest
```

See docker image commands in `entrypoint.sh`


Make migrations

```commandline
docker-compose run app alembic revision --autogenerate -m "01_initial_migration"
```

Apply migrations

```commandline
docker-compose run app alembic upgrade head
```


Config for vscode:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Payment service debug",
            "type": "debugpy",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "app.main:app",
                "--reload",
                "--host",
                "0.0.0.0",
                "--port",
                "8000",
            ],
            "envFile": "${workspaceFolder}/.env"
        }
    ]
}
```
