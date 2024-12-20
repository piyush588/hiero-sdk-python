import time
from hedera_sdk_python.hapi import query_header_pb2
from hedera_sdk_python.response_code import ResponseCode

class Query:
    """
    Base class for all Hedera network queries.

    This class provides common functionality for constructing and executing queries
    to the Hedera network. It has been simplified to remove payment handling logic
    since it's not needed for queries that do not require payment.
    """

    def __init__(self):
        """
        Initializes the Query with default values.
        """
        self.timestamp = int(time.time())
        self.node_account_ids = []
        self.operator = None
        self.node_index = 0

    def _before_execute(self, client):
        """
        Prepares the query for execution by setting up nodes.

        Args:
            client (Client): The client instance to use.
        """
        if not self.node_account_ids:
            self.node_account_ids = client.get_node_account_ids()

        self.operator = self.operator or client.operator
        self.node_account_ids = list(set(self.node_account_ids))

    def _make_request_header(self):
        """
        Constructs the request header for the query.

        Returns:
            QueryHeader: The protobuf QueryHeader object.
        """
        header = query_header_pb2.QueryHeader()
        header.responseType = query_header_pb2.ResponseType.ANSWER_ONLY
        return header

    def _make_request(self):
        """
        Constructs the query request.

        Returns:
            Query: The protobuf Query object.

        Raises:
            NotImplementedError: If not implemented by the subclass.
        """
        raise NotImplementedError("_make_request must be implemented by subclasses.")

    def execute(self, client, timeout=60):
        self._before_execute(client)
        max_attempts = getattr(client, 'max_attempts', 10)
        for attempt in range(max_attempts):
            try:
                self.node_index = attempt % len(self.node_account_ids)
                node_account_id = self.node_account_ids[self.node_index]
                response = client.send_query(self, node_account_id, timeout=timeout)
                if response is None:
                    continue
                status = self._get_status_from_response(response)
                if status == ResponseCode.OK:
                    return self._map_response(response)
                elif status in [ResponseCode.BUSY, ResponseCode.UNKNOWN]:
                    continue
                else:
                    raise Exception(f"Query failed with status: {ResponseCode.get_name(status)}")
            except Exception as e:
                print(f"Error executing query: {e}")
                continue
        raise Exception("Failed to execute query after maximum attempts.")


    def _get_status_from_response(self, response):
        """
        Extracts the status from the response.

        Args:
            response (Response): The response from the network.

        Returns:
            int: The status code.

        Raises:
            NotImplementedError: If not implemented by the subclass.
        """
        raise NotImplementedError("_get_status_from_response must be implemented by subclasses.")

    def _map_response(self, response):
        """
        Maps the response to the desired output.

        Args:
            response (Response): The response from the network.

        Returns:
            Any: The mapped response.

        Raises:
            NotImplementedError: If not implemented by subclasses.
        """
        raise NotImplementedError("_map_response must be implemented by subclasses.")
