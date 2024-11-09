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
    except Exception as e:
        connection.rollback()
        print("Error:", e)

# DELETE
def delete_task(connection, id):
    try:
        delete_task_query = """
            DELETE FROM task WHERE id = %s
        """
        task = (id,)
        cursor = connection.cursor()

        cursor.execute(delete_task_query, task)
        connection.commit()
        print(f"Task ID {id} を削除しました")

    except Exception as e:
        connection.rollback()
        print("Error:", e)
    finally:
        cursor.close()


def update_task(connection, id, title=None, completed=None):
    try:
        update_parts = []
        params = []

        # UPDATE文のパーツを構築
        if title is not None:
            update_parts.append("title = %s")
            params.append(title)
        if completed is not None:
            update_parts.append("completed = %s")
            params.append(completed)

        # パラメータが空の場合は更新しない
        if not update_parts:
            print("更新するフィールドが指定されていません")
            return

        # SQL文の構築
        update_query = f"""
            UPDATE task 
            SET {', '.join(update_parts)}
            WHERE id = %s
        """

        # IDをパラメータに追加
        params.append(id)

        # クエリの実行
        cursor = connection.cursor()
        cursor.execute(update_query, tuple(params))
        connection.commit()

        # 更新の確認
        if cursor.rowcount > 0:
            print(f"Task ID {id} を更新しました")
        else:
            print(f"Task ID {id} は見つかりませんでした")

    except Exception as e:
        connection.rollback()
        print("Error:", e)
    finally:
        cursor.close()


def get_all_tasks(connection):
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM task")
        tasks = cursor.fetchall()
        for task in tasks:
            print(f"ID: {task['id']}, Title: {task['title']}, Completed: {task['completed']}")
        return tasks
    except Exception as e:
        print("Error:", e)
    finally:
        cursor.close()


if __name__ == '__main__':
    connection = connect_to_database()

    if connection:
        try:
            # 更新前のデータを表示
            print("更新前のタスク一覧:")
            get_all_tasks(connection)

            # タスクの更新
            id = 2
            new_title = "トイレ掃除をする"
            update_task(connection, id, title=new_title, completed=1)

            # 更新後のデータを表示
            print("\n更新後のタスク一覧:")
            get_all_tasks(connection)

        finally:
            connection.close()