#!/bin/bash

# Amazon Linux 패키지 업데이트
sudo yum update -y

# Python3 및 pip 설치
sudo yum install -y python3 python3-pip

# 필요한 라이브러리 설치
sudo pip3 install Flask boto3 matplotlib pandas requests

# AWS ACCESS KEY 환경변수 설정
echo "export AWS_ACCESS_KEY_ID='AWS_ACCESS_KEY_ID'" >> ~/.bashrc
echo "export AWS_SECRET_ACCESS_KEY='AWS_SECRET_ACCESS_KEY'" >> ~/.bashrc
source ~/.bashrc

# Flask 앱 실행
python3 app.py

