# Dister
Dister - Distributed runner for python tasks

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
