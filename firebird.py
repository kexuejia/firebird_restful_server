class firebird():

    def __init__(self, db, user='SYSDBA',password= 'masterkey',charset='WIN1251', sql_dialect =3, fb_library_name=None):
        import fdb

        # con = fdb.connect(dsn=db, user='CASH', password='achs',charset = 'WIN1251',sql_dialect = 1, fb_library_name = fb_library_name)
        try:
            self.__fdb = fdb
            con = self.__fdb.connect(dsn=db, user=user, password=password ,charset = charset,sql_dialect = sql_dialect, fb_library_name = fb_library_name)
        except  Exception as e:
            print("Ошибка при открытии базы данных:\n"+str(e))
            raise Exception(e)
        self.__con = con
        self.__cursor = self.__con.cursor()

    def select(self, SELECT, params = ()):

        ex = self.__cursor.execute(SELECT,params)
        blobs = []
        for descriptor in ex.description:
            if self.is_blob(descriptor):
                blobs.append(descriptor[0])
                self.__cursor.set_stream_blob(descriptor[0])
                print (descriptor[0]+ ' is blob')
            else:
               print (descriptor[0]+ ' is not blob')

        DATA  = []
        import base64
        for row in self.__cursor.itermap():
            row = dict(row)

            for blob in blobs:
                if (row[blob] != None):
                    if row[blob].is_text:
                        row[blob] = row[blob].read()
                        row[blob] = row[blob].encode()
                    else:
                        row[blob] = row[blob].read()

                    if self.isBase64(row[blob]):
                        row[blob] = row[blob].decode()
                    else:

                        row[blob] = base64.b64encode(row[blob]).decode()

            DATA.append(row)

        self.__con.commit()
        self.__con.close()
        return DATA

    def execute(self, QUERY, params = ()):

        self.__cursor.execute(QUERY,params)
        self.__con.commit()
        return True

    def is_blob(self,descriptor):
        return (descriptor[self.__fdb.DESCRIPTION_DISPLAY_SIZE] == 0
            and descriptor[self.__fdb.DESCRIPTION_INTERNAL_SIZE] == 8)




    def isBase64(self, s):
        import base64
        try:
            return base64.b64encode(base64.b64decode(s)) == s
        except Exception:
            return False

