Module cmdline.ArgParser
========================
Cli argument parser

Functions
---------

    
`parse(args: list) ‑> dict`
:   Gets a list from program arguments and returns parsed args
    
    parsed arguments output structure:
    {
        ## all of arguments where starts with `-` (dict)
        "options": {
            "--option1": "value",
            "--option2": None, ## value will be None when option has not value
            ## ...
        },
    
        ## all of non-option arguemnt (list)
        "arguments": [
            "arg1",
            "arg2",
            ## ...
        ]
    }