# https://click.palletsprojects.com/en/8.0.x/testing/

from click.testing import CliRunner

from rachleff.main import get_data


def test_get_data() -> None:
    """Use optional argument to grab only one year."""
    runner = CliRunner()
    # standalone_mode=False gives the return_value
    result = runner.invoke(get_data, ["--test"], standalone_mode=False)
    assert result.exit_code == 0


if __name__ == "__main__":
    test_get_data()
