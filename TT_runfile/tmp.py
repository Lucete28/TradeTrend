import sys
my_variable = sys.argv[1]
print(my_variable)
print(sys.argv[0])


# 파일 경로
file_path = "/home/jhy/airflow-local/dags/TT/abc.txt"

# 파일 열기
with open(file_path, "w") as file:
    # 변수 값을 파일에 쓰기
    file.write(my_variable)