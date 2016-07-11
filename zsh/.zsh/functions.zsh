dls () {
	# directory LS
	echo `ls -l | grep "^d" | awk '{ print $1 }' | tr -d "/"`
}
dfind(){
	# recursive search for filename/pattern
	find . -type f -name $1
}
dgrep() {
	# A recursive, case-insensitive grep that excludes binary files
	grep -iR "$1" * | grep -v "Binary"| grep -v "env"
}
dfgrep() {
	# A recursive, case-insensitive grep that excludes binary files
	# and returns only unique filenames
	grep -iR "$1" * | grep -v "Binary"| grep -v "env" | sed 's/:/ /g' | awk '{ print $1 }' | sort | uniq
}
psgrep() {
	if [ ! -z $1 ] ; then
	echo "Grepping for processes matching $1..."
	ps aux | grep $1 | grep -v grep
else
	echo "!! Need name to grep for"
	fi
}
