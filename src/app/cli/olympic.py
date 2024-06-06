import click


@click.group()
def main():
    """main
    """

@main.command()
@click.option('-d', '--debug', default=False, is_flag=True)
def collect_code(
        debug: bool
    ):
    from batch.olympic.collect_code import collect_code

    print(collect_code(
        debug=debug
    ))

@main.command()
@click.option('-s', '--sport', default="basketball")
@click.option('-d', '--debug', default=False, is_flag=True)
def collect_sport(
        sport: str
        , debug: bool
    ):
    from batch.olympic.collect_sport import collect_sport

    print(collect_sport(
        sport=sport
        , debug=debug
    ))

@main.command()
@click.option('-d', '--debug', default=False, is_flag=True)
def bulk_sport_info(debug: bool):
    """전체 경기정보 수집

    Args:
        debug (bool): 개발:True 운영:False
    """
    from batch.olympic.collect_sport import bulk_sport_info

    print(bulk_sport_info(debug=debug))


@main.command()
@click.option('-d', '--debug', default=False, is_flag=True)
def list_schedule(
        debug: bool
    ):
    """전체 경기일정 정보 수집

    Args:
        debug (bool): 개발:True 운영:False
    """
    from batch.olympic.collect_schedule import list_schedule

    print(list_schedule(
        debug=debug
    ))


@main.command()
@click.option('-s', '--sport_name', default="농구")
@click.option('-sge', '--sport_en_name', default="basketball")
@click.option('-d', '--debug', default=False, is_flag=True)
def collect_schedule(
        sport_name: str
        , sport_en_name: str
        , debug: bool
    ):
    """경기일정 정보 수집 단위기능

    Args:
        sport_name (str): 한글종목명
        sport_en_name (str): 영문종목명
        debug (bool): 개발:True 운영:False
    """
    from batch.olympic.collect_schedule import collect_schedule

    print(collect_schedule(
        sport_name=sport_name
        , sport_en_name=sport_en_name
        , debug=debug
    ))



@main.command()
def collect_schedule_test():
    """경기일정 정보 클래스명 파악용 테스트 기능
    """
    from batch.olympic.collect_schedule import collect_schedule_test

    print(collect_schedule_test())


@main.command()
@click.option('-d', '--debug', default=False, is_flag=True)
def bulk_sport(debug: bool):
    """MongoDB 종목정보 테이블에서 Mysql종목정보 테이블로 데이터 insert

    Args:
        debug (bool): 개발:True 운영:False
    """
    from batch.olympic.batch_sport import batch_sport

    print(batch_sport(debug=debug))

@main.command()
@click.option('-d', '--debug', default=False, is_flag=True)
def insert_col(debug: bool):
    """MongoDB 컬렉션 복사 기능

    Args:
        debug (bool): 개발:True 운영:False
    """
    from batch.olympic.insert_col import insert_col

    print(insert_col(debug=debug))

@main.command()
@click.option('-d', '--debug', default=False, is_flag=True)
def update_col(debug: bool):
    """MongoDB Update기능

    Args:
        debug (bool): 개발:True 운영:False
    """
    from batch.olympic.update_col import update_col

    print(update_col(debug=debug))