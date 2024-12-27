#!/usr/bin/env bash

set -e

hapi_version=v0.57.3
protos_dir=.protos


mkdir -p "$protos_dir"
rm -rf "$protos_dir"/*

curl -sL "https://github.com/hashgraph/hedera-protobufs/archive/refs/tags/${hapi_version}.tar.gz" \
  | tar -xz -C "$protos_dir" --strip-components=1

find "$protos_dir" -mindepth 1 -maxdepth 1 \
  ! -name platform \
  ! -name mirror \
  ! -name services \
  -exec rm -r {} +

rm -rf src/hedera_sdk_python/hapi/*
mkdir -p src/hedera_sdk_python/hapi/auxiliary/tss
mkdir -p src/hedera_sdk_python/hapi/event
mkdir -p src/hedera_sdk_python/hapi/mirror  
touch src/hedera_sdk_python/hapi/__init__.py

python -m grpc_tools.protoc \
  --proto_path="$protos_dir/platform" \
  --proto_path="$protos_dir/services" \
  --pyi_out=./src/hedera_sdk_python/hapi \
  --python_out=./src/hedera_sdk_python/hapi \
  --grpc_python_out=./src/hedera_sdk_python/hapi \
  "$protos_dir"/services/*.proto \
  "$protos_dir"/services/auxiliary/tss/*.proto \
  "$protos_dir"/platform/event/*.proto

python -m grpc_tools.protoc \
  --proto_path="$protos_dir/mirror" \
  --proto_path="$protos_dir/services" \
  --proto_path="$protos_dir/platform" \
  --pyi_out=./src/hedera_sdk_python/hapi/mirror \
  --python_out=./src/hedera_sdk_python/hapi/mirror \
  --grpc_python_out=./src/hedera_sdk_python/hapi/mirror \
  $(find "$protos_dir/mirror" -name '*.proto')

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

echo "All done generating protos."
