# pylint: disable=missing-function-docstring

def test_commands_loaddb(runner):
    result = runner.invoke(args=["loaddb", "./appli/data/init"])
    assert result.output == ""

def test_commands_savedb(runner):
    result = runner.invoke(args=["savedb", "./appli/data/init"])
    assert result.output == ""
