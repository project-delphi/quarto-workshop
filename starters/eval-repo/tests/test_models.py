"""No model version can see `duration`, which is only known after the call."""

from acme_eval import data, models


def test_no_release_uses_duration():
    for release in models.load_releases():
        assert data.LEAKY not in release.features, release.version


def test_fitted_pipelines_never_see_duration():
    sample = data.load().sample(2_000, random_state=0)
    for release in models.load_releases():
        pipeline = models.build(release).fit(sample[release.features], sample[data.TARGET])
        assert data.LEAKY not in pipeline.feature_names_in_, release.version


def test_releases_are_as_documented():
    releases = {r.version: r for r in models.load_releases()}
    assert list(releases) == ["v1", "v2", "v3"]
    assert releases["v1"].features == ["age", "balance", "housing", "loan"]
    assert releases["v2"].features == data.FEATURES
    assert releases["v3"].model == "gradient_boosting"
