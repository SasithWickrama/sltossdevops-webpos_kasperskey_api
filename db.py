from log import getLogger
import traceback
import cx_Oracle
import const

logger = getLogger('kasperskyapi', 'logs/kaspersky')


class DbConnection:
    def dbconn(self):
        try:
            dsn_tns = cx_Oracle.makedsn(const.hostname, const.port, service_name=const.service)
            conn = cx_Oracle.connect(user=const.user, password=const.password, dsn=dsn_tns)
            return conn
        except Exception as e:
            print("Exception : %s" % traceback.format_exc())
            logger.info("Exception : %s" % traceback.format_exc())
            return traceback.format_exc()