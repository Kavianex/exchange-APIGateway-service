from enum import Enum


class Roles(Enum):
    admin = 'ADMIN'
    staff = 'STAFF'
    user = 'USER'
    visitor = 'VISITOR'
