import sqlite3 

def sqlnames():
    db = sqlite3.connect(":memory:")
    cur = db.cursor()
    cur.execute("create table names(first text, last text)")
    cur.execute("create table nameswithemails(first text, last text, email text)")

    with open("names.csv") as names:
        headerline = True

        for name in names.readlines():
            if headerline:
                headerline = False
                continue

            sql = "insert into names values ('{}', '{}')".format(
                name.split(",")[0].strip(), name.split(",")[1].strip()
            )
            cur.execute(sql)

    with open("nameswithemails.csv") as nameswithemails:
        headerline = True
        for email in nameswithemails:
            if headerline:
                headerline = False
                continue
            sql = "insert into nameswithemails values ('{}', '{}', '{}')".format(
                email.split(",")[0].strip(),
                email.split(",")[1].strip(),
                email.split(",")[2].strip(),
            )
            cur.execute(sql)
    
    matchsql = '''
        select *
        from nameswithemails nwe where exists (
            select 1
            from names n 
            where lower(nwe.first) = lower(n.first)
                and lower(nwe.last) = lower(n.last)
        )
    '''
    cur.execute(matchsql)
    matches = cur.fetchall()
    for match in matches:
        print(match)


if __name__ == "__main__":
    # matchnames()
    sqlnames()