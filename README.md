# Wards: A Simple python time profiler

Wards is a chill little Python library that times your functions, no big deal. It's not gonna weigh you down with bloat or anything. Just does its thing quietly in the background. But here's the kicker - Wards also hooks you up with some slick visualizations . You get to see your timing data in living color, all interactive and stuff. If you're looking to optimize your Python code without breaking a sweat, Wards is your wingman. It's got you covered with that smooth, effortless vibe.

<p align="center">
  <img src=".assets/ward.gif" alt="GIF Description" width="600" />
</p>

# Usage
```python
    from ward import ward
    ward.remove()

    @ward.watchit
    def func_1():
        return sleep(0.3)

    @ward.watchit
    def func_2():
        return sleep(0.5)

    @ward.watchit
    def func_3():
        sl = [0.15, 0.20, 0.30, 0.2]
        for i in sl:
            func_4(i)

    func_1()
    func_2()
    func_3()
```

> [!WARNING]
> This software is unfinished. Keep your expectations low.


*Please, read [CONTRIBUTING.md](CONTRIBUTING.md) before making a PR.*