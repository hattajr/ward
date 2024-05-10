from time import sleep


def test_ward_watchit_output():
    from ward import ward

    @ward.watchit
    def test_func():
        return 1 + 1

    assert test_func() == 2


def test_ward_remove():
    from ward import ward

    @ward.watchit
    def test_func():
        return 1 + 1

    test_func()

    ward.remove()
    assert ward.benchmarks == []


def test_ward_watchit_in_loop():
    from ward import ward

    ward.remove()

    @ward.watchit
    def test_func():
        return 1 + 1

    def test_func_loop():
        for i in range(3):
            test_func()

    test_func_loop()

    assert len(ward.benchmarks) == 3
    assert len(set(benchmark.func_details for benchmark in ward.benchmarks)) == 1


def test_ward_draw():
    from ward import ward

    from . import from_module

    ward.remove()

    @ward.watchit
    def func_1():
        return sleep(0.3)

    @ward.watchit
    def func_2():
        return sleep(0.5)

    @ward.watchit
    def func_3():
        return sleep(0.1)

    @ward.watchit
    def func_4(sl):
        return sleep(sl)

    @ward.watchit
    def func_4_run():
        sl = [0.15, 0.20, 0.30, 0.2]
        for i in sl:
            func_4(i)

    func_1()
    func_2()
    func_3()
    func_4_run()
    from_module.func_other_1()

    # chart_fp = "ward.html"
    # ward.draw()
    # assert len(ward.benchmarks) == 7
    # assert Path(chart_fp).exists()

    # Path(chart_fp).unlink()
