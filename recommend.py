import pandas as df
from django.db import connections
from django.core.exceptions import EmptyResultSet


def to_df(queryset, using=None, compiler=None):
    try:
        if type(queryset) == str:  # SQL이 문자열로 그대로 들어올 경우
            query = queryset
            params = None
        else:
            if using:  # 어떤 DB를 사용할지 지정한다면..
                con = connections[using]
            else:
                con = connections["default"]
            if compiler:  # 어떤 SQLCompiler를 사용할지 지정한다면..
                query, params = queryset.query.as_sql(compiler=compiler, connection=con)
            else:
                query, params = queryset.query.sql_with_params()
    except EmptyResultSet:  # 만약 쿼리셋의 결과가 비어있다면 빈 DataFrame 반환
        return pd.DataFrame()
    if using:  # 어떤 DB를 사용할지 지정했다면 해당 DB connection 이용
        df = pd.read_sql_query(query, connections[using], params=params)
    else:
        df = pd.read_sql_query(query, connection, params=params)
    return df
