# pull official base image
FROM python:slim


# set work directory
WORKDIR /dashboard


# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# EXPOSE 9000

COPY . /dashboard


# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "9000"]
