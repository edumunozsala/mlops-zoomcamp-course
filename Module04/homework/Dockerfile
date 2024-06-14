FROM agrigorev/zoomcamp-model:mlops-2024-3.10.13-slim

ENV PROJECT_DIR /app

RUN python -m pip install --upgrade pip
RUN pip install pipenv

WORKDIR ${PROJECT_DIR}
RUN mkdir output
COPY Pipfile Pipfile.lock starter.py ${PROJECT_DIR}/
RUN pipenv install --system --deploy

ENV PATH="/.venv/bin:$PATH"

ENTRYPOINT ["python", "-m", "starter"]
CMD ["-y", "2023","-m", "5"]
