# The Cati package manager shell completion
# This file is part of Cati package manager
# Copyright parsa shahmaleki <parsampsh@gmail.com>
# Under the GPL-v3

_CATI_MAIN_COMMANDS="help pkg list remove show state query search files finfo"
_CATI_GENERAL_OPTIONS="--no-ansi -h --help"

_cati_help()
{
	COMPREPLY=($(compgen -W "-v --version ${_CATI_MAIN_COMMANDS}" -- "$thecur"))
}

_cati_pkg()
{
	COMPREPLY=($(compgen -f -W "install show build --without-scripts --target= --keep-conffiles --force -f" -- "$thecur"))
}

_cati_list()
{
	COMPREPLY=($(compgen -W "--installed -q --quiet -v --verbose --installed-manual --author= --maintiner= --category= --search= --upgradable" -- "$thecur"))
}

_cati_remove()
{
	COMPREPLY=($(compgen -W "$(ls /var/lib/cati/installed) -y --yes --conffiles --without-scripts --force -f" -- "$thecur"))
}

_cati_show()
{
	COMPREPLY=($(compgen -W "--versions" -- "$thecur"))
}

_cati_state()
{
	COMPREPLY=($(compgen -W "--abort --complete -y --yes" -- "$thecur"))
}

_cati_query()
{
	COMPREPLY=($(compgen -W "-q --quiet" -- "$thecur"))
}

_cati_files()
{
	COMPREPLY=($(compgen -W "--installed $(ls /var/lib/cati/lists)" -- "$thecur"))
}

_cati_finfo()
{
	COMPREPLY=($(compgen -fd))
}

_cati() {
	local i=1 cmd

	while [[ "$i" -lt "$COMP_CWORD" ]]
	do
		local s="${COMP_WORDS[i]}"

		case "$s" in
			-*) ;;
			*)
			cmd="$s"
			break
			;;
		esac
		(( i++ ))
	done

	if [[ "$i" -eq "$COMP_CWORD" ]]
	then
		# the index
		local cur="${COMP_WORDS[COMP_CWORD]}"
		COMPREPLY=($(compgen -W "${_CATI_MAIN_COMMANDS} ${_CATI_GENERAL_OPTIONS}" -- "$cur"))
	fi

	thecur="${COMP_WORDS[$COMP_CWORD]}"
	case "$cmd" in
		help) _cati_help;;
		pkg) _cati_pkg;;
		list) _cati_list;;
		remove) _cati_remove;;
		show) _cati_show;;
		state) _cati_state;;
		query) _cati_query;;
		search);;
		files) _cati_files;;
		finfo) _cati_finfo;;
	esac
}

complete -F _cati cati

