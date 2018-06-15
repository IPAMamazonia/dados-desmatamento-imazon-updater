import psycopg2
from configs import DB_NAME, PW, HOST, USER, TABLE_NAME


class DB_Model:

    def __init__(self):
        self.con = psycopg2.connect(
            host=HOST, database=DB_NAME,user=USER, password=PW)
        self.cur = self.con.cursor()

    def calculate(self):
        print 'Calculando...'
        self.cur.execute('''
            INSERT INTO alerta_desmate_sad (id_ti, distance, area_ha, lat, lng, mes, ano, date)
(SELECT * FROM
    (
	 SELECT 
	   t.id as id_ti,
	   round((ST_Distance(ST_Transform(d.geom ,900913), ST_Transform(t.geom, 900913))/1000)::numeric, 2) as distance, -- Em Km
	   round((d.area*100)::numeric, 2) as area_ha,
	   round(ST_Y(ST_Centroid(d.geom))::numeric, 6) as lat,
	   round(ST_X(ST_Centroid(d.geom))::numeric, 6) as lng,
	   d.mes,
	   d.ano,
	   (ano || '-' || mes || '-15')::date
	 FROM 
	   terras_indigenas as t,
	   {} as d
	 --WHERE t.id = 4068
    ) AS foo
WHERE distance <= 10
ORDER BY distance)
        '''.format(TABLE_NAME))
        self.con.commit()
        print "Calculo concluido"

    def check_if_table_exists(self):

        self.cur.execute('''
        SELECT EXISTS (
   SELECT 1
   FROM   information_schema.tables 
   WHERE  table_schema = 'public'
   AND    table_name = '{}'
   );
'''.format(TABLE_NAME))

        exists = self.cur.fetchone()[0]

        return exists


    def drop_table(self):
        self.cur.execute('''
        DROP TABLE {};
        '''.format(TABLE_NAME))
        self.con.commit()
        print "Table dropada"
    def close_conn(self):
        self.con.close()

    # def select(self):
    #     self.cur.execute('select * from imazon_sad_desmatamento')
    #     print self.cur.fetchall()
    def database_calculate_and_drop_table(self):

        self.calculate()
        self.drop_table()
        self.close_conn()
# db = DB_Model()
# db.drop_table()
# db.close_conn()