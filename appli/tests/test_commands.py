# pylint: disable=missing-function-docstring

def test_commands_loaddb(runner):
    result = runner.invoke(args=["loaddb", "./appli/data"])
    assert result.output == ""
