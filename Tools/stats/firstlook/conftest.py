def pytest_addoption(parser):
    parser.addoption('--file1', action='store')
    parser.addoption('--file2', action='store')

def pytest_generate_tests(metafunc):
    file1 = metafunc.config.option.file1
    file2 = metafunc.config.option.file2

    if 'file1' in metafunc.fixturenames and 'file2' in metafunc.fixturenames:
        metafunc.parametrize('file1', [file1])
        metafunc.parametrize('file2', [file2])
    elif 'file1' in metafunc.fixturenames:
        metafunc.parametrize('file1', [file1])