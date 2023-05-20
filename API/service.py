from API.repositories import *


class ServiceException(Exception):
    def __init__(self, message: str):
        self.__message = message

    @property
    def message(self) -> str:
        return self.__message


class UnauthorizedException(ServiceException):
    def __init__(self, message: str = 'user unauthorized'):
        super().__init__(message)


class NotFoundException(ServiceException):
    def __init__(self, message: str = 'not found'):
        super().__init__(message)


class InvalidSyntaxException(ServiceException):
    def __init__(self, message: str = 'invalid syntax'):
        super().__init__(message)


class Service:
    employee_repository = EmployeeRepository()
    employee_session_repository = EmployeeSessionRepository()

    @staticmethod
    def find_employee(username: str = None, password: str = None, session: str = None) -> Employee:
        if username is not None and password is not None:
            if employee := Service.employee_repository.find_by_username_and_password(username, password):
                return employee
            raise NotFoundException()
        elif session is not None:
            if employee_session := Service.employee_session_repository.find_by_session(session):
                return employee_session.employee
            raise NotFoundException('employee not found')
        else:
            raise InvalidSyntaxException()

    @staticmethod
    def create_session(employee: Employee, session: str) -> None:
        Service.employee_session_repository.save(EmployeeSession(employee=employee, session=session))

    @staticmethod
    def delete_session(session: str) -> None:
        Service.employee_session_repository.delete(Service.validate_session(session))

    @staticmethod
    def validate_session(session: str, employee_type: str = None) -> EmployeeSession:
        if requester := Service.employee_session_repository.find_by_session(session=session):
            if requester is None or (employee_type is not None and requester.employee.type != employee_type):
                raise UnauthorizedException()
            return requester
        raise NotFoundException()

    @staticmethod
    def find_all_employees(session: str) -> list[Employee]:
        Service.validate_session(session=session, employee_type='administrator')
        return Service.employee_repository.find_all()

    @staticmethod
    def create_employee(session: str, employee_username: str, employee_password: str,
                        employee_type: str) -> Employee:
        Service.validate_session(session=session, employee_type='administrator')
        employee = Employee(username=employee_username, password=employee_password, type=employee_type)
        Service.employee_repository.save(employee)
        return employee

    @staticmethod
    def update_employee(session: str, employee_id: int, employee_username: str, employee_password: str,
                        employee_type: str):
        Service.validate_session(session=session, employee_type='administrator')
        employee = Service.employee_repository.find_by_id(employee_id)
        if employee is None:
            raise NotFoundException()
        employee.username = employee_username
        employee.password = employee_password
        employee.type = employee_type
        Service.employee_repository.update(employee)

    @staticmethod
    def delete_employee(session: str, employee_id: int):
        Service.validate_session(session=session, employee_type='administrator')
        employee = Service.employee_repository.find_by_id(employee_id)
        if employee is None:
            raise NotFoundException()
        Service.employee_repository.delete(employee)
