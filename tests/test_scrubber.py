import os
import pytest

from checkpoint_scrubber import main


@pytest.fixture
def sample_fpath(tmp_path):
    sample_files = ["vggnet-001.params",
                    "vggnet-0010.params",
                    "vggnet-0011.params",
                    "vggnet-0012.params",
                    "vggnet-0013.params",
                    "vggnet-0014.params",
                    "vggnet-0050.params",
                    "vggnet-0093.params",
                    "vggnet-symbol.json"]
    for fname in sample_files:
        p = tmp_path / fname
        p.touch()

    return tmp_path


def test_main(sample_fpath):
    main(sample_fpath)
    files = os.listdir(sample_fpath)
    assert len(files) == 4
    assert "vggnet-001.params" in files
    assert "vggnet-0010.params" not in files
    assert "vggnet-0050.params" in files
    assert "vggnet-0093.params" in files
    assert "vggnet-symbol.json" in files
