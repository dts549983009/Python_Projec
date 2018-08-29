import re
import pymysql


db = pymysql.connect("localhost", "root", "123456")
cursor = db.cursor()
cursor.execute("create database dict;")
cursor.execute("use dict;")
cursor.execute("create table word(id int primary key auto_increment, word varchar(50) not null,\
 interpreter varchar(300) not null);")


def main():
    """匹配字典文本存储mysql"""
    with open('dict.txt') as f:
        content = f.read()
        regex = r"([a-zA-Z\.-]*'? ?[a-zA-Z\.-]* ?[a-zA-Z\.]*) +([A-Za-z0-9\.,&\?\*`\"\'\[\]\(\)!/\-;=+:<>~ ]*)"
        results = re.findall(regex, content)
        for i in results:
            cursor.execute('''insert into word(word, interpreter) values("%s", "%s")''' %
                           (i[0].strip().replace("'", "\'"), i[1].strip().replace("'", "\'")))
    db.commit()
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()

