from mkpipe.spark import JdbcExtractor

JAR_PACKAGES = ['com.mysql:mysql-connector-j:9.1.0']


class MysqlExtractor(JdbcExtractor, variant='mysql'):
    driver_name = 'mysql'
    driver_jdbc = 'com.mysql.cj.jdbc.Driver'

    def build_jdbc_url(self):
        return (
            f'jdbc:{self.driver_name}://{self.host}:{self.port}/{self.database}'
            f'?user={self.username}&password={self.password}'
        )
