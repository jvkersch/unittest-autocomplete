UNITTEST_COMMAND=change this to the name of the unit test command

_complete()
{
  cur=${COMP_WORDS[COMP_CWORD]}
  completions=$( unittest-complete.py $cur )
  COMPREPLY=( $( compgen -W "$completions" -- $cur ) )
}
complete -o default -o nospace -F _complete $UNITTEST_COMMAND
