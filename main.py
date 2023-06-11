import code
import dis
import symtable

c = """
import io

def my_func(a, /, b, *, c, d=3):
    # a is positional-only 
    # c and d are keyword-only
    a *= 2
    f = 'a'
    def g():
        # All 3 variables will be in in g.__closure__, and their names in
        # g.__code__.co_freevars and its value 
        # All 3 will be in my_func.__code__.co_cellvars since they are
        # referenced by nested functions, but only 'b' and 'c' will be in
        # my_func.__code__.co_varnames (since they are args)!
        nonlocal b
        nonlocal f
        print(c)
    # ... but not x ! A closure only happens when an inner function is defined
    # in an outer function. For module-level functions, __closure__ will be
    # None, and here 'x' will be in co_names, and its value in
    # my_func.__globals__
    print(x)
    return a + e

l = [i for i in range(3)]
x = 'xx'
b = my_func(3)
print(b)
"""


def print_code_info(co: code):
    """Print all co_... attributes of a code object"""
    attrs = [
        # --- Main attributes
        #
        # Raw bytecode instructions and arguments (run dis.dis(co.co_code) to
        # print the human-readable version)
        "co_code",
        # Function name if the code object is a function code object, else
        # '<module>'
        "co_name",
        # Tuple with "the literals used by the bytecode" (?)
        "co_consts",
        # Tuple with the names used by the bytecode
        "co_names",
        #
        # --- Attributes useful for functions only
        #
        # For functions, the number of arguments (positional args including
        # ones with default values, positional-only, keyword-only). Else, 0 ?
        "co_argcount",
        "co_posonlyargcount",
        "co_kwonlyargcount",
        # Local variables used by the function (including the args): number of
        # variables and tuple with their names (starting with the args)
        # (?) do we always have co_nlocals == len(co_varnames) ? it would seem
        # so...
        # https://github.com/python/cpython/blob/d636d7dfe714e7168b342c7ea5f9f9d3b3569ed0/Objects/codeobject.c#L694
        "co_nlocals",
        "co_varnames",
        # Names of local variables referenced by nested functions. Note that
        # non-args local variables appearing here will NOT be in co_varnames.
        "co_cellvars",
        # Names of "free variables", which seems to refer to the variables
        # inside a function's closure (if any)
        "co_freevars",
        #
        # --- Miscellaneous
        #
        # File name from which the code was compiled
        "co_filename",
        # Line number and bytecode offsets
        "co_firstlineno",
        "co_lnotab",
        # Required stack size (?)
        "co_stacksize",
        # Number of flags for the interpreter (?)
        "co_flags",
    ]
    assert set(attrs) == set(x for x in dir(co) if x.startswith("co_"))
    for x in attrs:
        print(f"co.{x} = {getattr(co, x)}")


def main():
    # Get the symbol table (= list of namespaces, locals, globals for the
    # compiler to use)
    t = symtable.symtable(c, "filename.py", "exec")
    # Print all symbols in the top namespace
    print(t.get_symbols())
    # Print the children namespaces (if any)
    print(t.get_children())
    # (?)
    # What is a namespace? it seems to be a block of code inside which you
    # have a number of variables defined. A function has its own namespace for
    # instance, but an imported module does not (since it's simply an object?)
    # Edit: actually, for a module, its namespace is a readonly dict object
    # (m.__dict__)

    # Get a code object from a source file
    co = compile(c, "filename.py", "exec")
    # Print the raw bytecode instructions (with human-readable names)
    dis.dis(co.co_code)
    #
    print(co.co_name)

    # Print the associated bytecode (= list of instructions)
    dis.dis(c)


if __name__ == "__main__":
    main()
