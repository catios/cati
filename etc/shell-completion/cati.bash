# The Cati package manager shell completion
# This file is part of Cati package manager
# Copyright parsa shahmaleki <parsampsh@gmail.com>
# Under the GPL-v3

_CATI_MAIN_COMMANDS="help pkg list remove show state query search files finfo rdepends forget check repo update autoremove clear-cache download install upgrade full-upgrade"
_CATI_GENERAL_OPTIONS="--no-ansi"

_cati_help()
{
	COMPREPLY=($(compgen -W "-v --version ${_CATI_MAIN_COMMANDS}" -- "$thecur"))
}

_cati_pkg()
{
	COMPREPLY=($(compgen -f -W "--help install show build --without-scripts --target= --keep-conffiles --force -f" -- "$thecur"))
}

_cati_list()
{
	COMPREPLY=($(compgen -W "-q --quiet -v --verbose --help --installed -q --quiet -v --verbose --installed-manual --author= --maintiner= --category= --search= --upgradable" -- "$thecur"))
}

_CATI_REMOVE_COMMAND_OPTIONS="-y --yes --conffiles --without-scripts --force -f"

_cati_remove()
{
	COMPREPLY=($(compgen -W "--help $(ls /var/lib/cati/installed) ${_CATI_REMOVE_COMMAND_OPTIONS}" -- "$thecur"))
}

_cati_show()
{
	COMPREPLY=($(compgen -W "--help --versions $(ls /var/lib/cati/lists)" -- "$thecur"))
}

_cati_state()
{
	COMPREPLY=($(compgen -W "--help --abort --complete -y --yes" -- "$thecur"))
}

_cati_query()
{
	COMPREPLY=($(compgen -W "-q --quiet --help -q --quiet" -- "$thecur"))
}

_cati_files()
{
	COMPREPLY=($(compgen -W "-q --quiet --help --installed $(ls /var/lib/cati/lists)" -- "$thecur"))
}

_cati_finfo()
{
	COMPREPLY=($(compgen -fd))
}

_cati_rdepends()
{
	COMPREPLY=($(compgen -W "-q --quiet --help $(ls /var/lib/cati/lists)" -- "$thecur"))
}

_cati_forget()
{
	COMPREPLY=($(compgen -W "--help $(ls /var/lib/cati/lists)" -- "$thecur"))
}

_cati_check()
{
	COMPREPLY=($(compgen -W "--help -q --quiet -v --verbose" -- "$thecur"))
}

_cati_repo()
{
	COMPREPLY=($(compgen -W "--help -e --edit -a --add --scan" -- "$thecur"))
}

_cati_update()
{
	COMPREPLY=($(compgen -W "-v --verbose -q -quiet" -- "$thecur"))
}

_cati_autoremove()
{
	COMPREPLY=($(compgen -W "--help ${_CATI_REMOVE_COMMAND_OPTIONS}" -- "$thecur"))
}

_cati_download()
{
	COMPREPLY=($(compgen -W "-q --quiet --help $(ls /var/lib/cati/lists) --output= -o=" -- "$thecur"))
}

_CATI_INSTALL_COMMAND_OPTIONS="-y --yes --reinstall --download-only --with-recommends"

_cati_install()
{
	COMPREPLY=($(compgen -W "--help $(ls /var/lib/cati/lists) ${_CATI_INSTALL_COMMAND_OPTIONS}" -- "$thecur"))
}

_cati_upgrade()
{
	COMPREPLY=($(compgen -W "--help ${_CATI_INSTALL_COMMAND_OPTIONS}" -- "$thecur"))
}

_cati_full_upgrade()
{
	COMPREPLY=($(compgen -W "--help -y --yes" -- "$thecur"))
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
		rdepends) _cati_rdepends;;
		forget) _cati_forget;;
		check) _cati_check;;
		repo) _cati_repo;;
		update) _cati_update;;
		autoremove) _cati_autoremove;;
		clear-cache) _cati_update;;
		download) _cati_download;;
		install) _cati_install;;
		upgrade) _cati_upgrade;;
		full-upgrade) _cati_full_upgrade;;
	esac
}

complete -F _cati cati
