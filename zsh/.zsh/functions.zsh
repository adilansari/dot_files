# List permission strings (e.g. drwxr-xr-x) of subdirectories in the current directory.
# Example: dls
dls () {
	echo `ls -l | grep "^d" | awk '{ print $1 }' | tr -d "/"`
}

# Find files recursively by name; argument is a glob pattern.
# Example: dfind "*.py"   dfind "Makefile"
dfind(){
	find . -type f -name $1
}

# Recursive, case-insensitive grep in current dir; skips binary files and lines containing "env".
# Example: dgrep "TODO"   dgrep "function_name"
dgrep() {
	grep -iR "$1" * | grep -v "Binary"| grep -v "env"
}

# Like dgrep but prints only unique filenames that contain the search string.
# Example: dfgrep "import foo"   dfgrep "config"
dfgrep() {
	grep -iR "$1" * | grep -v "Binary"| grep -v "env" | sed 's/:/ /g' | awk '{ print $1 }' | sort | uniq
}

# Search running processes by name; matches the given pattern in ps aux output.
# Example: psgrep nginx   psgrep "python"
psgrep() {
	if [ ! -z $1 ] ; then
	echo "Grepping for processes matching $1..."
	ps aux | grep $1 | grep -v grep
else
	echo "!! Need name to grep for"
	fi
}
