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
def list_schedule(
        debug: bool
    ):
    """전체 경기일정 정보 수집
    """
    from batch.olympic.collect_schedule import list_schedule

    print(list_schedule(
        debug=debug
    ))


@main.command()
@click.option('-g', '--game_name', default="농구")
@click.option('-ge', '--game_en_name', default="basketball")
@click.option('-d', '--debug', default=False, is_flag=True)
def collect_schedule(
        game_name: str
        , game_en_name: str
        , debug: bool
    ):
    """경기일정 정보 수집 단위기능

    Args:
        sport (str): _description_
        debug (bool): _description_
    """
    from batch.olympic.collect_schedule import collect_schedule

    print(collect_schedule(
        game_name=game_name
        , game_en_name=game_en_name
        , debug=debug
    ))



@main.command()
def collect_schedule_test():
    """경기일정 정보 클래스명 파악용 테스트 기능
    """
    from batch.olympic.collect_schedule import collect_schedule_test

    print(collect_schedule_test())
