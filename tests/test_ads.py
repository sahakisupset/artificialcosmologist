from cosmo_research.literature.ads import ADSClient


def test_ads_maps_search_response(httpx_mock):
    httpx_mock.add_response(
        method="GET",
        json={"response": {"docs": [{
            "bibcode": "2026TEST..000A",
            "title": ["Alternative redshift"],
            "abstract": "A propagation model.",
            "author": ["Doe, Jane"],
            "pubdate": "2026-05-01",
            "doi": ["10/test"],
            "keyword": ["Cosmology"],
        }]}},
    )
    papers = ADSClient("test-token").search("redshift", rows=1)
    assert len(papers) == 1
    assert papers[0].source == "ads"
    assert papers[0].title == "Alternative redshift"
