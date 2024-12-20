#!/bin/bash

hapi_version=v0.57.3
protos_dir=.protos

mkdir -p $protos_dir
rm -rf $protos_dir/*


# Download the tarball of a specific tag and immediately extract the subdirectory
curl -sL "https://github.com/hashgraph/hedera-protobufs/archive/refs/tags/${hapi_version}.tar.gz" | tar -xz -C $protos_dir --strip-components=1
# Keep 'platform' and 'services', remove everything else in the current directory
find "$protos_dir" -mindepth 1 -maxdepth 1 ! -name platform ! -name services -exec rm -r {} +

rm -rf src/hedera_sdk_python/hapi/*
mkdir -p src/hedera_sdk_python/hapi/auxiliary/tss
mkdir -p src/hedera_sdk_python/hapi/event
touch src/hedera_sdk_python/hapi/__init__.py
python -m grpc_tools.protoc \
    --proto_path=$protos_dir/platform \
    --proto_path=$protos_dir/services \
    --pyi_out=./src/hedera_sdk_python/hapi \
    --python_out=./src/hedera_sdk_python/hapi \
    --grpc_python_out=./src/hedera_sdk_python/hapi \
    $protos_dir/services/*.proto $protos_dir/services/auxiliary/tss/*.proto $protos_dir/platform/event/*.proto

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