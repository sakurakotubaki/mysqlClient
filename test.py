import mysql.connector
from mysql.connector import errorcode


def connect_to_database():
    try:
        connection = mysql.connector.connect(
            user='jboy',
            password='1234qw',
            host='127.0.0.1',
            database='myapp',
            port=3306,
            # 認証プラグインを指定
            auth_plugin='mysql_native_password'
        )
        print("データベースに接続成功！")
        return connection
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("ユーザー名またはパスワードが間違っています")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("データベースが存在しません")
        else:
            print(f"エラー: {err}")
        return None


def create_table(connection):
    try:
        cursor = connection.cursor()  # connectionを使用

        # SQLの文法エラーを修正（最後のカンマを削除）
        create_table_query = """
        CREATE TABLE IF NOT EXISTS task (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT FALSE
        )
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("テーブル作成成功！")

    except Exception as e:
        connection.rollback()  # connectionを使用
        print(f"エラー: {e}")
    finally:
        cursor.close()

#  INSERT METHOD
def add_task(connection, title):
    try:
        add_task_query="""
    INSERT INTO task (title, completed) VALUES (%s, %s)    
    """
        task = (title, False)
        cursor = connection.cursor()
        cursor.execute(add_task_query, task)
        connection.commit()

if __name__ == '__main__':
    connection = connect_to_database()

    if connection:
        create_table(connection)
        connection.close()