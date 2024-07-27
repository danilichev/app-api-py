# app-api-py

### Overview

This is a FastAPI-based application designed to be a quick start for new projects. This project aims to streamline the development process by offering a ready-to-use template that can be easily extended and customized to meet specific requirements.

Based on great project [fastapi-sqlalchemy-asyncpg](https://github.com/grillazz/fastapi-sqlalchemy-asyncpg) but it is tailored for ML-related applications.

Uses [MiVolo](https://github.com/WildChlamydia/MiVOLO) model for age estimation endpoint, checkpoints avalilble [here](https://drive.google.com/file/d/1LtDfAJrWrw-QA9U5IuC3_JImbvAQhrJE/view).

### Make commands

```shell
# start local development
make setup
# build project
make docker-build
# apply db migrations
make docker-apply-db-migrations
# run project in docker
make docker-up
```

### Citations

```
@article{mivolo2024,
   Author = {Maksim Kuprashevich and Grigorii Alekseenko and Irina Tolstykh},
   Title = {Beyond Specialization: Assessing the Capabilities of MLLMs in Age and Gender Estimation},
   Year = {2024},
   Eprint = {arXiv:2403.02302},
}
```
