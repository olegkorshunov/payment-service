from pydantic import PostgresDsn as PgDsn


class PostgresDsn(PgDsn):
    @property
    def raw_dsn(self) -> str:
        return f"{self.scheme}://{self.user}:{self.password}@{self.host}:{self.port}{self.path}"
