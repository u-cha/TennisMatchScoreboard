from uuid import uuid4


class UUIDEmissionService:
    @staticmethod
    def emit_uuid() -> str:
        uuid = uuid4().hex
        return uuid
