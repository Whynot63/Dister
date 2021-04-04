# Dister
Dister - Distributed runner for python tasks

# Example
```python
# see actual version in https://github.com/Whynot63/Dister/blob/master/src/example.py


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
```

# WTF?

This repo shows how organize parallel execution of python scripts. It takes requirements, function code and functions args, run it and returns result.


# Restrictions

## Single function
You should use in your functions only modules without another function. To run multiple functions just wrap all of them to single function and exec this. 


before
```python
def a():
    ...
   
def b():
    a()
   
exec_func(b)
```


after
```python
def main():
    def a():
        ...
   
    def b():
        a()
        
    return b()
    
exec_func(main)
```

## Packages with not common build
If package should be build from source, then you cannot use Dister. :( 
