

import pandas as pd
from datetime import datetime


def main_(class_csv_path, attendance_csv_path):
    try:
        class1_df = pd.read_csv(class_csv_path)
        l_df = pd.read_csv(attendance_csv_path)

        current_date = datetime.now().strftime("%Y-%m-%d")

        attendance_dict = dict(zip(l_df["Name"], l_df["Status"]))

        def get_status(student_name):
            return attendance_dict.get(student_name, "A")

        if current_date in class1_df.columns:
            column_versions = [
                col for col in class1_df.columns if col.startswith(current_date)
            ]
            next_version = len(column_versions) + 1
            current_date = f"{current_date}_{next_version}"

        class1_df[current_date] = class1_df["Name"].apply(get_status)
        class1_df.to_csv(class_csv_path, index=False)

        print(
            f"Attendance has been updated and saved to '{class_csv_path}' with the date column '{current_date}'."
        )
    except Exception as e:
        print(f"An error occurred: {e}")


# main_("D:/DNN PROJECT 2024 MS-351/csv files/Instructor/ali.nasir@gmail.com/class1.csv", "D:/DNN PROJECT 2024 MS-351/csv files/classes_list/l.csv")
