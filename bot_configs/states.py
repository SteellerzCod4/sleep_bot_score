import enum


class States(enum.Enum):
    START = "START"
    NAME_REG = "NAME_REG"
    AGE_REG = "AGE_REG"

    GO_TO_SLEEP = "GO_TO_SLEEP"
    RETIRE_MODE = "RETIRE_MODE"

    BEST_RETIRE_TIME_REG = "BEST_RETIRE_TIME_REG"
    BEST_WAKEUP_TIME_REG = "BEST_WAKEUP_TIME_REG"
