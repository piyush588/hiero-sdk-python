import pytest
from unittest.mock import MagicMock
from hedera_sdk_python.query.transaction_get_receipt_query import TransactionGetReceiptQuery
from hedera_sdk_python.transaction.transaction_id import TransactionId
from hedera_sdk_python.client.client import Client
from hedera_sdk_python.account.account_id import AccountId
from hedera_sdk_python.response_code import ResponseCode
from hedera_sdk_python.hapi import (
    response_pb2,
    transaction_receipt_pb2,
    transaction_get_receipt_pb2,
    response_header_pb2,
)

def test_transaction_get_receipt_query():
    transaction_id = TransactionId.generate(AccountId(0, 0, 1234))

    query = TransactionGetReceiptQuery()
    query.set_transaction_id(transaction_id)

    client = MagicMock(spec=Client)
    client.operator = MagicMock()
    client.get_node_account_ids.return_value = [AccountId(0, 0, 3)]
    client.max_attempts = 1

    receipt = transaction_receipt_pb2.TransactionReceipt(
        status=ResponseCode.SUCCESS
    )

    response = response_pb2.Response(
        transactionGetReceipt=transaction_get_receipt_pb2.TransactionGetReceiptResponse(
            header=response_header_pb2.ResponseHeader(
                nodeTransactionPrecheckCode=ResponseCode.OK
            ),
            receipt=receipt
        )
    )
    client.send_query.return_value = response

    result = query.execute(client)

    assert result.status == ResponseCode.SUCCESS
    client.send_query.assert_called_once()
    print("Test passed: TransactionGetReceiptQuery returns SUCCESS status.")
