import inspect
import time
from collections import namedtuple
from dataclasses import dataclass
from functools import wraps
from typing import Optional

import altair as alt
import polars as pl

# TODO: multiple output format (svg, html, png, jpeg)
# TODO: multiple time units (ms, second, minutes, hour)
# TODO: more information in tooltip
# TODO: fix left-side interactive zoom
# TODO: handle loop function in seperate chart


@dataclass
class Ward:
    filepath: Optional[str] = "./ward.html"

    def __post_init__(self):
        self.benchmark = namedtuple(
            "benchmark", ["func_name", "start_time", "end_time", "elapsed", "func_details"]
        )
        self.benchmarks = []

    def watchit(self, a_func):
        @wraps(a_func)
        def wrapper(*args, **kwargs):
            try:
                start_time = time.time_ns()
                start = time.perf_counter_ns()
                res = a_func(*args, **kwargs)
                func_name = a_func.__name__
                return res
            finally:
                end = time.perf_counter_ns()
                elapsed_time = end - start  # in ns

                caller_frame = inspect.currentframe().f_back
                caller_filename = caller_frame.f_code.co_filename.split("/")[-1]
                caller_lineno = caller_frame.f_lineno
                self.benchmarks.append(
                    self.benchmark(
                        func_name,
                        start_time,
                        end,
                        elapsed_time / 1e9,
                        f"{caller_filename}:{func_name}:{caller_lineno}",
                    )
                )

        return wrapper

    def remove(self):
        self.benchmarks = []

    def draw(self):
        # columns=["func_name", "start", "end", "elapsed", "func_details"]
        df = pl.DataFrame(self.benchmarks)
        print(df)

        df = (
            df
            .sort(by="start_time")
            .with_columns(pl.col("elapsed").shift_and_fill(n=1, fill_value=0).cumsum().alias("datum_min"))
            .with_columns((pl.col("datum_min") + pl.col("elapsed")).alias("datum_max"))
            .with_columns(pl.cum_count("func_details").over("func_details").alias("ngroup"))
            .with_columns(pl.count("func_details").over("func_details").alias("ncount"))
            .with_columns(pl.when(pl.col("ncount") > 1).then(pl.lit("*")).otherwise(None).alias("is_it"))
            .with_columns(pl.concat_str([pl.col("func_details"), pl.lit(" "), pl.lit("["), pl.col("ngroup"), pl.col("is_it"), pl.lit("]")], ignore_nulls=True).alias("fuid"))
        )

        print(df)

        alt.selection_interval(bind="scales", encodings=["x"])

        bar = (
            alt.Chart(df)
            .mark_bar(cornerRadius=5, height=5)
            .encode(
                x=alt.X("datum_min:Q", title="Time (s)"),
                x2="datum_max:Q",
                y=alt.Y("fuid:N", title="Functions").sort(field="start_time", order="ascending"),
                color=alt.Color("func_name:N", title="Function", legend=None),
                tooltip="fuid"
            )
        )

        elapsed_time_text = (
            alt.Chart(df)
            .mark_text(align="left", dx=5)
            .encode(
                x="datum_max:Q",
                y=alt.Y("fuid:N").sort(field="start_time", order="ascending"),
                text=alt.Text("elapsed:Q", format=".1f"),
            )
        )

        chart = (bar + elapsed_time_text).interactive()
        chart.save(self.filepath, embed_options={"renderer": "svg"})
