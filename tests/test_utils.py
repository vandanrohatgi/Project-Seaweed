"""Tests for util functions"""

import pytest
from project_seaweed.util import is_reachable, parse_template,cve_payload_gen
from pytest_mock import MockFixture
import yaml

@pytest.fixture
def mock_nuclei_template(mocker: MockFixture):
    """Mock nuclei POC yaml file
    
    Patches "open" file function.
    """
    sample_dict={
        "info":{
            "name": "cve name",
            "severity": "critical",
            "tags": "xss,rce,sqli",
            "classification":{
                "cwe-id":"CWE-420"
            }
        }
    }
    mocked_yaml = mocker.mock_open(read_data=yaml.dump(sample_dict))
    mocker.patch("builtins.open", mocked_yaml)

def test_parse_template(mock_nuclei_template:pytest.fixture) -> None:
    """Tests for opening nuclei yaml template and extract data"""
    result=parse_template(cve="CVE-2022-1337")
    assert "name" in result.keys()
    assert result["cvss-score"] == "None"

def test_is_reachable(mock_head_request: MockFixture) -> None:
    """Test if is_reachable function returns True on alive URLs"""
    result_true=is_reachable(url="http://validurl.com")
    result_false=is_reachable(url="notvalidurl")
    assert result_true == True

def test_is_not_reachable(mock_unreachable_url:MockFixture) -> None:
    """Test if is_reachable function returns False on dead / wrong URLs"""
    result_false=is_reachable(url="invalidurl")
    assert result_false == False

def test_cve_payload_gen() -> None:
    result_good_cve=cve_payload_gen(cve="CVE-2022-1337")
    result_bad_cve=cve_payload_gen(cve="not_a.cve")
    assert "CVE-2022-1337" in result_good_cve 
    assert result_bad_cve is None

