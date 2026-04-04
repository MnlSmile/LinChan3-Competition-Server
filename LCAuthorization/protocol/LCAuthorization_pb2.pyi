from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Envelope(_message.Message):
    __slots__ = ()
    TYPE_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    type: int
    uuid: str
    data: bytes
    def __init__(self, type: _Optional[int] = ..., uuid: _Optional[str] = ..., data: _Optional[bytes] = ...) -> None: ...

class PushNewestAuthorizationCodeQuery(_message.Message):
    __slots__ = ()
    TASK_UUID_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    task_uuid: str
    code: str
    original_message: str
    time: int
    def __init__(self, task_uuid: _Optional[str] = ..., code: _Optional[str] = ..., original_message: _Optional[str] = ..., time: _Optional[int] = ...) -> None: ...

class PushNewestAuthorizationCodeResponse(_message.Message):
    __slots__ = ()
    TASK_UUID_FIELD_NUMBER: _ClassVar[int]
    task_uuid: str
    def __init__(self, task_uuid: _Optional[str] = ...) -> None: ...
