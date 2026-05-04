import pytest


@pytest.mark.skip(reason="Фича в разработке") # Указываем маркировку, которая пропустит данный автотест
def test_feature_in_development():
    pass