zappy='/home/tim/extra/dev/fosm' ; export zappy
export gtm_dist="$zappy/gtm"; export gtm_dist
gtmx="$zappy/gtmx"; export gtmx
gtmgbldir="$zappy/data/xapi.gld"; export gtmgbldir
gtmroutines="$zappy/scripts/o($zappy/scripts $zappy/serenji $gtmx) $gtm_dist/libgtmutil.so $gtm_dist"; export gtmroutines
gtm="$gtmx/gtmrun ^direct gtm"; export gtm
gtmrun="$gtmx/gtmrun" ; export gtmrun
mupip="$gtm_dist/mupip"; export mupip
lke="$gtm_dist/lke"; export lke
gde="$gtmx/gtmrun ^GDE"; export gde
dse="$gtm_dist/dse"; export dse
PATH=$PATH:$zappy/scripts:$gtm_dist
gtm_repl_instance="fosm02.repl";export gtm_repl_instance
gtm_repl_instname="fosm02";export gtm_repl_instname
export gtm_access_ci="$zappy/scripts/gtm_access.ci"
export gtm_data_dir="$zappy/data"

