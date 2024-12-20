#!/bin/bash
rm -rf src/hedera_sdk_python/hapi/*
mkdir -p src/hedera_sdk_python/hapi/auxiliary/tss
mkdir -p src/hedera_sdk_python/hapi/event
touch src/hedera_sdk_python/hapi/__init__.py
python -m grpc_tools.protoc \
    --proto_path=./src/protos \
    --pyi_out=./src/hedera_sdk_python/hapi \
    --python_out=./src/hedera_sdk_python/hapi \
    --grpc_python_out=./src/hedera_sdk_python/hapi \
    ./src/protos/*.proto ./src/protos/event/*.proto ./src/protos/auxiliary/tss/*.proto

# Modify the script for the specific import changes
if [[ "$OSTYPE" == "darwin"* ]]; then
    find ./src/hedera_sdk_python/hapi -type f -name "*.py" -exec sed -i '' \
        -e '/^import .*_pb2 as .*__pb2/s/^/from . /' \
        -e 's/^from auxiliary\.tss/from .auxiliary.tss/' \
        -e 's/^from event/from .event/' {} +
else
    find ./src/hedera_sdk_python/hapi -type f -name "*.py" -exec sed -i \
        -e '/^import .*_pb2 as .*__pb2/s/^/from . /' \
        -e 's/^from auxiliary\.tss/from .auxiliary.tss/' \
        -e 's/^from event/from .event/' {} +
fi