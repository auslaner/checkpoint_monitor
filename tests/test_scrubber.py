import os
import pytest

from checkpoint_scrubber import main


@pytest.fixture
def sample_fpath(tmp_path):
    def populate_test_directories(sample_files, model_directory):
        for fname in sample_files:
            p = model_directory / fname
            p.touch()

    model_1_files = ["model1-001.params",
                     "model1-0010.params",
                     "model1-0011.params",
                     "model1-0012.params",
                     "model1-0013.params",
                     "model1-0014.params",
                     "model1-0050.params",
                     "model1-0093.params",
                     "model1-symbol.json"]

    model_2_files = ["model2-002.params",
                     "model2-0011.params",
                     "model2-0012.params",
                     "model2-0017.params",
                     "model2-0051.params",
                     "model2-0052.params",
                     "model2-symbol.json"]

    model_3_files = ["model3-0010.params",
                     "model3-0060.params",
                     "model3-0070.params",
                     "model3-symbol.json"]

    model_1 = tmp_path / "model_1"
    model_2 = tmp_path / "model_2"
    model_3 = tmp_path / "model_3"

    model_1.mkdir()
    model_2.mkdir()
    model_3.mkdir()

    populate_test_directories(model_1_files, model_1)
    populate_test_directories(model_2_files, model_2)
    populate_test_directories(model_3_files, model_3)

    return tmp_path


def test_main(sample_fpath):
    # Test to make sure the sample files are setup correctly
    model_dirs = os.listdir(sample_fpath)
    assert "model_1" in model_dirs
    assert "model_2" in model_dirs
    assert "model_3" in model_dirs

    for dirpath, dirnames, filenames in os.walk(sample_fpath):
        print("Testing {}".format(dirpath))
        print("It contains the files:\n\t{}".format(filenames))

        if dirpath.split(os.sep)[-1] == "model_1":
            assert len(filenames) == 9
            assert "model1-001.params" in filenames
            assert "model1-0012.params" in filenames

        if dirpath.split(os.sep)[-1] == "model_2":
            assert len(filenames) == 7
            assert "model2-symbol.json" in filenames
            assert "model2-0017.params" in filenames

    print("*" * 90)
    print("[!] Running main function from checkpoint_scrubber...")
    # Test the function
    main(sample_fpath)
    print("[!] Done!")
    print("*" * 90)

    for dirpath, dirnames, filenames in os.walk(sample_fpath):
        print("Testing {}".format(dirpath))
        print("It contains the files:\n\t{}".format(filenames))

        if dirpath.split(os.sep)[-1] == "model_1":
            assert len(filenames) == 3
            assert "model1-001.params" not in filenames
            assert "model1-0012.params" not in filenames
            assert "model1-0093.params" in filenames
            assert "model1-symbol.json" in filenames

        if dirpath.split(os.sep)[-1] == "model_2":
            assert len(filenames) == 2
            assert "model2-0017.params" not in filenames
            assert "model2-symbol.json" in filenames
