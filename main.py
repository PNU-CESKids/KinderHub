import psycopg2

if __name__=='__main__':
    con = psycopg2.connect(
        database='termkk',
        user='db2023',
        password='db!2023',
        host='::1',
        port='5432'
    )

    conn = con.cursor()


    conn.execute('select * from Student')
    result = conn.fetchall()
    
    print(result)