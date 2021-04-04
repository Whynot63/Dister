import marshal

from tasks import exec_func


def check_status(base_url, path=None):
    url = urllib.parse.urljoin(base_url, path)
    r = requests.get(url)
    return r.status_code


result = exec_func.delay(
    marshal.dumps(check_status.__code__),
    {
        "requests": "requests==2.25.1",
        "urllib": None,
    },
    ("https://http.cat/",),
    {"path": "200"},
)

print(result.get(timeout=40))  # should print 200
