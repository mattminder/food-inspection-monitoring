import datetime
import unittest
from unittest import mock
import pandas as pd

from src.schema.inspection import Inspection
from src.schema.activity import Activity

from src.plots.lateness_over_time import (
    _calculate_percentage_late_single_canton,
    _calculate_number_invalid,
    _get_next_inspection,
    _EngineeredColumns,
)


class TestLatenessOverTime(unittest.TestCase):
    def test__get_next_inspection(self):
        df = pd.DataFrame(
            [
                ("2021-01-01", 2),
                ("2021-01-31", 1),
                ("2020-02-29", 3),  # map leap year to non-leap-year
                ("2020-02-29", 4),  # map leap year to leap year
                ("NaT", 2),  # map NaT to NaT
            ],
            columns=[Inspection.date, Activity.base_frequency],
        )
        df[Inspection.date] = pd.to_datetime(df[Inspection.date])

        expected = pd.to_datetime(
            pd.Series(["2023-01-01", "2022-01-31", "2023-03-01", "2024-02-29", "NaT"])
        )
        result = _get_next_inspection(df)
        pd.testing.assert_series_equal(expected, result)

    def test__calculate_number_invalid_single_canton(self):
        single_canton = pd.DataFrame(
            [
                # uid1 is late in February 2023
                ("2022-01-01", "2023-01-01", "uid1"),
                ("2023-02-28", "2024-02-28", "uid1"),
                # uid2 is late in February and March 2023
                ("2021-01-05", "2023-01-05", "uid2"),
                ("2023-03-07", "2025-03-07", "uid2"),
                # uid3 is not considered, as its first inspection is in 2024
                ("2024-01-01", "2026-01-01", "uid3"),  # opened later
            ],
            columns=[
                Inspection.date,
                _EngineeredColumns.next_inspection_due_date,
                Activity.activity_uid,
            ],
        )
        single_canton[Inspection.date] = pd.to_datetime(single_canton[Inspection.date])
        single_canton[_EngineeredColumns.next_inspection_due_date] = pd.to_datetime(
            single_canton[_EngineeredColumns.next_inspection_due_date]
        )

        # construct the expected series from Jan to Apr
        expected = pd.Series(
            [
                0.0,
                1.0,  # uid1 and uid2 late
                0.5,  # uid2 late
                0.0,  # uid2 late
            ],
            index=pd.date_range(
                "2023-01-01", "2023-04-01", freq=pd.offsets.MonthBegin(1)
            ),
        )

        percentage_late = _calculate_percentage_late_single_canton(
            single_canton, "2023-01-01", "2023-04-01"
        )
        pd.testing.assert_series_equal(expected, percentage_late)

    @mock.patch("src.plots.lateness_over_time._get_start_end_date")
    @mock.patch("src.plots.lateness_over_time._calculate_percentage_late_single_canton")
    def test__calculate_number_invalid(
        self, mock__calculate_percentage_late_single_canton, mock__get_start_end_date
    ):
        # mock _calculate_percentage_late_single_canton
        date_range = pd.date_range(
            "2023-01-01", "2023-04-01", freq=pd.offsets.MonthBegin(1)
        )
        series_canton1 = pd.Series(
            [0.0, 0.2, 0.4, 0.6],
            index=date_range,
        )
        series_canton2 = pd.Series(
            [0.5, 0.5, 1.0, 1.0],
            index=date_range,
        )

        mock__calculate_percentage_late_single_canton.side_effect = [
            series_canton1,
            series_canton2,
        ]

        # mock _get_start_end_date
        mock__get_start_end_date.return_value = [
            datetime.date(2023, 1, 1),
            datetime.date(2023, 4, 1),
        ]

        # construct input dataframe with two cantons
        merged = pd.DataFrame(
            {
                Activity.canton: ["canton1", "canton1", "canton2"],
                "foo": ["bar1", "bar", "bar2"],
            }
        )

        # construct expected
        expected = pd.DataFrame(
            [(0.0, 0.2, 0.4, 0.6), (0.5, 0.5, 1.0, 1.0)],
            index=pd.Index(["canton1", "canton2"], name=Activity.canton),
            columns=date_range,
        )

        result = _calculate_number_invalid(merged)

        # compare results
        pd.testing.assert_frame_equal(result, expected)

        # make sure the mocks have the right calls
        # since __eq__ is overloaded in dataframes, we have to explicitly unpack the calls
        (call1_args, call1_kwargs), (
            call2_args,
            call2_kwargs,
        ) = mock__calculate_percentage_late_single_canton.call_args_list

        (call_df1,) = call1_args
        pd.testing.assert_frame_equal(
            call_df1,
            merged[merged[Activity.canton] == "canton1"].drop(Activity.canton, axis=1),
        )
        self.assertEqual(
            call1_kwargs,
            {
                "start_date": datetime.date(2023, 1, 1),
                "end_date": datetime.date(2023, 4, 1),
            },
        )

        (call_df2,) = call2_args
        pd.testing.assert_frame_equal(
            call_df2,
            merged[merged[Activity.canton] == "canton2"].drop(Activity.canton, axis=1),
        )
        self.assertEqual(
            call2_kwargs,
            {
                "start_date": datetime.date(2023, 1, 1),
                "end_date": datetime.date(2023, 4, 1),
            },
        )
