import queue as queue

from Employee import *


class XStage:
    def __init__(self, stage_name: str, next_stage: str = None, number_of_employee: int = 1) -> None:
        self.stage_name = stage_name
        self.employees = []
        for i in range(number_of_employee):
            self.employees.append(Employee(i + 1))
        self.next_stage = next_stage
        self.wait_queue = queue.Queue()

    def get_next_stage(self) -> str:
        return self.next_stage

    def set_next_stage(self, next_stage: str) -> None:
        self.next_stage = next_stage

    def findAvailableEmployees(self) -> int:
        for i in range(len(self.employees)):
            if not self.employees[i].busy:
                return i
        return -1

    def print_XStage(self) -> None:
        print(f"{self.stage_name} stage, next stage: {self.next_stage}")
        for employee in self.employees:
            print(employee)


# if __name__ == "__main__":
#     collections = XStage('collections', number_of_employee=3)
#     collections.print_XStage()
