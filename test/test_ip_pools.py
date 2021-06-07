import pytest
import responses

from sparkpost import SparkPost
from sparkpost.exceptions import SparkPostAPIException


@responses.activate
def test_success_list_ip_pools():
    responses.add(
        responses.GET,
        "https://api.sparkpost.com/api/v1/ip-pools",
        status=200,
        content_type="application/json",
        body="""{
  "results": [
    {
      "id": "marketing_ip_pool",
      "name": "Marketing IP Pool",
      "ips": [],
      "signing_domain": "example.com",
      "fbl_signing_domain": "sparkpostmail.com",
      "auto_warmup_overflow_pool": "overflow_pool"
    },
    {
      "id": "default",
      "name": "Default",
      "ips": [
        {
          "external_ip": "54.244.54.135",
          "hostname": "mta472a.sparkpostmail.com",
          "auto_warmup_enabled": true,
          "auto_warmup_stage": 5
        }
      ]
    }
  ]
}"""
    )
    sp = SparkPost("fake-key")
    results = sp.ip_pools.list()
    assert len(results) == 2
    assert results[0]["id"] == "marketing_ip_pool"


@responses.activate
def test_fail_list_ip_pools():
    responses.add(
        responses.GET,
        "https://api.sparkpost.com/api/v1/ip-pools",
        status=500,
        content_type="application/json",
        body="""
        {"errors": [{"message": "You failed", "description": "More Info"}]}
        """
    )
    with pytest.raises(SparkPostAPIException):
        sp = SparkPost("fake-key")
        sp.ip_pools.list()


@responses.activate
def test_success_get_ip_pool():
    responses.add(
        responses.GET,
        "https://api.sparkpost.com/api/v1/ip-pools/marketing_ip_pool",
        status=200,
        content_type="application/json",
        body="""{
  "results": {
    "id": "marketing_ip_pool",
    "name": "Marketing IP Pool",
    "fbl_signing_domain": "sparkpostmail.com",
    "ips": [
      {
        "external_ip": "54.244.54.135",
        "hostname": "mta472a.sparkpostmail.com",
        "auto_warmup_enabled": true,
        "auto_warmup_stage": 5
      },
      {
        "external_ip": "54.244.54.137",
        "hostname": "mta474a.sparkpostmail.com",
        "auto_warmup_enabled": false
      }
    ],
    "signing_domain": "example.com",
    "auto_warmup_overflow_pool": "overflow_pool"
  }
}"""
    )
    sp = SparkPost("fake-key")
    result = sp.ip_pools.get("marketing_ip_pool")
    assert result is not None


@responses.activate
def test_not_found_get_ip_pool():
    responses.add(
        responses.GET,
        "https://api.sparkpost.com/api/v1/ip-pools/foo.com",
        status=404,
        content_type="application/json",
        body="""{"errors": [{"message": "Resource could not be found"}]}"""
    )
    with pytest.raises(SparkPostAPIException):
        sp = SparkPost("fake-key")
        sp.ip_pools.get("foo.com")


@responses.activate
def test_success_delete_ip_pool():
    responses.add(
        responses.DELETE,
        "https://api.sparkpost.com/api/v1/ip-pools/marketing_ip_pool",
        status=204,
        content_type="application/json"
    )
    sp = SparkPost("fake-key")
    results = sp.ip_pools.delete("marketing_ip_pool")
    assert results is True


@responses.activate
def test_not_found_delete_ip_pool():
    responses.add(
        responses.DELETE,
        "https://api.sparkpost.com/api/v1/ip-pools/foo.com",
        status=404,
        content_type="application/json",
        body="""{"errors": [{"message": "Resource could not be found"}]}"""
    )
    with pytest.raises(SparkPostAPIException):
        sp = SparkPost("fake-key")
        sp.ip_pools.delete("foo.com")


@responses.activate
def test_success_update_ip_pool():
    responses.add(
        responses.PUT,
        "https://api.sparkpost.com/api/v1/ip-pools/marketing",
        status=200,
        content_type="application/json",
        body="""{
  "name": "Updated Marketing Pool",
  "fbl_signing_domain": "sparkpostmail.com",
  "auto_warmup_overflow_pool": "overflow_pool"
}"""
    )

    sp = SparkPost("fake-key")
    results = sp.ip_pools.update("marketing",
                                 name="Updated Marketing Pool",
                                fbl_signing_domain="sparkpostmail.com",
                                auto_warmup_overflow_pool="overflow_pool")
    assert results is not None
    assert results["name"] == "Updated Marketing Pool"


@responses.activate
def test_success_create_ip_pool():
    responses.add(
        responses.POST,
        "https://api.sparkpost.com/api/v1/ip-pools",
        status=200,
        content_type="application/json",
        body="""{
  "results": {
    "id": "marketing_ip_pool"
  }
}"""
    )

    sp = SparkPost("fake-key")
    results = sp.ip_pools.create(name="marketing IP Pool",
                                 fbl_signing_domain="sparkpostmail.com",
                                 auto_warmup_overflow_pool="overflow_pool")
    assert results is not None
    assert results["id"] == "marketing_ip_pool"
