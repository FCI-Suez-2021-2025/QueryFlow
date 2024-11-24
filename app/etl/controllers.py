import traceback

from app.compiler import parser
from app.gui import ui

from datetime import datetime
import time
from tabulate import tabulate


def compile():
    try:
        query = str(ui.inputbox.text())
        result = parser.parse(query)
        ui.outputbox.setText(str(result))
    except Exception as e:
        traceback.print_exc()
        # print("Compilation Error.", e)


def execute():
    try:
        current_time = datetime.now().strftime("%H:%M:%S")
        start_time = time.time()
        code = str(ui.outputbox.toPlainText())
        exec(str(code))
        ui.results.setText(f"Execution started at: {current_time}\n")

        from app.etl import core

        total = time.time() - start_time
        mins = int(total / 60)
        secs = float(total % 60)
        ui.results.setText(
            ui.results.toPlainText()
            + f"\nExcecution process on {len(core.transformed_data)} rows.\n \tTook: {mins} Minutes, {secs:.2f} Seconds.\n"
        )

        if isinstance(core.transformed_data, str):
            ui.results.setText(
                ui.results.toPlainText() + f"\n{core.transformed_data}\n"
            )
        else:
            table = tabulate(
                core.transformed_data, headers=core.transformed_data.keys()
            )
            ui.results.setText(ui.results.toPlainText() + f"\n{table}\n")

    except Exception as e:
        traceback.print_exc()
        # print("Execution Error.", e.)
