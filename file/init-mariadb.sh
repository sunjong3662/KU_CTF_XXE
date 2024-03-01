#!/bin/bash
# MariaDB 사용자 및 그룹 생성
groupadd -r mariadb
useradd -r -g mariadb mariadb

# MariaDB 데이터 디렉토리 및 설정 파일의 소유권 설정
chown -R mariadb:mariadb /var/lib/mysql
chown mariadb:mariadb /etc/my.cnf

# MariaDB 서버 초기화 및 안전한 설치 실행 (선택 사항)
mysql_install_db --user=mariadb
mysql_secure_installation
