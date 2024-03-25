from datetime import datetime, timedelta
from database.models import TimeInfo, TimeSettings
import numpy as np


def r2_retire_score(current_time: str, edge_time: str = "03:00", optimal_time: str = "22:30", ) -> float:
    current_time, edge_time = datetime.strptime(current_time, '%H:%M'), datetime.strptime(edge_time, '%H:%M')
    optimal_time = datetime.strptime(optimal_time, '%H:%M')
    if current_time >= optimal_time:
        numerator = current_time - optimal_time
    else:
        current_time += timedelta(days=1)
        numerator = current_time - optimal_time
    edge_time += timedelta(days=1)
    denominator = edge_time - optimal_time
    return 1 - (numerator / denominator)


def r2_wakeup_score(current_time: str, edge_time: str = "12:00", optimal_time: str = "05:00", ) -> float:
    return 1 - ((datetime.strptime(current_time, '%H:%M') - datetime.strptime(optimal_time, '%H:%M'))
                / (datetime.strptime(edge_time, '%H:%M') - datetime.strptime(optimal_time, '%H:%M')))


def sleep_duration_score(retire_time: str, wakeup_time: str, optimal_duration: float) -> float:
    wakeup_time, retire_time = datetime.strptime(wakeup_time, '%H:%M'), datetime.strptime(retire_time, '%H:%M')
    wakeup_time += timedelta(days=int(retire_time > wakeup_time))
    sleep_duration = wakeup_time - retire_time
    return 1 / (np.exp(np.square(sleep_duration.total_seconds() / 60 / 60 - optimal_duration) / 4))


# def f1_sleep_score(retire_time: str, edge_retire_time: str, optimal_retire_time: str,
#                    wakeup_time: str, edge_wakeup_time: str, optimal_wakeup_time: str,
#                    optimal_duration: int, first_n: int) -> float:
#     retire_score, wakeup_score, duration_score = (r2_retire_score(retire_time, edge_retire_time, optimal_retire_time),
#                                                   r2_wakeup_score(wakeup_time, edge_wakeup_time, optimal_wakeup_time),
#                                                   sleep_duration_score(retire_time, wakeup_time, optimal_duration))
#     print(f"retire_score: {retire_score}\nwakeup_score: {wakeup_score}\nduration_score: {duration_score}")
#     retire_score_fixed, wakeup_score_fixed = np.maximum(0, retire_score), np.maximum(0, wakeup_score)
#     return np.round((3 * retire_score_fixed * wakeup_score_fixed * duration_score /
#                      (retire_score_fixed + wakeup_score_fixed + duration_score)), first_n)

def f1_sleep_score(current_wakeup_time: str, time_info: TimeInfo, time_settings: TimeSettings, first_n: int) -> float:

    retire_score, wakeup_score, duration_score = (r2_retire_score(time_info.current_retire_time,
                                                                  time_settings.worst_retire_time,
                                                                  time_settings.best_retire_time),
                                                  r2_wakeup_score(current_wakeup_time,
                                                                  time_settings.worst_wakeup_time,
                                                                  time_settings.best_wakeup_time),
                                                  sleep_duration_score(time_info.current_retire_time,
                                                                       current_wakeup_time,
                                                                       time_settings.best_sleep_duration))

    print(f"retire_score: {retire_score}\nwakeup_score: {wakeup_score}\nduration_score: {duration_score}")

    retire_score_fixed, wakeup_score_fixed = np.maximum(0, retire_score), np.maximum(0, wakeup_score)

    return np.round((3 * retire_score_fixed * wakeup_score_fixed * duration_score /
                     (retire_score_fixed + wakeup_score_fixed + duration_score)), first_n)
