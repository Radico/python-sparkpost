from .base import Resource


class IpPools(Resource):
    """
    IpPools class used to search, get, and modify ip pools.
    For detailed request and response formats, see the `IP Pool API
    documentation
    <https://www.sparkpost.com/api#/reference/ip-pools>`_.
    """
    key = 'ip-pools'

    def create(self, **kwargs):
        """
        Creates an IP Pool and returns a unique ID.
        :param str name: name of the IP Pool
        :param str signing_domain: Domain to use as the DKIM verified signing domain
        :param str fbl_signing_domain: FBL Signing Domain for the pool
        :param str auto_warmup_overflow_pool: IP Pool ID to be used as an overflow pool
            during auto IP warmup. Can specify shared pool to overflow
            to the SparkPost Shared Pool if you have access.

        :returns: IP Pools's ID
        :raises: :exc:`SparkPostAPIException` if API call fails
        """

        return self.request('POST', self.uri, json=kwargs)

    def get(self, id):
        """
        Get an IP Pool

        :param str id: the id of the IP Pool to retrieve

        :returns: the requested IP Pool if found
        :raises: :exc:`SparkPostAPIException` if IP Pool is not found
        """

        uri = "%s/%s" % (self.uri, id)
        return self.request('GET', uri)

    def list(self):
        """
        Get all IP Pools

        :returns: all IP Pools
        :raises: :exc:`SparkPostAPIException` if no subaccount is not found
        """

        return self.request('GET', self.uri)

    def update(self, id, **kwargs):
        """
        Updates an IP Pool
        :param str name: name of the IP Pool
        :param str signing_domain: Domain to use as the DKIM verified signing domain
        :param str fbl_signing_domain: FBL Signing Domain for the pool
        :param str auto_warmup_overflow_pool: IP Pool ID to be used as an overflow pool
            during auto IP warmup. Can specify shared pool to overflow
            to the SparkPost Shared Pool if you have access.

        :returns: IP Pools's ID
        :raises: :exc:`SparkPostAPIException` if API call fails

        :returns: updates IP Pool
        :raises: :exc:`SparkPostAPIException` if no IP Pool is not found
        """
        uri = "%s/%s" % (self.uri, id)
        return self.request('PUT', uri, json=kwargs)

    def delete(self, id):
        """
        Deletes an IP Pool and moves all sending IPs in that pool to the default pool.
         The default pool cannot be deleted.
        :param str id: the id of the IP Pool to delete

        :returns: empty respose body
        :raises: :exc:`SparkPostAPIException` if API call fails
        """
        uri = "%s/%s" % (self.uri, id)
        return self.request('DELETE', uri)
