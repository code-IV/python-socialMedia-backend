import pytest
import asyncio
from logs import logs 


# mock object pretending to send logs from a Docker container
async def ticker(delay, to):    
    for i in range(to):
        yield i
        await asyncio.sleep(delay)


class MockResponse:
    def __init__(self, delay, to):
        self.content = ticker(delay, to)
        
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass
    

@pytest.mark.asyncio
async def test_logs(mocker, capsys):
    to = 4
    delay = 1

    resp = MockResponse(delay, to)
    
    # Changing aiohttp method to pur mock
    mocker.patch('aiohttp.ClientSession.get', return_value=resp)

    cont = "my_container"
    name = "my_name"

    expected_output = ''.join([f'{name} {i}\n' for i in range(to)]) 

    # Executing the tested function
    await logs(cont, name)

    # Capturing the std out
    out, err = capsys.readouterr()

    # Printing output for additional verbosity
    print(out)

    assert out == expected_output
