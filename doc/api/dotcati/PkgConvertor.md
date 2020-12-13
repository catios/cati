Module dotcati.PkgConvertor
===========================
Deb and Rpm to cati package convertor

Functions
---------

    
`convert_depends_list(debian_depends_control_value: str) ‑> list`
:   Converts the debian control file `depends/conflicts` items syntax to cati depends/conflicts list
    
    Args:
        debian_depends_control_value (str): value of package debian control field
    
    Returns:
        list: the list of depends/conflicts (converted to cati strcture)

    
`deb2cati(file_path: str) ‑> str`
:   Converts deb package to cati package and returns generated cati package file path
    
    Args:
        file_path: deb package filepath
    
    Returns:
        returns generated cati package filepath

    
`rpm2cati(file_path: str) ‑> str`
:   Converts rpm package to cati package and returns generated cati package file path
    
    Args:
        file_path: rpm package filepath
    
    Returns:
        returns generated cati package filepath