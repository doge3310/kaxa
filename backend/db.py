from peewee import Model, CharField, DateTimeField, MySQLDatabase, AutoField, ForeignKeyField
import pymysql

from hasher import hash_password


password = "1234_8765"
user = "root"
host = "127.0.0.1"
port = 3306
database = "kaxa"

connect = pymysql.connect(user=user, host=host, password=password)
db_connect = MySQLDatabase(database=database,
                           user=user,
                           host=host,
                           port=port,
                           password=password)


class Table(Model):
    class Meta:
        database = db_connect


class User(Table):
    id = AutoField()
    name = CharField()
    password = CharField()


class Message(Table):
    id = AutoField()
    text = CharField()
    time = DateTimeField()
    from_user = ForeignKeyField(User)
    to_user = ForeignKeyField(User)


def main():
    user1 = User.get_or_create(
        name="user1",
        password=hash_password("123")
    )

    user2 = User.get_or_create(
        name="user2",
        password=hash_password("123")
    )

    message = Message.get_or_create(
        text="dfghdfghdfgh",
        time="2026.02.12 12:23:56",
        from_user=1,
        to_user=2
    )


if __name__ == "__main__":
    db_connect.create_tables([
        User,
        Message
    ])

    main()
