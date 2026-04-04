from __init__ import TaskType

"""
protoc --proto_path=./LCAuthorization/protocol --pyi_out=./LCAuthorization/protocol --python_out=./LCAuthorization/protocol LCAuthorization.proto
"""

messages = []

for attr, v in TaskType.__dict__.items():
    if type(v) == int:
        msgg = f"""message {attr}Query {{
    string task_uuid = 1;
}}

message {attr}Response {{
    string task_uuid = 1;
}}"""
        messages += [msgg]

general_pb = f"""syntax = "proto3";

message Envelope {{
    int32 type = 1;
    string uuid = 2;
    bytes data = 3;
}}

{'\n\n'.join(messages)}"""

with open('./protocol/LCAuthorization.proto', 'w', encoding='utf-8') as f:
    f.write(general_pb)