#!/bin/bash

# Variables
hapi_version="v0.57.3"
protos_dir=".protos"
output_dir="src/hedera_sdk_python/hapi/mirror"

# Step 1: Create necessary directories
mkdir -p $protos_dir
mkdir -p $output_dir

# Step 2: Clear previous downloads and output
rm -rf $protos_dir/*
rm -rf $output_dir/*

# Step 3: Download and extract the protobuf files
echo "Downloading Hedera protobufs version $hapi_version..."
curl -sL "https://github.com/hashgraph/hedera-protobufs/archive/refs/tags/${hapi_version}.tar.gz" | tar -xz -C $protos_dir --strip-components=1

# Step 4: Compile the mirror protobuf files with dependencies
echo "Compiling mirror protobuf files..."
python -m grpc_tools.protoc \
    --proto_path=$protos_dir/mirror \
    --proto_path=$protos_dir/services \
    --python_out=$output_dir \
    --grpc_python_out=$output_dir \
    $protos_dir/mirror/*.proto

# Step 5: Confirm success
if [ "$(ls -A $output_dir)" ]; then
  echo "Mirror protobuf files compiled and copied successfully to '$output_dir'."
else
  echo "Error: Mirror protobuf files failed to compile or copy."
  exit 1
fi
