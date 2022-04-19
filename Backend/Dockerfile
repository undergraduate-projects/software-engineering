FROM python:3.8.5

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

COPY . /usr/src/app

# For Django
EXPOSE 80
CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]

